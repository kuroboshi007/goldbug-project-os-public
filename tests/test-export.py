#!/usr/bin/env python3
"""Privacy/export regressions using fictional data in disposable local clones."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_READMES = ('README.md', 'README.zh-TW.md', 'README.ja.md')
ENV = {k: v for k, v in os.environ.items()
       if not k.startswith(('GIT_', 'PROJECT_OS_'))}
ENV.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)


def git(directory, *args):
    return subprocess.check_output(['git', *args], cwd=directory, env=ENV,
                                   text=True, stderr=subprocess.PIPE).strip()


def entries(directory):
    return [line for line in (directory / 'export/manifest.txt').read_text().splitlines()
            if line and not line.startswith('#')]


def mapped_source(name):
    return {'PROJECTS.md': 'export/PROJECTS.example.md',
            'archive/README.md': 'scripts/export-candidate.sh'}.get(name, name)


def committed_output(directory, name):
    source = mapped_source(name)
    content = subprocess.check_output(['git', 'show', 'HEAD:' + source],
                                      cwd=directory, env=ENV)
    if name == 'archive/README.md':
        prefix = b'# archive-readme:'
        content = b''.join(line[len(prefix):].removeprefix(b' ') for line in content.splitlines(keepends=True)
                           if line.startswith(prefix))
        return content, 0o644
    mode = git(directory, 'ls-tree', 'HEAD', '--', source).split()[0]
    return content, 0o755 if mode == '100755' else 0o644


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='project-os-export-test-')
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.seed = self.work / 'seed'
        self.seed.mkdir()
        for name in entries(ROOT):
            source = ROOT / mapped_source(name)
            target = self.seed / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if name == 'archive/README.md':
                target.write_text('FICTIONAL_PRIVATE_ARCHIVE_SENTINEL\n')
            else:
                shutil.copy2(source, target)
        (self.seed / 'PROJECTS.md').write_text('FICTIONAL_PRIVATE_REGISTRY_SENTINEL\n')
        git(self.seed, 'init', '-q', '--template=')
        git(self.seed, 'add', '.')
        git(self.seed, '-c', 'user.name=Synthetic Author',
            '-c', 'user.email=author@example.invalid', '-c', 'commit.gpgsign=false',
            'commit', '-qm', 'Synthetic export fixture')
        self.clone = self.work / 'clone'
        git(self.work, 'clone', '-q', '--no-local', str(self.seed), str(self.clone))
        self.destination = self.work / 'candidate'

    def export(self, expected=0, error=None):
        result = subprocess.run(['bash', str(self.clone / 'scripts/export-candidate.sh'),
                                 str(self.destination)], cwd=self.clone, env=ENV,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        if error:
            self.assertIn(error, result.stderr)
        return result

    def test_allowlist_synthetic_registry_and_new_tracked_private_file(self):
        for name in ('new-project-private.md', 'private/project-os.json',
                     'archive/proposals/synthetic-private.md', '.config/project-os.local.json',
                     'local-artifact.txt'):
            path = self.clone / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('FICTIONAL_PRIVATE_SENTINEL\n')
            git(self.clone, 'add', '-f', name)
        self.export()
        actual = sorted(path.relative_to(self.destination).as_posix()
                        for path in self.destination.rglob('*') if path.is_file())
        self.assertEqual(actual, sorted(entries(self.clone)))
        self.assertEqual((self.destination / 'PROJECTS.md').read_bytes(),
                         (self.clone / 'export/PROJECTS.example.md').read_bytes())
        self.assertTrue((self.destination / 'archive/README.md').is_file())
        self.assertFalse((self.destination / '.git').exists())
        self.assertFalse((self.destination / 'private').exists())
        self.assertFalse((self.destination / 'archive/proposals').exists())
        for path in self.destination.rglob('*'):
            if path.is_file() and path.name != 'test-export.py':
                self.assertNotIn(b'FICTIONAL_PRIVATE', path.read_bytes())

        # A deliberate manifest change is the only way a newly tracked file is admitted.
        manifest = self.clone / 'export/manifest.txt'
        manifest.write_text(manifest.read_text() + 'new-project-private.md\n')
        git(self.clone, 'add', 'export/manifest.txt', 'new-project-private.md')
        git(self.clone, '-c', 'user.name=Synthetic Author',
            '-c', 'user.email=author@example.invalid', '-c', 'commit.gpgsign=false',
            'commit', '-qm', 'Synthetic reviewed admission')
        self.destination = self.work / 'explicitly-admitted-candidate'
        self.export()
        self.assertEqual((self.destination / 'new-project-private.md').read_text(),
                         'FICTIONAL_PRIVATE_SENTINEL\n')

    def test_dirty_sources_and_manifest_are_refused(self):
        for name in ('README.md', 'export/PROJECTS.example.md',
                     'scripts/export-candidate.sh', 'export/manifest.txt'):
            path = self.clone / name
            original = path.read_text()
            for staged in (False, True):
                with self.subTest(source=name, staged=staged):
                    path.write_text(original + '# Synthetic unreviewed change\n')
                    if staged:
                        git(self.clone, 'add', name)
                    self.export(1, 'uncommitted manifest or export source')
                    self.assertFalse(self.destination.exists())
                    git(self.clone, 'reset', '-q', 'HEAD', '--', name)
                    path.write_text(original)

    def test_leading_dot_path_is_rejected(self):
        manifest = self.clone / 'export/manifest.txt'
        manifest.write_text(manifest.read_text() + './README.md\n')
        self.export(1, 'invalid manifest entry')
        self.assertFalse(self.destination.exists())

    def test_export_uses_commit_bytes_and_modes(self):
        self.export()
        for name in entries(self.clone):
            expected, mode = committed_output(self.clone, name)
            self.assertEqual((self.destination / name).read_bytes(), expected)
            self.assertEqual((self.destination / name).stat().st_mode & 0o777, mode)

    def test_optional_display_and_generic_archive_mapping(self):
        protected = (self.clone / 'archive/README.md').read_bytes()
        self.export()
        archive = self.destination / 'archive/README.md'
        self.assertEqual(archive.read_bytes(),
                         committed_output(self.clone, 'archive/README.md')[0])
        self.assertEqual((self.clone / 'archive/README.md').read_bytes(), protected)
        self.assertIn('Only the maintainer may delete', archive.read_text())
        self.assertNotRegex(archive.read_text(), r'Only [A-Za-z] may delete')
        readme = (self.destination / 'README.md').read_text()
        self.assertIn('goldBug Project OS', readme)
        for name in ('README.md', 'docs/configuration.md'):
            self.assertIn('freely change or omit', (self.destination / name).read_text())
        self.assertEqual(len(entries(self.clone)), 45)
        for name in (*PUBLIC_READMES, 'LICENSE'):
            self.assertIn(name, entries(self.clone))
            self.assertEqual((self.destination / name).read_bytes(),
                             committed_output(self.clone, name)[0])
        for name in PUBLIC_READMES:
            text = (self.destination / name).read_text()
            for other in PUBLIC_READMES:
                self.assertIn('](' + other + ')', text)
            self.assertIn('](LICENSE)', text)
        self.assertFalse((self.destination / 'export/ARCHIVE.README.example.md').exists())

    def test_downstream_reexports_with_customized_or_omitted_attribution(self):
        self.export()
        downstream = self.destination
        git(downstream, 'init', '-q', '--template=')
        paragraphs = {name: (downstream / name).read_text().split('\n\n')
                      for name in PUBLIC_READMES}
        legal_notice = (downstream / 'LICENSE').read_bytes()
        for label, credit in (
            ('initial', None),
            ('custom', '`goldBug Project OS` provides project rules built by A with AI collaborators.'),
            ('omitted', '`goldBug Project OS` provides project rules, playbooks, and templates.'),
        ):
            with self.subTest(attribution=label):
                for name in PUBLIC_READMES:
                    edited = paragraphs[name][:]
                    if credit is not None:
                        edited[1] = credit
                    (downstream / name).write_text('\n\n'.join(edited))
                git(downstream, 'add', '.')
                git(downstream, '-c', 'user.name=Synthetic Author',
                    '-c', 'user.email=author@example.invalid',
                    '-c', 'commit.gpgsign=false', 'commit', '--allow-empty', '-qm',
                    'Synthetic downstream ' + label)
                destination = self.work / ('downstream-' + label)
                result = subprocess.run(
                    ['bash', 'scripts/export-candidate.sh', str(destination)],
                    cwd=downstream, env=ENV, text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                actual = sorted(path.relative_to(destination).as_posix()
                                for path in destination.rglob('*') if path.is_file())
                self.assertEqual(actual, sorted(entries(downstream)))
                self.assertEqual(len(actual), 45)
                for name in entries(downstream):
                    expected, mode = committed_output(downstream, name)
                    self.assertEqual((destination / name).read_bytes(), expected)
                    self.assertEqual((destination / name).stat().st_mode & 0o777, mode)
                for name in PUBLIC_READMES:
                    self.assertEqual((destination / name).read_bytes(),
                                     (downstream / name).read_bytes())
                self.assertEqual((destination / 'LICENSE').read_bytes(), legal_notice)
                self.assertEqual((downstream / 'LICENSE').read_bytes(), legal_notice)

    def test_missing_embedded_template_fails_before_writing(self):
        script = self.clone / 'scripts/export-candidate.sh'
        script.write_text(''.join(line for line in script.read_text().splitlines(keepends=True)
                                  if not line.startswith('# archive-readme:')))
        git(self.clone, 'add', 'scripts/export-candidate.sh')
        git(self.clone, '-c', 'user.name=Synthetic Author',
            '-c', 'user.email=author@example.invalid', '-c', 'commit.gpgsign=false',
            'commit', '-qm', 'Synthetic missing archive template')
        self.export(1, 'missing embedded archive template')
        self.assertFalse(self.destination.exists())

    def test_existing_destination_is_untouched(self):
        self.destination.mkdir()
        sentinel = self.destination / 'owner-file'
        sentinel.write_text('Preserve this file')
        self.export(1, 'destination already exists')
        self.assertEqual(sentinel.read_text(), 'Preserve this file')
        self.assertEqual(list(self.destination.iterdir()), [sentinel])

    def test_forbidden_unsafe_and_duplicate_entries_fail_before_writing(self):
        manifest = self.clone / 'export/manifest.txt'
        original = manifest.read_text()
        for extra in ('private/project-os.json', '.git/config',
                      'archive/proposals/synthetic.md', '.config/project-os.local.json',
                      '.env', '../outside', '/outside', 'README.md'):
            with self.subTest(entry=extra):
                manifest.write_text(original + extra + '\n')
                self.export(1, 'export error:')
                self.assertFalse(self.destination.exists())

    def test_missing_and_untracked_sources_fail_before_writing(self):
        manifest = self.clone / 'export/manifest.txt'
        original = manifest.read_text()
        manifest.write_text(original + 'unreviewed.md\n')
        self.export(1, 'missing manifest source')
        self.assertFalse(self.destination.exists())
        (self.clone / 'unreviewed.md').write_text('Synthetic untracked file\n')
        self.export(1, 'untracked manifest source')
        self.assertFalse(self.destination.exists())

    def test_symlink_source_is_withheld(self):
        source = self.clone / 'README.md'
        source.unlink()
        source.symlink_to('PROJECTS.md')
        self.export(1, 'symlink source withheld')
        self.assertFalse(self.destination.exists())

    def test_symlink_parent_is_withheld(self):
        (self.clone / 'docs').rename(self.clone / 'actual-docs')
        (self.clone / 'docs').symlink_to('actual-docs', target_is_directory=True)
        self.export(1, 'symlink source withheld')
        self.assertFalse(self.destination.exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
