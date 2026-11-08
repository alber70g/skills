"""Behavioral checks in disposable Git repositories; no live model calls."""
import csv
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'lab.py'
spec = importlib.util.spec_from_file_location('lab', SCRIPT)
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class LabTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('config', 'user.name', 'Test')
        (self.root / 'task.md').write_text('List action items with an owner. Do not invent owners.')
        self.git('add', 'task.md')
        self.git('commit', '-qm', 'baseline')
        self.sha = self.git('rev-parse', 'HEAD')

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], text=True).strip()

    def cli(self, *args, ok=True):
        result = subprocess.run(['python3', str(SCRIPT), '--root', str(self.root), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, ok, result.stderr)
        return result

    def test_archive_preserves_library_base_and_user_work(self):
        self.cli('init')
        state = self.root / '.harness2'
        (state / 'base' / 'H0.md').write_text('original')
        entry = state / 'library' / 'entry-001'
        entry.mkdir()
        (entry / 'EXPERIENCE.md').write_text('Observed an owner missing in run 0.')
        (state / 'runs' / 'trajectory.md').write_text('reference evidence')
        (self.root / 'task.md').write_text('uncommitted user edit')
        archive = Path(self.cli('archive').stdout.strip())
        self.assertEqual((state / 'base' / 'H0.md').read_text(), 'original')
        self.assertTrue((state / 'library' / 'entry-001' / 'EXPERIENCE.md').exists())
        self.assertTrue((archive / 'runs' / 'trajectory.md').exists())
        self.assertEqual(list((state / 'runs').iterdir()), [])
        self.assertEqual((self.root / 'task.md').read_text(), 'uncommitted user edit')
        self.git('check-ignore', '.harness2/config.md', str(archive / 'config.md'))
        self.cli('init', ok=False)

    def test_snapshot_is_complete_and_preserves_executable_mode(self):
        source = self.root / 'harness'
        (source / 'scripts').mkdir(parents=True)
        tool = source / 'scripts' / 'run.py'
        tool.write_text('print("owner: unknown")\n')
        tool.chmod(0o755)
        destination = self.root / 'snapshot'
        lab.snapshot(source, destination)
        self.assertEqual((destination / 'scripts/run.py').read_bytes(), tool.read_bytes())
        self.assertEqual((destination / 'scripts/run.py').stat().st_mode & 0o777, 0o755)
        with self.assertRaises(ValueError):
            lab.snapshot(source, destination)
        with self.assertRaises(ValueError):
            lab.snapshot(source, source / 'recursive')
        (source / 'leak').symlink_to(self.root / 'task.md')
        with self.assertRaises(ValueError):
            lab.snapshot(source, self.root / 'unsafe')

    def test_guard_rejects_scores_rubrics_links_and_embedded_fields(self):
        evidence = self.root / 'input'
        evidence.mkdir()
        (evidence / 'task.md').write_text('Extract action items and owners.')
        self.cli('guard', str(evidence))
        for name, body in [('scores.json', '{}'), ('rubric.md', 'secret'), ('notes.md', 'score: 99'), ('data.json', '{"score":99}')]:
            path = evidence / name
            path.write_text(body)
            self.cli('guard', str(evidence), ok=False)
            path.unlink()
        (evidence / 'source').symlink_to(self.root / 'task.md')
        self.cli('guard', str(evidence), ok=False)

    def test_record_requires_commit_and_keeps_parent_history(self):
        self.cli('init')
        self.cli('record', '--status', 'baseline', '--duration', '1', '--description', 'base', ok=False)
        for status, parent in [('baseline', []), ('discard', ['--parent', '0'])]:
            self.cli('record', '--status', status, '--commit', self.sha, '--duration', '1', '--description', 'run', *parent)
        self.cli('record', '--status', 'keep', '--commit', 'invalid', '--duration', '1', '--description', 'bad', ok=False)
        with (self.root / '.harness2/results.tsv').open() as handle:
            rows = list(csv.DictReader(handle, delimiter='\t'))
        self.assertEqual([r['experiment'] for r in rows], ['0', '1'])
        self.assertEqual(rows[1]['parent'], '0')
        self.assertEqual(rows[1]['metric'], '')
        self.assertEqual(rows[1]['commit'], self.sha)
        self.assertIn('discard', self.cli('status').stdout)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.sha)


if __name__ == '__main__':
    unittest.main()
