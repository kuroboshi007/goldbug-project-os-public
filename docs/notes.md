# Notes policy

Resolve the [active profile](configuration.md) before selecting a provider. GitHub owns
operational state; notes are confirmed human-facing summaries. When
`registry.portfolio_exists` is true, the configured portfolio owns status, type,
perspective and start-date facts. The operational registry owns approved onboarding,
onboarding state and repository URLs. Neither mirrors the other.

## Modes

- `none` (default): onboarding, tasks, review, merge and handoff need no notes account,
  destination, summary block or outstanding synchronization. Record `Not applicable`.
- `notion`: use [the provider guide](notion-sync.md) and profile destinations. Prepare
  the exact status update in `language.summaries`, updating one designated status page
  in place after a confirmed merge. No access means remaining delivery, not opt-out.
- `markdown`: prepare confirmed Markdown for `notes.markdown.destination_folder` in
  `language.summaries`. Direct writing needs an approved folder. Otherwise hand off
  the prepared artifact and record outstanding delivery. No plugin or daemon is needed.

A selected missing, unreadable, malformed, unsupported or invalid profile blocks its
dependent action with a diagnostic. Never turn an error or an undelivered write into
`none`. A valid disabled feature is not applicable.

## Delivery states

- `Not applicable`: mode is none, or this action has no notes obligation.
- `Prepared — delivery outstanding`: exact text/artifact exists; its external write
  remains undone (including an unapproved Markdown destination).
- `Blocked: <reason>`: required configuration, preparation or delivery is blocked;
  name the gap. Retain any prepared artifact rather than silently opting out.
- `Delivered`: a permitted write to the configured destination was verified.

Handoffs and PRs name the state and remaining delivery. Translate Merged / Current
state / Next and their text into `language.summaries`. A pre-merge draft describes
prepared work truthfully; it does not claim a merge or delivery.

## Confirmation gate

Unless the maintainer explicitly requests automatic synchronization for a content
type, wait for review or merge before creating or materially changing a summary
article. A merge confirms its status-page update. Onboarding summaries, milestones,
decisions, releases and reusable guides can merit an article; ordinary tasks do not.
Update existing summaries rather than duplicating them. No bidirectional sync: a
decision made in notes must be recorded in its GitHub source before implementation.

Never sync unapproved proposals, raw chat, debugging logs, speculation, duplicated
code detail, secrets or sensitive operational data. No provider is a second task tracker.
