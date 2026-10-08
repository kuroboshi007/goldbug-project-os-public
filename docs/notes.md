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
  both artifacts in `language.summaries`; deliver them to the existing designated
  status page under [Delivery and catch-up](#delivery-and-catch-up).
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

For notion and markdown, Latest also retains its represented qualified PR key
(`owner/repo#<PR>`) and that PR's exact confirmed GitHub `merged_at` UTC timestamp
alongside the text. These are destination-content metadata, not profile fields or
Notion database properties. Translate labels into `language.summaries`, retaining
the qualified key and timestamp values unchanged.

Before merge, the implementer puts both exact prepared texts and their separate
delivery states in the PR. Add the Latest PR key once GitHub assigns its number;
keep its merge timestamp `Pending — unconfirmed`. After a confirmed merge, verify
the PR key and actual `merged_at` in GitHub and finalize the prepared artifact in
the PR before permitted delivery. A draft does not claim merge or delivery.
Mode none records both as `Not applicable`, needs neither text nor a destination,
requires no Latest provenance, and never falls back to another provider.

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

Read Latest's represented PR key, merge timestamp and complete text. Verify both
represented and incoming PR metadata against GitHub's confirmed merges before
comparing timestamp instants; PR numbers do not determine order.

| Existing Latest | Action |
| --- | --- |
| No Latest exists | Deliver the finalized artifact under existing destination authorization. |
| Same PR; full text and metadata match | Skip the write and verify complete readback. |
| Same PR; content or metadata differs | Preserve it; explicit named repair or Blocked is required. |
| Different PR; incoming merge strictly later | Replace Latest under the existing permission and readback contract. |
| Different PR; incoming merge earlier or equal | Retain Latest, record its PR key/time and `Not applicable — current Latest retained; incoming merge is not later`. |

An existing Latest with missing, malformed or conflicting provenance is preserved
and `Blocked: <missing Latest PR key>`, `Blocked: <missing merge timestamp>` or
`Blocked: <conflicting Latest provenance>`, as applicable. Do not infer its PR from
the newest History entry, PR numbers, prose dates or current repository head.
Keep any independently successful authorized History delivery; an unknown Latest
does not authorize changing it or other History entries.

If existing content or its exact prior delivery record unambiguously identifies
the represented PR, verify that PR's confirmed GitHub `merged_at` and prepare a
named metadata-only repair. Execute it only with explicit authorization for that
repair, retaining Latest text and other History; verify complete readback before
reconsidering replacement. Without proven identity or authorization, retain the
specific Blocked state. No automatic backfill or migration overwrite is permitted.

After writing or skipping matching content, read back the full History line and
the represented PR key, merge timestamp and all Merged / Current state / Next text,
not just headings. Record Delivered only on a full match. Keep one `Notes delivery`
comment on the merged PR (update that
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
