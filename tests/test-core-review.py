#!/usr/bin/env python3
"""Synthetic regressions for PR 39 core and timezone review findings.

Run from any directory: python3 tests/test-core-review.py
Requires Python 3, Git, Bash and jq; never reads the pilot profile.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import struct
import tempfile


SOURCE = Path(__file__).resolve().parents[1]
ENV = {key: value for key, value in os.environ.items()
       if not key.startswith(('PROJECT_OS_', 'GIT_'))}
ENV.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
RESULTS = []


def verify(label, command, directory, expected, extra, source_label,
           diagnostic=None):
    env = ENV.copy()
    env.update(extra)
    result = subprocess.run(command, cwd=directory, env=env, text=True,
                            capture_output=True)
    output = result.stdout + result.stderr
    assert result.returncode == expected, (label, result.returncode, output)
    assert source_label in output, (label, output)
    if diagnostic:
        assert output.strip() == diagnostic, (label, output)
        assert 'off —' not in output and 'on —' not in output, (label, output)
    for address in ('author@example.invalid', 'other@example.invalid'):
        assert address not in output, (label, 'address in diagnostic')
    RESULTS.append(f'{label}: PASS; exit={result.returncode}')


def notion_profile(portfolio):
    result = {'schema_version': 1, 'notes': {'mode': 'notion', 'notion': {
        'home_page': 'https://example.invalid/home',
        'status_page': 'https://example.invalid/status',
        'articles_database': {'id': 'synthetic-articles', 'name': 'Articles'},
        'schema_fields': {key: key.title() for key in
                          ('status', 'type', 'repo', 'source', 'updated', 'project')},
    }}}
    if portfolio is not None:
        result['registry'] = {'portfolio_exists': portfolio}
    if portfolio:
        result['notes']['notion']['portfolio_database'] = {
            'id': 'synthetic-portfolio', 'name': 'Portfolio'}
        result['notes']['notion']['schema_fields'].update(
            perspective='Perspective', start_date='Start date')
    return result


def remove(value, path, blank=False):
    value = copy.deepcopy(value)
    target = value['notes']['notion']
    for key in path[:-1]:
        target = target[key]
    if blank:
        target[path[-1]] = ''
    else:
        del target[path[-1]]
    return value


with tempfile.TemporaryDirectory(prefix='project-os-review-') as temp:
    directory = Path(temp)
    profile_file = directory / 'selected.json'

    def profile_case(label, value, diagnostic=None):
        profile_file.write_text(json.dumps(value))
        verify(label, ['bash', str(SOURCE / 'scripts/project-os-config.sh')],
               directory, 1 if diagnostic else 0,
               {'PROJECT_OS_PROFILE': str(profile_file)},
               diagnostic or 'on — PROJECT_OS_PROFILE', diagnostic)

    common_error = 'configuration source: error — missing notion destination or schema field'
    portfolio_error = 'configuration source: error — missing notion portfolio destination or schema field'
    common = [('home_page',), ('status_page',),
              ('articles_database', 'id'), ('articles_database', 'name')]
    common += [('schema_fields', key) for key in
               ('status', 'type', 'repo', 'source', 'updated', 'project')]
    for flag, label in ((False, 'false'), (None, 'omitted'), (True, 'true')):
        value = notion_profile(flag)
        profile_case(f'Notion / portfolio {label}', value)
        for path in common:
            profile_case(f'Notion / portfolio {label} / missing {".".join(path)}',
                         remove(value, path), common_error)
    portfolio_fields = [('portfolio_database', 'id'), ('portfolio_database', 'name'),
                        ('schema_fields', 'perspective'), ('schema_fields', 'start_date')]
    for path in portfolio_fields:
        for blank in (False, True):
            profile_case(f'Notion / portfolio true / {"empty" if blank else "missing"} {".".join(path)}',
                         remove(notion_profile(True), path, blank), portfolio_error)
    profile_case('Notion / empty common field',
                 remove(notion_profile(False), ('home_page',), True), common_error)
    value = notion_profile(False)
    value['notes']['notion']['portfolio_database'] = {'id': 7}
    profile_case('Disabled portfolio retains type validation', value,
                 'configuration source: error — invalid field type')
    for mode in ('none', 'markdown'):
        value = {'schema_version': 1, 'registry': {'portfolio_exists': True},
                 'notes': {'mode': mode}}
        if mode == 'markdown':
            value['notes']['markdown'] = {'destination_folder': 'synthetic-notes'}
        profile_case(f'{mode} mode / portfolio true needs no notion fields', value)

    def git(*args):
        return subprocess.check_output(['git', *args], cwd=directory, env=ENV,
                                       text=True, stderr=subprocess.PIPE).strip()

    def commit(email='author@example.invalid'):
        git('-c', 'user.name=Synthetic Author', '-c', f'user.email={email}',
            '-c', 'commit.gpgsign=false', 'commit', '--allow-empty', '-qm',
            'Synthetic review regression')
        return git('rev-parse', 'HEAD')

    git('init', '-q', '--template=')
    no_profile_base = commit()
    no_profile_head = commit('other@example.invalid')
    private = directory / 'private/project-os.json'
    private.parent.mkdir()
    private.write_text(json.dumps({'schema_version': 1, 'commit_email': {
        'enforce': True, 'address': 'author@example.invalid'}}))
    git('add', 'private/project-os.json')
    policy_base = commit()
    matching_head = commit()
    other_head = commit('other@example.invalid')

    def ci_case(label, base, head, expected, variable, source_label,
                diagnostic=None):
        extra = {'PROJECT_OS_CI': '1'}
        if variable is not None:
            extra['PROJECT_OS_COMMIT_EMAIL'] = variable
        verify(label, ['bash', str(SOURCE / 'scripts/check-commits.sh'), base, head],
               directory, expected, extra, source_label, diagnostic)

    invalid = 'configuration source: error — invalid repository variable'
    whitespace = (' ', '   ', '\t', '\n', '\r', '\v\f', ' \t\n\r ')
    for index, variable in enumerate(whitespace, 1):
        for base, head, label in ((policy_base, matching_head, 'with base policy'),
                                  (no_profile_base, no_profile_head, 'without base policy')):
            ci_case(f'CI whitespace variant {index} / {label}', base, head,
                    1, variable, invalid, invalid)
    for variable, label in ((None, 'unset'), ('', 'empty')):
        ci_case(f'CI {label} / tracked match', policy_base, matching_head,
                0, variable, 'on — tracked profile')
        ci_case(f'CI {label} / tracked mismatch', matching_head, other_head,
                1, variable, 'on — tracked profile')
        ci_case(f'CI {label} / no base profile', no_profile_base, no_profile_head,
                0, variable, 'off — no configuration')
    ci_case('CI nonblank variable wins / match', matching_head, other_head,
            0, 'other@example.invalid', 'on — repository variable')
    ci_case('CI nonblank variable wins / mismatch', policy_base, matching_head,
            1, 'other@example.invalid', 'on — repository variable')
    ci_case('CI nonblank padded value remains exact', matching_head, other_head,
            1, ' other@example.invalid ', 'on — repository variable')

# Self-contained trusted-data fixtures test name lookup, not offset calculation.
with tempfile.TemporaryDirectory(prefix='project-os-timezone-') as temp:
    directory = Path(temp)
    zone_root = directory / 'zoneinfo'
    tzif = (b'TZif' + b'\0' * 16 + struct.pack('>6l', 0, 0, 0, 0, 1, 4)
            + struct.pack('>lbb', 0, 0, 0) + b'UTC\0')
    for name in ('Etc/UTC', 'America/New_York', 'US/Eastern', 'localtime',
                 'posixrules', 'posix/America/New_York', 'right/America/New_York'):
        path = zone_root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(tzif)
    bad_file = zone_root / 'Europe/Bad_Data'
    bad_file.parent.mkdir(parents=True, exist_ok=True)
    bad_file.write_text('Synthetic non-TZif metadata')
    invalid = 'configuration source: error — invalid timezone'
    unavailable = 'configuration source: error — timezone data unavailable'
    field_type = 'configuration source: error — invalid field type'
    selected = directory / 'selected.json'

    def timezone_case(label, value, diagnostic=None, data_root=zone_root):
        selected.write_text(json.dumps(value))
        verify('Timezone / ' + label,
               ['bash', str(SOURCE / 'scripts/project-os-config.sh')],
               directory, 1 if diagnostic else 0,
               {'PROJECT_OS_PROFILE': str(selected), 'TZDIR': str(data_root)},
               diagnostic or 'on — PROJECT_OS_PROFILE', diagnostic)

    timezone_case('omitted default without data', {'schema_version': 1},
                  data_root=directory / 'missing-data')
    timezone_case('explicit default without data',
                  {'schema_version': 1, 'timezone': 'Etc/UTC'},
                  data_root=directory / 'missing-data')
    for name in ('America/New_York', 'US/Eastern'):
        timezone_case('valid ' + name, {'schema_version': 1, 'timezone': name})
    for label, name in (
        ('invented', 'Mars/Olympus'), ('typo', 'America/NewYork'),
        ('Windows ID', 'Eastern Standard Time'), ('empty', ''), ('whitespace', '   '),
        ('traversal', '../Etc/UTC'), ('absolute', '/Etc/UTC'),
        ('host-local alias', 'localtime'), ('rule file', 'posixrules'),
        ('posix namespace', 'posix/America/New_York'),
        ('right namespace', 'right/America/New_York'),
        ('non-TZif file', 'Europe/Bad_Data'), ('redacted invalid value', 'author@example.invalid'),
    ):
        timezone_case(label, {'schema_version': 1, 'timezone': name}, invalid)
    # These exact JSON strings must never normalize into valid shell names.
    malformed_strings = (
        ('single trailing LF', 'Etc/UTC\n'),
        ('multiple trailing LF', 'Etc/UTC\n\n'),
        ('canonical trailing LF', 'America/New_York\n'),
        ('trailing NUL', 'Etc/UTC\0'),
        ('interior NUL', 'America/\0New_York'),
        ('leading NUL', '\0Etc/UTC'),
        ('mixed NUL and LF', 'Etc/UTC\0\n'),
        ('trailing CRLF', 'Etc/UTC\r\n'),
    )
    for label, name in malformed_strings:
        timezone_case('exact string / CLI / ' + label,
                      {'schema_version': 1, 'timezone': name}, invalid)
    for label, value in (('number', 42), ('null', None), ('boolean', False), ('array', [])):
        timezone_case(label, {'schema_version': 1, 'timezone': value}, field_type)
    timezone_case('relative TZDIR', {'schema_version': 1, 'timezone': 'America/New_York'},
                  data_root='zoneinfo')
    for label, root in (('missing database', directory / 'missing-data'),
                        ('empty TZDIR', '')):
        timezone_case(label, {'schema_version': 1, 'timezone': 'America/New_York'},
                      unavailable, root)
    broken = directory / 'broken-zoneinfo'
    (broken / 'Etc').mkdir(parents=True)
    (broken / 'Etc/UTC').write_text('Synthetic corrupt marker')
    timezone_case('non-TZif database marker',
                  {'schema_version': 1, 'timezone': 'America/New_York'}, unavailable, broken)

    # Every selected source uses the same semantic check; no profile fallback.
    for path, label in (('.config/project-os.local.json', 'local profile'),
                        ('private/project-os.json', 'tracked profile')):
        file = directory / path
        file.parent.mkdir(parents=True, exist_ok=True)
        for name, diagnostic in (('America/New_York', None), ('Mars/Olympus', invalid)):
            file.write_text(json.dumps({'schema_version': 1, 'timezone': name}))
            verify('Timezone / ' + label + (' valid' if not diagnostic else ' invalid'),
                   ['bash', str(SOURCE / 'scripts/project-os-config.sh')], directory,
                   1 if diagnostic else 0, {'TZDIR': str(zone_root)},
                   diagnostic or 'on — ' + label, diagnostic)
        for case_label, name in malformed_strings:
            file.write_text(json.dumps({'schema_version': 1, 'timezone': name}))
            verify('Timezone / exact string / ' + label + ' / ' + case_label,
                   ['bash', str(SOURCE / 'scripts/project-os-config.sh')], directory,
                   1, {'TZDIR': str(zone_root)}, invalid, invalid)
        file.unlink()

    # CI sees the pinned base profile, not a repaired/broken HEAD value.
    def tz_git(*args):
        return subprocess.check_output(['git', *args], cwd=directory, env=ENV,
                                       text=True, stderr=subprocess.PIPE).strip()

    tz_git('init', '-q', '--template=')
    ci_file = directory / 'policy.json'
    def tz_commit(name):
        ci_file.write_text(json.dumps({'schema_version': 1, 'timezone': name}))
        tz_git('add', 'policy.json')
        tz_git('-c', 'user.name=Synthetic Author', '-c', 'user.email=author@example.invalid',
               '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Synthetic timezone policy')
        return tz_git('rev-parse', 'HEAD')

    bad_base = tz_commit('Mars/Olympus')
    good_base = tz_commit('America/New_York')
    ci_env = {'PROJECT_OS_CI': '1', 'PROJECT_OS_COMMIT_EMAIL': '',
              'PROJECT_OS_PROFILE': 'policy.json', 'TZDIR': str(zone_root)}
    command = ['bash', str(SOURCE / 'scripts/project-os-config.sh')]
    verify('Timezone / CI invalid base despite valid HEAD', command + [bad_base],
           directory, 1, ci_env, invalid, invalid)
    tz_commit('Mars/Olympus')
    verify('Timezone / CI valid base despite invalid HEAD', command + [good_base],
           directory, 0, ci_env, 'on — PROJECT_OS_PROFILE')
    for label, name in malformed_strings:
        malformed_base = tz_commit(name)
        tz_commit('America/New_York')
        verify('Timezone / exact string / pinned CI / ' + label,
               command + [malformed_base], directory, 1, ci_env, invalid, invalid)
    tz_commit('Etc/UTC\n')
    verify('Timezone / CI valid base despite malformed exact HEAD', command + [good_base],
           directory, 0, ci_env, 'on — PROJECT_OS_PROFILE')
    verify('Timezone / CI override ignores malformed exact base', command + [malformed_base],
           directory, 0, {'PROJECT_OS_CI': '1', 'PROJECT_OS_PROFILE': 'policy.json',
                          'PROJECT_OS_COMMIT_EMAIL': 'author@example.invalid',
                          'TZDIR': str(directory / 'missing-data')}, 'on — repository variable')
    tz_commit('Mars/Olympus')
    ci_file.rename(directory / 'private/project-os.json')
    tz_git('add', 'policy.json', 'private/project-os.json')
    tz_git('-c', 'user.name=Synthetic Author', '-c', 'user.email=author@example.invalid',
           '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Synthetic tracked timezone policy')
    tracked_base = tz_git('rev-parse', 'HEAD')
    verify('Timezone / CI tracked invalid base', command + [tracked_base], directory, 1,
           {'PROJECT_OS_CI': '1', 'PROJECT_OS_COMMIT_EMAIL': '', 'TZDIR': str(zone_root)},
           invalid, invalid)
    verify('Timezone / CI whole repository-variable override', command + [tracked_base],
           directory, 0, {'PROJECT_OS_CI': '1', 'PROJECT_OS_COMMIT_EMAIL': 'author@example.invalid',
                          'TZDIR': str(directory / 'missing-data')}, 'on — repository variable')

print('\n'.join(RESULTS))
print(f'{len(RESULTS)} synthetic regression cases verified; PASS')
