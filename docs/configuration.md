# Configuration contract

One JSON profile wins in full; fields never merge across profiles. Resolve before acting:
`PROJECT_OS_PROFILE` (explicit path, CLI/CI only) → `.config/project-os.local.json`
when present → `private/project-os.json` when present → built-in defaults.
The local profile is ignored; the tracked pilot profile is private and never exported.
Start with the synthetic [example](../.config/project-os.example.json).
No credentials belong in any profile. Use authorized connectors or CI secret storage.

Run `bash scripts/project-os-config.sh` from the OS checkout to validate and print
only the source label. Missing, unreadable, malformed, unsupported or invalid selected
profiles fail; withhold dependent work. A valid feature disabled by the selected profile
is not applicable. Never substitute another profile after an error. An unavailable
profile in a relay is `configuration unavailable`; name the affected action without guessing.

Every handoff states `OS revision: <commit>` and `configuration source: <label>`:
`off — no configuration`, `on — local profile`, `on — tracked profile`,
`on — PROJECT_OS_PROFILE`, or `error — <kind>`. Print labels, never contents.

## Schema version 1

Unknown keys at any level fail. Optional omitted fields take the defaults below;
that is not merging another profile. All containers are objects; text fields are strings,
flags booleans. Empty enabled-feature values fail. The synthetic example supplies every field.

| Field | Default | Requirement / consumer |
| --- | --- | --- |
| `schema_version` | None | Required, exactly `1`; missing/unknown versions are unsupported. |
| `maintainer.name` | `the maintainer` | Human-facing name; maintainer role wording stays neutral. |
| `maintainer.mark` | `M` | One letter, excluding reserved `C` and `X` (case insensitive); human authorship mark. |
| `maintainer.handle` | Empty | Optional public attribution; never a Git identity placeholder. |
| `commit_email.enforce` | `false` | Enables the repository author-email restriction. |
| `commit_email.address` | Empty | Required if enforcement is enabled; compared without printing it. |
| `language.operational` | `English` | Operational document language. |
| `language.summaries` | `English` | Prepared summaries and their Merged / Current state / Next headings. |
| `timezone` | `Etc/UTC` | IANA timezone for clock-based task caps; the task supplies its deadline. |
| `notes.mode` | `none` | `none`, `notion`, or `markdown`; see the [notes contract](notes.md). |
| `notes.notion.home_page` | Empty | Required in notion mode; notes home. |
| `notes.notion.status_page` | Empty | Required in notion mode; OS status destination; products use their designated page. |
| `notes.notion.portfolio_database.id` | Empty | Required in notion mode when `registry.portfolio_exists` is `true`; portfolio database. |
| `notes.notion.portfolio_database.name` | Empty | Required in notion mode when `registry.portfolio_exists` is `true`; portfolio display name. |
| `notes.notion.articles_database.id` | Empty | Required in notion mode; fallback articles destination. |
| `notes.notion.articles_database.name` | Empty | Required in notion mode; articles display name. |
| `notes.notion.schema_fields.status` | Empty | Required in notion mode; status field. |
| `notes.notion.schema_fields.type` | Empty | Required in notion mode; type field. |
| `notes.notion.schema_fields.perspective` | Empty | Required in notion mode when `registry.portfolio_exists` is `true`; portfolio perspective field. |
| `notes.notion.schema_fields.start_date` | Empty | Required in notion mode when `registry.portfolio_exists` is `true`; portfolio start-date field. |
| `notes.notion.schema_fields.repo` | Empty | Required in notion mode; source repository field. |
| `notes.notion.schema_fields.source` | Empty | Required in notion mode; source artifact field. |
| `notes.notion.schema_fields.updated` | Empty | Required in notion mode; synchronization-date field. |
| `notes.notion.schema_fields.project` | Empty | Required in notion mode; project field. |
| `notes.markdown.destination_folder` | Empty | Required in markdown mode; write only with destination approval. |
| `upstream.url` | Empty | Required to clone shared policy; never invent it if unavailable. |
| `upstream.sibling_checkout` | `../project-os` | Bootstrap hint for an existing OS checkout. |
| `registry.path` | `PROJECTS.md` | Operational registry location. |
| `registry.portfolio_exists` | `false` | Whether the configured notes provider owns portfolio facts. |
| `shared_services.announcement_channel.enabled` | `false` | Makes the optional integration available, never mandatory. |
| `shared_services.announcement_channel.how_to_url` | Empty | Required when enabled; private procedure destination. |

## Timezone validation

The loader checks timezone names after JSON/schema validation. Omission keeps
`Etc/UTC`; this known UTC default needs no timezone database. Other names and
aliases must identify readable TZif files in a trusted installed IANA zoneinfo
database. The loader uses the first available database at `/usr/share/zoneinfo`,
`/usr/share/lib/zoneinfo`, or `/usr/lib/zoneinfo`, identified by its `Etc/UTC` file.
Systems with another data location may set `TZDIR` to its directory (relative paths use the caller’s working directory);
an explicitly set unavailable directory does not fall back to system data.
Use OS-provided or trusted IANA data; the loader never downloads or installs it.

Unknown names, Windows display IDs, empty/whitespace values, path traversal and
the host-specific `localtime`/`posixrules` or `posix/`/`right/` namespaces fail with
`error — invalid timezone`. An unavailable/unreadable zoneinfo database for a custom name
fails with `error — timezone data unavailable`. Neither error prints the selected
value or data path, falls back to local time, or becomes `off`. Schema errors,
including non-string timezone values, retain their existing diagnostics. The same
check applies to CLI, local, tracked and base-pinned CI profiles; whole-profile
precedence, including the CI repository-variable override, is unchanged. Runtime
tools remain Bash, Git, jq and standard `head`; custom zones also need zoneinfo data.

## Display attribution

Display attribution is optional. Downstream users may freely change or omit it,
including the README credit. `maintainer.name` supplies customizable human-facing
labels; `maintainer.handle` is optional public attribution and may be empty. These
fields do not automatically rewrite the README or set a Git identity.
Without a profile, the name remains `the maintainer` and the handle is empty;
the example profile stays synthetic. Display choices do not change license or
copyright obligations.

## Commit-check policy

`bash scripts/check-commits.sh <base> <head>` resolves/validates the profile, checks
non-merge commits' emails only when enforced, and checks trailers both-or-neither.
Display names are unrestricted. No profile means email enforcement is off, not an error.

With `PROJECT_OS_CI=1`, the workflow environment/repository variable
`PROJECT_OS_COMMIT_EMAIL` wins for email policy (`on — repository variable`).
A nonempty whitespace-only value fails with `error — invalid repository variable`;
it never falls back or becomes a normalized address. Empty or unset values use the
fallback below; other nonempty values are compared exactly as supplied.
Otherwise read the tracked profile with `git show "$BASE_SHA:private/project-os.json"`,
or an explicit repository-relative `PROJECT_OS_PROFILE` at that same base revision.
No base profile means off; an explicitly selected missing profile means error.
The PR cannot disable the base profile's policy by editing its own profile. The
workflow/script remain PR-editable, as before; there is no privileged execution.
The migration PR uses the existing repository variable because its base has no profile.
Product workflow copies need all three: `check-commits.sh`, `project-os-config.sh`, and `profile.jq`.
Copies without a tracked profile run with email enforcement off unless that repository
sets `PROJECT_OS_COMMIT_EMAIL`.
