> Archived 2026-10-13. Superseded by [issue #5](https://github.com/kuroboshi007/goldbug-project-os-public/issues/5).
> Reason: Obsolete — supported native AGENTS.md loading replaces the verbal entry-point workaround within the observed scope.

Author: X (Codex)
Role: Implementer and evidence recorder
Session: 2026-10-13 r1

# Claude entry-point retirement evidence

This is a closed record of the retired text, the completed observation and its
limits. Issue #5 directs full removal with no replacement. Adoption and any later
candidate-specific evidence belong to the issue/PR record; this archive is not
active policy or a claim that every Claude surface loads project instructions.
The issue is the existing authoritative reference; no unassigned PR number is
invented.

## Retired text and compensated limitation

The two public entry files instructed Claude Code to open the canonical shared
AGENTS.md when it did not discover that file itself. They held no separate project
instructions. Their exact text at source base
`c95747d9a727233fbf0b85a5fec56a3fc2c14a93` follows.

Root CLAUDE.md:

```markdown
# Claude Code Entry Point

Read [`AGENTS.md`](AGENTS.md) completely before doing any work.

Then follow the read order and working rules defined there. `AGENTS.md` is the canonical shared instruction file for Codex, Claude Code, and other agents; this file exists only as a Claude Code entry point.

Do not create a separate Claude-specific process unless a real tool limitation requires one. If such a limitation is discovered, document the smallest necessary exception and propose it through a pull request.

That order includes resolving the active profile and reporting its source label; without a profile, the documented defaults apply.
```

Template templates/CLAUDE.md:

```markdown
# Claude Code Entry Point
Read [`AGENTS.md`](AGENTS.md) completely before doing any work.
Then follow the read order and working rules defined there.

That order includes resolving the active profile and reporting its source label; without a profile, the documented defaults apply.
```

## Official support, checked 2026-10-13

Source: [Claude Code memory documentation](https://code.claude.com/docs/en/memory).
Sections: AGENTS.md; When Claude Code reads AGENTS.md;
When AGENTS.md support is unavailable; Remove an earlier AGENTS.md workaround.

Direct AGENTS.md reading requires Code 2.1.277 or later. Default discovery uses it
when counting project/ancestor Claude instruction files are absent; user-scope
instructions do not suppress it. Older versions, a disabled built-in plugin and
some first-upgrade sessions can lack this support. The vendor distinguishes
native loading from a verbal redirect, which relies on a chosen file read, and
lists deletion of a verbal-only entry as a migration option. Native loading also
differs for hooks, additional directories and external imports; equivalence is
not assumed.

## Completed reachable observation

Observed 2026-10-13: desktop Local Code, embedded Claude Code 2.1.295,
desktop app 2.31226.1, macOS ARM64. The existing authenticated desktop session
completed a model response. No model, loading setting, sandbox mode, login or
additional macOS permission was changed. Trust was accepted once for the exact
previously approved isolated fixture; that does not authorize another folder.

The fixture was pinned to `c97ba30030d647c2853cd94263480b1dcdb133ec`, with
both entry files absent and the other 44 files unchanged. Its Git index/manifest
still described 46 files: this was a removal simulation, not a final 44-file
export or 45-file retirement tree. No counting ancestor suppressor was found;
one user-scope instruction remained, with contents neither read nor published.

Evidence for actual loading was the native context/Usage Memory files list,
which named the fixture-root AGENTS.md at about 2.3k tokens. A no-tool first prompt
asked for already-supplied project rules without naming the file or supplying
answers. It recalled reserved C/X marks, default notes none, the issue-number
branch pattern and the qualified Claude Code/coauthor trailer pair. No tool/file
read card appeared. The native loaded-file list supports the observation beyond
the model's own claim. Retained files and the two pre-existing omissions were
unchanged after the probe.

Capability limits: /config showed no matching Project instructions entry; no
setting was changed. /context and its loaded-file panel were observed. Native
/memory was NOT RUN: the picker search offered only an unrelated skill, which was
not invoked. A separate startup loading line was not exposed or captured.
These missing diagnostics alone do not demonstrate a loading failure.

Standalone CLI loading is NOT RUN: the existing standalone 2.1.282 and direct
bundled 2.1.295 CLI auth statuses were unauthenticated. That is separate from the
successful embedded desktop session. Other versions/platforms, ordinary Claude
chat, Cowork and Codex startup loading are NOT RUN; no behavior is inferred for
them. No live provider or account-permission test is claimed.

Observation SHA-256:
`8edb9d6353ee493ae6bb71bb18ee4ef18d954c6ee4dab22d8d992b7a600344a4`.
No private machine/account/session identifiers, paths, instruction contents or
signed private report links are included here.

## Strongest case for keeping the entry files

A pinned engine without native discovery, a counted project/ancestor instruction
file, a disabled reader, or a workflow relying on native/import loading differences
may still need deliberate discovery of shared instructions. Removing an entry
without noticing that limitation could leave the session without project rules.
The verbal entry itself was not proof of automatic loading. The maintainer chose
full removal, not a permanent import fallback; no existing user, ancestor, private
or downstream entry file is deleted or reconfigured by this public change.
An independent retirement reviewer must assess this keep-case; this author's
record is not independent approval.

## Source relationship and regression symptom

The observed c97ba300 fixture is seven commits and thirteen changed paths behind
implementation base c95747d9, including AGENTS.md. The actual retirement is based
on current main, not a wholesale copy of the old fixture. Loading on the final
retirement candidate was not part of the completed observation above.

A regression would be a reachable, supported no-redirect session whose native
loaded-file evidence omits the expected AGENTS.md or whose no-tool response lacks
its required rules despite the recorded prerequisites. Such an actual failure
requires specific evidence and pauses rollout; absent settings/diagnostic UI or
an unreachable unauthenticated CLI alone is not that failure. Any later remedy
belongs to a separately reviewed change, not an automatic replacement redirect.

This record is outside the export manifest. Its historical file names and quoted
text are not active references or startup entry points. The intended payload is
44 files; the source tree separately includes this record for 45 tracked files.
