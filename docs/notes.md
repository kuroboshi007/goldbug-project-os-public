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
  both artifacts in `language.summaries` on the existing designated status page.
- `markdown`: use one repository-named Markdown file in the approved
  `notes.markdown.destination_folder`, with the same Latest and History sections in
  `language.summaries`. No plugin or daemon is needed.

A selected missing, unreadable, malformed, unsupported or invalid profile blocks its
dependent action with a diagnostic. Never turn an error or an undelivered write into
`none`. A valid disabled feature is not applicable.

## Two artifacts

Each meaningful merged PR contributes a History entry and a Latest summary.
History retains one line per PR, newest first:
`YYYY-MM-DD · owner/repo#<PR> · <one-line outcome> [· D-<id> when applicable]`.
Insert new entries without changing existing ones. Latest replaces Merged / Current
state / Next in place. Translate their labels and text into `language.summaries`.
These summaries do not replace GitHub or product operational records.

Before merge, the implementer puts both exact prepared texts and their separate
delivery states in the PR. A draft does not claim to have merged or been delivered.
Mode none records both as `Not applicable`, needs neither text nor a destination,
and never falls back to another provider.

## Delivery states

- `Not applicable`: mode is none, or this action has no notes obligation.
- `Prepared — delivery outstanding`: exact text/artifact exists; its external write
  remains undone (including an unapproved Markdown destination).
- `Blocked: <reason>`: required configuration, preparation or delivery is blocked;
  name the gap. Retain any prepared artifact rather than silently opting out.
- `Delivered`: full content at the configured destination matches the prepared
  artifact, verified by readback after a permitted write or a matching-content skip.

Record History and Latest separately in PRs and handoffs. The overall state is the
least complete applicable state: Blocked before Prepared before Delivered; exclude
Not applicable. Retain successful partial delivery and both prepared texts on retry.

## Delivery and catch-up

After a confirmed merge, delivery is the final step of [Close](project-lifecycle.md#7-close).
Before any delivery or catch-up, resolve the active profile and provider, assign the
deliverer and verify existing tool access and destination authorization. The merge
confirms content; it grants no tool or destination permission. The authorized
implementer owns delivery; an authorized reviewer or relay with verified access may
take it over. The actual writer owns readback. The maintainer is not the default
messenger. If none has access, record the specific `Blocked: <reason>` and retain
the prepared text; do not assume a new grant or silently change providers.

Read the destination first, using `owner/repo#<PR>` as the History key. Matching
content skips the write and records readback. A different or incomplete entry needs
an explicit named repair of that entry or `Blocked: <mismatch>`; never silently
overwrite it or alter other History entries. After partial delivery, read again and
repair only the incomplete artifact, retaining matching content.

Replace Latest only when this PR's merge timestamp is later than that of the PR
currently represented, or no Latest exists; PR numbers do not determine order.
For the same PR, matching text skips the write; differing text requires an explicit
named repair or Blocked. If a newer confirmed Latest already exists, retain it and
record Latest as `Not applicable — newer confirmed summary retained`, with its PR
key and merge timestamp. Unknown ordering is `Blocked: <missing merge timestamp>`.

After writing or skipping matching content, read back the full History line and
all content of Merged / Current state / Next, not just headings. Record Delivered
only on a match. Keep one `Notes delivery` comment on the merged PR (update that
comment on retry), naming the deliverer by Agent, Role and public Session, separate
History/Latest states, a safe destination label and readback time. Keep the prepared
texts in the PR body; never publish private destination IDs or URLs.

A later session catches up only after taking delivery ownership with verified
provider access. Reading a merged PR confers neither write rights nor ownership;
no scheduler is required. With mode none, a missing delivery comment is not a
blocker and creates no write obligation.

## Confirmation gate

Unless the maintainer explicitly requests automatic synchronization for a content
type, wait for review or merge before creating or materially changing a summary
article. A merge confirms its status-page update. Onboarding summaries, milestones,
decisions, releases and reusable guides can merit an article; ordinary tasks do not.
Update existing summaries rather than duplicating them. No bidirectional sync: a
decision made in notes must be recorded in its GitHub source before implementation.

Never sync unapproved proposals, raw chat, debugging logs, speculation, duplicated
code detail, secrets or sensitive operational data. No provider is a second task tracker.
