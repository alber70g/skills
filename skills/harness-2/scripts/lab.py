#!/usr/bin/env python3
"""Local harness-2 evidence primitives. No model calls or destructive Git operations."""
import argparse
import csv
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys

FIELDS = ['experiment', 'branch', 'parent', 'commit', 'metric', 'status', 'duration_s', 'description']
STATUSES = ['baseline', 'keep', 'discard', 'crash', 'timeout', 'thought', 'interesting', 'interrupted']
SENSITIVE = re.compile(r'(^|[^a-z])(scores?|scoring|rubrics?|evaluat(?:or|ion)s?|grades?|ground.?truth|answer.?keys?|results)([^a-z]|$)', re.I)
LABEL = re.compile(r'^\s*[\s#*\-"\']*(?:score|metric|rubric|grade|ground_truth|answer_key|evaluation)(?:[\s"\']*[:=]|\s*\|)', re.I | re.M)


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


def lab_path(root):
    lab = root / '.harness2'
    if lab.is_symlink():
        raise ValueError('Lab may not be a symlink')
    return lab


def check_tree(source, evidence=False):
    if source.is_symlink() or not source.is_dir():
        raise ValueError(f'Expected a real directory: {source}')
    for path in source.rglob('*'):
        if path.is_symlink():
            raise ValueError(f'Symlink not allowed: {path}')
        if not path.is_file() and not path.is_dir():
            raise ValueError(f'Unsupported special file: {path}')
        if evidence and SENSITIVE.search(str(path.relative_to(source))):
            raise ValueError(f'Evaluation artifact in handoff: {path}')
        if evidence and path.is_file():
            try:
                body = path.read_text(encoding='utf-8')
            except (UnicodeError, ValueError) as exc:
                raise ValueError(f'Review and convert non-text evidence first: {path}') from exc
            if LABEL.search(body) or re.search(r'''["'](?:score|metric|rubric|grade|ground_truth|answer_key|evaluation)["']\s*:''', body, re.I):
                raise ValueError(f'Possible evaluation field in handoff: {path}')


def snapshot(source, destination):
    check_tree(source)
    source = source.resolve()
    destination = destination.absolute()
    if destination.exists() or destination.is_symlink():
        raise ValueError('Destination must not exist')
    if destination.resolve().is_relative_to(source):
        raise ValueError('Destination cannot be inside source')
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, copy_function=shutil.copy2)


def init(root):
    if Path(git(root, 'rev-parse', '--show-toplevel')).resolve() != root:
        raise ValueError('--root must be the Git project root')
    lab = lab_path(root)
    if lab.exists():
        raise ValueError('Existing lab: resume or archive first')
    ignore = root / '.gitignore'
    if ignore.is_symlink():
        raise ValueError('.gitignore may not be a symlink')
    text = ignore.read_text() if ignore.exists() else ''
    additions = [s for s in ['/.harness2/', '/.harness2.bak.*/'] if s not in text.splitlines()]
    if additions:
        ignore.write_text(text + ('\n' if text and not text.endswith('\n') else '') + '\n'.join(additions) + '\n')
    lab.mkdir()
    for folder in ['runs', 'library', 'base']:
        (lab / folder).mkdir()
    for name, body in {
        'config.md': '# Configuration\n\nFill agreed task, inputs, measure/direction, scope, constraints, eight-slot mapping, H₀, adapter, model/environment, k/mode, caps, termination, baseline, best and next phase before execution.\n',
        'log.md': '# Experiment log\n',
        'branches.md': '| Branch | Parent commit | Status | Experiments | Best | Notes |\n|---|---|---|---|---|---|\n',
        'parking-lot.md': '# Deferred ideas\n',
        'library/index.md': '# Improvement library\n\n| ID | Date | Task | Lesson |\n|---|---|---|---|\n',
    }.items():
        (lab / name).write_text(body)
    with (lab / 'results.tsv').open('w', newline='') as handle:
        csv.writer(handle, delimiter='\t').writerow(FIELDS)


def rows(lab):
    with (lab / 'results.tsv').open(newline='') as handle:
        return list(csv.DictReader(handle, delimiter='\t'))


def record(root, args):
    lab = lab_path(root)
    previous = rows(lab)
    number = int(previous[-1]['experiment']) + 1 if previous else 0
    if not math.isfinite(args.duration) or args.duration < 0:
        raise ValueError('Duration must be nonnegative')
    if args.status != 'thought' and not args.commit:
        raise ValueError('Real executions require a committed harness SHA')
    commit = git(root, 'rev-parse', '--verify', args.commit + '^{commit}') if args.commit else ''
    if args.parent is not None and str(args.parent) not in [r['experiment'] for r in previous]:
        raise ValueError('Parent experiment does not exist')
    row = [number, args.branch or git(root, 'branch', '--show-current'), args.parent if args.parent is not None else '', commit,
           args.metric, args.status, args.duration, args.description]
    with (lab / 'results.tsv').open('a', newline='') as handle:
        csv.writer(handle, delimiter='\t').writerow(row)
    with (lab / 'log.md').open('a') as handle:
        handle.write(f'\n## Experiment {number} — {args.description}\n\n' +
                     ' / '.join(f'{key}: {value}' for key, value in zip(FIELDS[1:], row[1:])) + '\n')
    print(number)


def archive(root):
    lab = lab_path(root)
    if not lab.is_dir():
        raise ValueError('No lab to archive')
    check_tree(lab)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    destination = root / ('.harness2.bak.' + stamp)
    lab.rename(destination)
    init(root)
    for name in ['library', 'base']:
        shutil.rmtree(lab / name)  # only newly initialized empty directories
        shutil.copytree(destination / name, lab / name)
    print(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd(), help='Git project root')
    commands = parser.add_subparsers(dest='action', required=True)
    commands.add_parser('init')
    commands.add_parser('status')
    commands.add_parser('archive')
    snap = commands.add_parser('snapshot', help='Copy a reviewed complete tree without overwriting')
    snap.add_argument('source', type=Path)
    snap.add_argument('destination', type=Path)
    guard = commands.add_parser('guard', help='Audit a prepared score-free session input directory')
    guard.add_argument('directory', type=Path)
    rec = commands.add_parser('record')
    rec.add_argument('--status', required=True, choices=STATUSES)
    rec.add_argument('--commit')
    rec.add_argument('--branch', help='Explicit branch for executions in another worktree')
    rec.add_argument('--parent', type=int)
    rec.add_argument('--metric', default='')
    rec.add_argument('--duration', type=float, required=True)
    rec.add_argument('--description', required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.action == 'init':
            init(root)
        elif args.action == 'archive':
            archive(root)
        elif args.action == 'snapshot':
            snapshot(args.source, args.destination)
        elif args.action == 'guard':
            check_tree(args.directory, evidence=True)
            print('Input audit passed; semantic review and runtime access controls still required.')
        elif args.action == 'record':
            record(root, args)
        elif args.action == 'status':
            lab = lab_path(root)
            if not lab.exists():
                print('No harness-2 lab')
                return
            history = rows(lab)
            print(json.dumps({'config': (lab / 'config.md').read_text(),
                              'experiments': len(history), 'baseline': history[0] if history else None,
                              'latest': history[-1] if history else None,
                              'library_entries': sorted(p.name for p in (lab / 'library').glob('entry-*') if p.is_dir())}, indent=2))
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
