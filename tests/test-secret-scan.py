#!/usr/bin/env python3
"""Run real scanner regressions: python3 tests/test-secret-scan.py /path/to/gitleaks.

Requires Gitleaks 8.24.3, Python 3 and Git. Fixtures contain synthetic tokens only;
they are created in a temporary directory and never contact a provider.
"""
import hashlib
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1]
SCANNER = str(Path(sys.argv.pop(1)).resolve()) if len(sys.argv) > 1 else 'gitleaks'
ENV = {key: value for key, value in os.environ.items()
       if not key.startswith(('GIT_', 'PROJECT_OS_', 'GITLEAKS_'))}
ENV.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
           GIT_TERMINAL_PROMPT='0', TZ='UTC', LC_ALL='C')
WORKFLOW = (SOURCE / '.github/workflows/os-checks.yml').read_text()
SCAN_LINES = [line.strip() for line in WORKFLOW.splitlines()
              if line.strip().startswith('"$scanner_dir/gitleaks" ')]
assert len(SCAN_LINES) == 1, 'The workflow must invoke the tested scanner command'
SCAN_ARGS = shlex.split(SCAN_LINES[0])[1:]
assert SCAN_ARGS[-1] == '.'


class SecretScanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='project-os-secret-scan-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.git('init', '-q', '--template=', '--initial-branch=main')

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.repo, env=ENV,
                                       stderr=subprocess.PIPE, text=True).strip()

    def commit(self, text):
        (self.repo / 'sample.txt').write_text(text)
        self.git('add', 'sample.txt')
        self.git('-c', 'user.name=Synthetic Scanner Fixture',
                 '-c', 'user.email=author@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Synthetic fixture')
        return self.git('rev-parse', 'HEAD')

    def synthetic_secret(self):
        # Construct only in scratch; no real credential is stored in this test.
        token = 'gh' + 'p_' + hashlib.sha256(self.id().encode()).hexdigest()[:36]
        return 'SYNTHETIC_TOKEN="' + token + '"\n'

    def scan(self, expected, repo=None):
        report = self.root / 'redacted-results.json'
        result = subprocess.run([SCANNER, *SCAN_ARGS[:-1], '--report-format=json',
                                 '--report-path=' + str(report), str(repo or self.repo)],
                                cwd=self.root, env=ENV, capture_output=True, text=True)
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, expected, output)
        if expected == 2:
            self.assertIn('leaks found', output)
            findings = report.read_text()
            self.assertIn('REDACTED', findings)
            token = self.synthetic_secret().split('"')[1]
            self.assertNotIn(token, output)
            self.assertNotIn(token, findings)
        return output

    def test_exact_scanner_version(self):
        self.assertEqual(subprocess.check_output([SCANNER, 'version'], env=ENV,
                                                 text=True).strip(), '8.24.3')

    def test_clean_single_root_commit(self):
        self.commit('clean root\n')
        self.assertIn('1 commits scanned', self.scan(0))

    def test_clean_multi_commit_first_push_rejects_old_parent_range(self):
        root = self.commit('clean root\n')
        self.commit('clean second\n')
        head = self.commit('clean third\n')
        old = subprocess.run(['git', 'log', '-p', root + '^..' + head],
                             cwd=self.repo, env=ENV, capture_output=True)
        self.assertNotEqual(old.returncode, 0)
        self.assertIn('3 commits scanned', self.scan(0))

    def test_root_secret_deleted_before_first_multi_commit_push(self):
        self.commit(self.synthetic_secret())
        self.commit('secret removed from current tree\n')
        self.scan(2)

    def test_later_secret_deleted_before_ordinary_push(self):
        self.commit('clean root\n')
        self.commit(self.synthetic_secret())
        self.commit('secret removed from current tree\n')
        self.scan(2)

    def test_merged_side_branch_secret_deleted_before_merge(self):
        self.commit('clean root\n')
        self.git('switch', '-qc', 'synthetic-side')
        self.commit(self.synthetic_secret())
        self.commit('clean before merge\n')
        self.git('switch', '-q', 'main')
        self.git('-c', 'user.name=Synthetic Scanner Fixture',
                 '-c', 'user.email=author@example.invalid',
                 '-c', 'commit.gpgsign=false', 'merge', '--no-ff', '-qm',
                 'Synthetic merge', 'synthetic-side')
        self.git('branch', '-D', 'synthetic-side')
        self.scan(2)

    def test_scanner_error_fails_instead_of_passing(self):
        missing = self.root / 'missing-repository'
        missing.mkdir()
        self.scan(1, missing)


if __name__ == '__main__':
    unittest.main()
