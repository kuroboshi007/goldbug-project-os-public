# Playbook: Bootstrap a Project

## Goal

Add the minimum OS functions without replacing useful existing documentation.

## Inspect

1. Read existing instructions, README, and project documentation.
2. Check the worktree, branch, validation commands, and recent merged work.
3. Confirm the project entry in `PROJECTS.md`.
4. Map existing files to the functions below.
5. Resolve the [profile](../docs/configuration.md), substitute `<maintainer>`, `<upstream-url>` and `<os-checkout-hint>` from its values/defaults, and decide the optional Shared services checklist in `PROJECT.md`. A missing upstream withholds cloning; placeholders are never Git identities.

## Minimum functions

- persistent agent instructions
- product definition and current status
- accepted decision history

Add task, handoff, or ADR locations only when the project needs them. If an equivalent exists, keep and link it instead of copying it into this layout:

```text
AGENTS.md
PROJECT.md
STATUS.md
DECISIONS.md
```

Populate from repository evidence and the maintainer's confirmed decisions. Mark unknowns `To confirm`.

When the kit replaces an existing file instead of adding a new one, diff the two and list in the pull request every rule the old file carried that the new one does not. Onboarding has already dropped project safety rules this way without anyone noticing. What to leave out is the maintainer's call, not the agent's.

## Validate and deliver

- Links resolve and instructions do not conflict.
- Status and commands match the repository.
- No secret or unnecessary personal information was copied.
- Copy this repository's [pull request template](../.github/pull_request_template.md) to `.github/pull_request_template.md` and [commit checks workflow](../.github/workflows/commit-checks.yml) to `.github/workflows/commit-checks.yml`, along with `scripts/check-commits.sh`, `scripts/project-os-config.sh`, and `scripts/profile.jq`. Product copies without a tracked profile may opt in with the non-secret Actions repository variable `PROJECT_OS_COMMIT_EMAIL`.
- A draft PR identifies mapped/added files, remaining unknowns, and the first OS task.

## Deliver the summary

Apply [notes](../docs/notes.md) and the active profile's summary language.
Mode none completes onboarding without a notes account, summary block, destination
or outstanding synchronization. With a provider, prepare what the project is,
current state, its OS adoption and configured upstream, onboarding decisions and
remaining maintainer choices. Use the configured provider destination; do not guess.

For notion, apply the [provider guide](../docs/notion-sync.md), use a product article
database or the configured fallback, and fill the profile's schema fields. For
markdown, prepare the artifact for its configured folder; direct writing needs
destination approval. Record the verified destination in the product's `Notes:`
field when delivered, otherwise retain the artifact and state the remaining delivery.
Use `Not applicable`, `Prepared — delivery outstanding`, `Blocked: <reason>`, or
`Delivered` truthfully. No bidirectional sync or second registry is introduced.
