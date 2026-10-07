# goldBug Project OS

`goldBug Project OS` is a small, versioned set of project rules, playbooks, and templates built by k.goldbug.studio with AI collaborators.

[English](README.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md)

## Who it is for

For maintainers and AI collaborators who need clear project scope, current status, accepted decisions, review responsibilities, and handoffs across conversations. Copy the minimum templates into a project and fill them with confirmed facts; use the playbooks to guide work.

This is a project operating framework, not a computer operating system or an installed application. It does not create projects, run agents, synchronize notes, or publish repositories automatically. Public source repository: [goldbug-project-os-public](https://github.com/kuroboshi007/goldbug-project-os-public).

These three READMEs provide aligned starting guides. The linked rules and templates are currently in English. Follow the canonical [AGENTS.md read order](AGENTS.md#required-read-order); configuration and policy details live in the linked documents.

## Prerequisites

- Bash, Git, jq, and standard `head` for the supplied scripts.
- Python 3.9 or newer for the test suites.
- Trusted installed IANA zoneinfo data for a custom timezone; default `Etc/UTC` works without it.
- A GitHub repository and access only when adopting the issue/PR workflow. Notes accounts and optional services are not needed for the local quickstart.

The scripts are exercised in a Bash environment. Native Windows execution is not verified; validate the tools and timezone data in your chosen environment. `lychee` is optional for the offline link check below.

## Smallest local quickstart

Run from the directory containing this README. This example creates a fresh sibling directory; if `../my-project` already exists, choose a new name instead of overwriting it.

```bash
bash scripts/project-os-config.sh &&
mkdir ../my-project &&
cp templates/AGENTS.md templates/PROJECT.md templates/STATUS.md templates/DECISIONS.md ../my-project/
```

With no selected profile, the first command prints `configuration source: off — no configuration`. The new directory receives four documents:

| File | Fill in before asking an agent to work |
| --- | --- |
| `AGENTS.md` | Project name, authority, safety rules, validation commands, and the actual accessible policy location/checkout hint |
| `PROJECT.md` | Users, goals, non-goals, stack, and known validation commands |
| `STATUS.md` | Current state, next action, blockers, and risks |
| `DECISIONS.md` | Accepted decisions; leave undecided questions unconfirmed |

Replace template placeholders with confirmed information, or mark unknowns `To confirm`. Never execute a placeholder as a URL, command, or Git identity. No public upstream URL is assumed: an unset `upstream.url` withholds cloning. Ask an agent to read the project instructions and documents, then propose one bounded task and its validation plan. Add task, handoff, or ADR templates only when useful; Claude users may also copy `templates/CLAUDE.md`.

For an existing project, inspect and map its current documents and safety rules first; do not replace them blindly. Follow [Bootstrap a Project](playbooks/bootstrap-project.md) for complete onboarding, workflow copies, and review.

## Configuration and private information

No profile is required. Defaults use neutral maintainer labels, `Etc/UTC`, notes mode `none`, email enforcement off, no portfolio, and the optional announcement service disabled.

To customize a new local copy, create the ignored `.config/project-os.local.json` using the [synthetic example](.config/project-os.example.json), or start with this minimal valid profile:

```json
{"schema_version": 1}
```

Edit an existing local profile rather than overwriting it. Validate from the OS directory:

```bash
bash scripts/project-os-config.sh
```

The selected local file prints `configuration source: on — local profile`. Selection is whole-profile precedence, not a merge:

```text
PROJECT_OS_PROFILE → .config/project-os.local.json → private/project-os.json → built-in defaults
```

The public candidate contains no private pilot profile. The full example is fictional; replace its example destinations before enabling a service. Keep private destinations and operational project inventory out of public content, and never store credentials in any profile. A missing, unreadable, malformed, or invalid selected profile blocks dependent work; do not bypass it with defaults. See the [configuration contract](docs/configuration.md).

Prefer canonical IANA `Area/Location` names such as `Asia/Tokyo` or `America/New_York`. Backward aliases such as `US/Eastern` work only when the host's trusted zoneinfo database includes the corresponding readable TZif file; availability can differ between hosts. Default `Etc/UTC` is a special known case. Windows display names, surrounding whitespace, control characters, and path traversal are rejected without trimming. Use trusted `TZDIR` data only when needed. Validation checks name/file membership and TZif magic, not offsets, DST calculations, full TZif structure, or data authenticity. See [timezone validation](docs/configuration.md#timezone-validation).

## Optional integrations

[Notes mode](docs/notes.md) defaults to `none`: no account, destination, summary delivery, or outstanding synchronization is required. `markdown` prepares confirmed summaries for an approved folder; `notion` needs authorized provider access and configured destinations/schema. Follow the confirmation and delivery rules before any external write. Profiles and scripts do not perform automatic synchronization.

Portfolio tracking and announcement channels are optional and disabled by default. Each product explicitly chooses whether to use an enabled announcement channel; no shared service is a universal dependency. See [project lifecycle](docs/project-lifecycle.md) and [announcement channels](knowledge/shared-announcement-channel.md).

## Workflow and roles

1. The maintainer approves the outcome and makes meaningful product, privacy, publication, and merge decisions.
2. An agent records a bounded GitHub issue, implements on a branch, and opens a draft PR.
3. A different agent reviews the complete change and evidence.
4. The maintainer resolves remaining decisions and merges.
5. Apply the selected notes mode only to confirmed information, then promote reusable learning through a separate OS issue/PR.

GitHub holds operational records; project documents hold project facts and accepted decisions. Notes hold confirmed human-facing summaries, not competing task state. Report the OS revision and configuration source in handoffs. Agent commits follow the qualified, consecutive trailers in [authorship marks](AGENTS.md#authorship-marks); display profile fields do not set a Git identity. See [operating model](docs/operating-model.md), [collaboration](docs/ai-collaboration.md), and [review](playbooks/review-change.md).

## Validate and export

Run the supplied suites from the OS directory; they use isolated synthetic fixtures:

```bash
python3 tests/test-core-review.py
python3 tests/test-export.py
```

Export requires a committed Git checkout. An unpacked archive has no Git history: initialize and commit a reviewed snapshot with your own verified public identity before exporting. The exporter does not initialize Git, choose an identity, commit, or publish. Commit included edits first, then use a new destination:

```bash
bash scripts/export-candidate.sh ../public-candidate
```

The explicit [manifest](export/manifest.txt) includes the three READMEs and `LICENSE`. Every included file is read from the captured commit, preserving executable modes. `PROJECTS.md` uses the synthetic registry; `archive/README.md` uses the generic embedded template. Private profiles, local settings, history, and unlisted files are excluded. Existing destinations, unsafe paths, symlinks, and uncommitted included sources are refused. Adding a tracked file does not add it to the export.

If `lychee` is installed, the documented offline check is:

```bash
lychee --offline --no-progress --include-fragments --exclude-path 'archive/' './**/*.md'
```

Inspect actual exported bytes, modes, links, filenames, and privacy separately. Git does not preserve filesystem xattrs, resource forks, or owners; metadata sidecars can leak through a folder archive. The exporter is a local file export, not an archive/privacy certification. See [export review and packaging limits](docs/export.md).

## Repository map

`AGENTS.md` contains shared rules; `docs/` holds policy; `playbooks/` holds procedures; `templates/` holds the project kit. `knowledge/` holds reusable lessons and candidates, not automatically active policy. `archive/` is historical and not current authority. The exported `PROJECTS.md` is synthetic, not your operational portfolio.

## License and optional project credit

This repository includes the standard [MIT License](LICENSE), copyright `2026 k.goldbug.studio`, as approved by the maintainer. MIT permits use, modification, commercial use, and redistribution subject to its terms, and provides no warranty. Preserve the copyright and permission notices when redistributing copies or substantial portions; keep any applicable third-party notices as well.

Display attribution is optional: downstream users may freely change or omit the project credit in these READMEs and customize `maintainer.name`/`maintainer.handle`. That optional project credit is separate from the required legal notices in `LICENSE`; changing display credit does not remove or replace them. See [display attribution](docs/configuration.md#display-attribution). Tagged releases remain a separate maintainer decision.
