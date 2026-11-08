"""Behavioral checks for stats.py in disposable directories; no model calls."""
import csv
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'stats.py'


class StatsTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.home = Path(temp.name).resolve()
        self.project = self.home / 'projects' / 'app'
        (self.project / 'src').mkdir(parents=True)
        subprocess.run(['git', 'init', '-q', str(self.project)], check=True)
        self.skill = self.home / 'projects' / 'skills' / 'skills' / 'commit'
        self.skill.mkdir(parents=True)
        (self.skill / 'SKILL.md').write_text('---\nname: commit\n---\n')

    def cli(self, *args, ok=True, run_in=None):
        env = {**os.environ, 'HOME': str(self.home)}
        result = subprocess.run(['python3', str(SCRIPT), *args], capture_output=True, text=True,
                                env=env, cwd=run_in or self.project)
        self.assertEqual(result.returncode == 0, ok, result.stderr)
        return result.stdout.strip()

    def review(self, score=1, **kw):
        return self.cli('session', '--agent', 'claude-code', '--session-id', 'abc', '--messages', '20',
                        '--mistake-score', str(score), '--skills', 'commit', **kw)

    def rows(self):
        with (self.project / '.review-session' / 'findings.tsv').open(newline='') as handle:
            return list(csv.DictReader(handle, delimiter='\t'))

    def test_skill_and_instruction_records_stay_in_the_project_not_the_skill_folder(self):
        # A skill's history belongs to the project it was applied to; skill folders stay clean.
        rid = self.review()
        self.cli('finding', '--review-id', rid, '--target', 'skill', '--skill', 'commit',
                 '--file', 'SKILL.md', '--q', '1', '--action', 'TUNE', '--eval-added', 'yes', '--note', 'branch check')
        self.cli('finding', '--review-id', rid, '--target', 'claude-md', '--file', 'CLAUDE.md',
                 '--action', 'TUNE', '--note', 'read before edit')
        self.cli('usage', '--review-id', rid, '--skill', 'commit', '--outcome', 'partial')
        self.assertEqual([(r['skill'], r['note']) for r in self.rows()],
                         [('commit', 'branch check'), ('', 'read before edit'), ('commit', '')])
        self.assertEqual(sorted(p.name for p in self.skill.iterdir()), ['SKILL.md'])

    def test_running_from_a_subdirectory_records_in_the_project_root(self):
        # Sessions started in src/ still belong to the project, so its history stays in one place.
        self.cli('session', '--agent', 'grok', '--session-id', 'unknown', '--messages', '5',
                 '--mistake-score', '0', '--session-cwd', '.', run_in=self.project / 'src')
        self.assertTrue((self.project / '.review-session' / 'sessions.tsv').exists())
        self.assertFalse((self.project / 'src' / '.review-session').exists())

    def test_status_flags_a_skill_file_tuned_in_two_reviews_and_tunes_without_eval(self):
        # A rule patched twice did not stick: the next review must rewrite it or enforce it differently.
        for score in (3, 1):
            rid = self.review(score)
            self.cli('finding', '--review-id', rid, '--target', 'skill', '--skill', 'commit',
                     '--file', 'SKILL.md', '--action', 'TUNE', '--note', f'patch {score}')
        report = json.loads(self.cli('status'))
        self.assertEqual(report['mistake_scores'], [3, 1])
        self.assertEqual(report['skills']['commit']['repeat_tunes'], {'SKILL.md': 2})
        self.assertEqual(len(report['skills']['commit']['tunes_without_eval']), 2)
        self.assertEqual(report['instructions']['findings'], 0)

    def test_records_need_a_recorded_review_and_skill_records_need_a_name(self):
        self.cli('finding', '--review-id', 'missing', '--target', 'memory', '--action', 'NONE', ok=False)
        rid = self.review()
        self.cli('finding', '--review-id', rid, '--target', 'skill', '--action', 'TUNE', ok=False)

    def test_local_records_are_ignored_by_git(self):
        self.review()
        subprocess.run(['git', '-C', str(self.project), 'check-ignore', '-q', '.review-session/sessions.tsv'], check=True)


if __name__ == '__main__':
    unittest.main()
