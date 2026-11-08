#!/usr/bin/env python3
"""Record /review-session results in the project the session worked on, and report trends.

All records go to <project>/.review-session/: the review itself, each finding (about a skill,
CLAUDE.md, AGENTS.md, memory, settings or hooks) and each skill's usage outcome. <project> is
--project, else the Git root of the current directory, else the current directory.
Standard library only; no model calls, no Git writes.
"""
import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

SESSION_FIELDS = ['review_id', 'date', 'agent', 'session_id', 'cwd', 'messages', 'mistake_score', 'skills']
RECORD_FIELDS = ['review_id', 'date', 'agent', 'kind', 'skill', 'outcome', 'target', 'file', 'q', 'action', 'eval_added', 'note']
TARGETS = ['skill', 'claude-md', 'agents-md', 'memory', 'settings', 'hook', 'other', 'none']
ACTIONS = ['TUNE', 'GROW', 'RETIRE', 'NONE']


def clean(value):
    return ' '.join(str(value).split())


def home_relative(path):
    try:
        return '~/' + str(path.relative_to(Path.home().resolve()))
    except ValueError:
        return str(path)


def default_project():
    here = Path.cwd()
    try:
        out = subprocess.run(['git', '-C', str(here), 'rev-parse', '--show-toplevel'],
                             capture_output=True, text=True, check=True).stdout.strip()
        return Path(out)
    except (OSError, subprocess.CalledProcessError):
        return here


def read(path):
    if not path.exists():
        return []
    with path.open(newline='') as handle:
        return list(csv.DictReader(handle, delimiter='\t'))


def store(project, name):
    folder = project / '.review-session'
    if not folder.exists():
        folder.mkdir(parents=True)
        (folder / '.gitignore').write_text('*\n')  # local evidence; never committed
    return folder / name


def append(path, fields, row):
    new = not path.exists()
    with path.open('a', newline='') as handle:
        writer = csv.writer(handle, delimiter='\t')
        if new:
            writer.writerow(fields)
        writer.writerow([clean(row.get(f, '')) for f in fields])


def record_session(args):
    review_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    append(store(args.project, 'sessions.tsv'), SESSION_FIELDS, {
        'review_id': review_id, 'date': review_id[:8], 'agent': args.agent, 'session_id': args.session_id,
        'cwd': home_relative(args.session_cwd or args.project), 'messages': args.messages,
        'mistake_score': args.mistake_score, 'skills': args.skills})
    print(review_id)


def record_item(args, kind):
    sessions = {r['review_id']: r for r in read(args.project / '.review-session' / 'sessions.tsv')}
    if args.review_id not in sessions:
        raise ValueError(f'Unknown review id {args.review_id}; run the session command first')
    target = 'skill' if kind == 'usage' else args.target
    if target == 'skill' and not args.skill:
        raise ValueError('A skill record needs --skill <name>')
    row = {'review_id': args.review_id, 'date': sessions[args.review_id]['date'],
           'agent': sessions[args.review_id]['agent'], 'kind': kind, 'skill': args.skill or '',
           'target': target, 'note': args.note}
    if kind == 'usage':
        row['outcome'] = args.outcome
    else:
        row.update(file=args.file, q=args.q or '', action=args.action, eval_added=args.eval_added)
    path = store(args.project, 'findings.tsv')
    append(path, RECORD_FIELDS, row)
    print(path)


def summarize(rows):
    """Flag files tuned in 2+ reviews and TUNEs that got no regression eval."""
    findings = [r for r in rows if r['kind'] == 'finding']
    reviews_per_file = defaultdict(set)
    for r in findings:
        if r['action'] == 'TUNE' and r['file']:
            reviews_per_file[r['file']].add(r['review_id'])
    return {
        'findings': len(findings),
        'by_target': dict(Counter(r['target'] for r in findings)),
        'repeat_tunes': {f: len(ids) for f, ids in reviews_per_file.items() if len(ids) >= 2},
        'tunes_without_eval': [f"{r['review_id']} {r['file']}: {r['note']}" for r in findings
                               if r['action'] == 'TUNE' and r['eval_added'] != 'yes'],
        'usage': dict(Counter(r['outcome'] for r in rows if r['kind'] == 'usage')),
        'recent_notes': [f"{r['review_id']} {r['file']}: {r['note']}" for r in findings[-5:]],
    }


def status(args):
    folder = args.project / '.review-session'
    sessions = read(folder / 'sessions.tsv')
    rows = read(folder / 'findings.tsv')
    report = {'project': home_relative(args.project), 'reviews': len(sessions),
              'mistake_scores': [int(r['mistake_score']) for r in sessions if r['mistake_score'].isdigit()][-10:],
              'instructions': summarize([r for r in rows if not r['skill']]),
              'skills': {name: summarize([r for r in rows if r['skill'] == name])
                         for name in sorted({r['skill'] for r in rows if r['skill']})}}
    print(json.dumps(report, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, help='Project the session worked on (default: Git root of the current directory)')
    commands = parser.add_subparsers(dest='command', required=True)
    s = commands.add_parser('session', help='Record one review; prints its review id')
    s.add_argument('--agent', required=True, choices=['claude-code', 'grok'])
    s.add_argument('--session-id', required=True)
    s.add_argument('--session-cwd', type=Path, help='Working directory of the session, if not the project root')
    s.add_argument('--messages', type=int, required=True)
    s.add_argument('--mistake-score', type=int, required=True)
    s.add_argument('--skills', default='', help='Comma-separated skills used')
    f = commands.add_parser('finding', help='Record one correction and its fix')
    u = commands.add_parser('usage', help='Record the outcome of one skill used in the session')
    for p in (f, u):
        p.add_argument('--review-id', required=True)
        p.add_argument('--skill', help='Skill name, for skill findings and usage')
        p.add_argument('--note', default='')
    f.add_argument('--target', required=True, choices=TARGETS)
    f.add_argument('--file', default='', help='File changed, e.g. SKILL.md or CLAUDE.md')
    f.add_argument('--q', type=int, choices=range(1, 8))
    f.add_argument('--action', required=True, choices=ACTIONS)
    f.add_argument('--eval-added', default='no', choices=['yes', 'no'])
    u.add_argument('--outcome', required=True, choices=['success', 'partial', 'failed'])
    commands.add_parser('status', help='Report trends for the project and each skill used in it')
    args = parser.parse_args()
    args.project = (args.project or default_project()).resolve()
    if getattr(args, 'session_cwd', None):
        args.session_cwd = args.session_cwd.resolve()
    try:
        if args.command == 'session':
            record_session(args)
        elif args.command in ('finding', 'usage'):
            record_item(args, args.command)
        else:
            status(args)
    except (ValueError, OSError) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
