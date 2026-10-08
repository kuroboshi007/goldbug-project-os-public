# Notion provider guide

Apply this guide only when the resolved profile selects `notes.mode = notion`.
The common [notes policy](notes.md) owns modes, delivery states, the confirmation
gate and the operational/portfolio distinction. Credentials stay in authorized
connectors; no profile contains tokens or access credentials.

## Destinations

Read `notes.notion.home_page`, `notes.notion.status_page`,
`notes.notion.portfolio_database` (`id`, `name`) and
`notes.notion.articles_database` (`id`, `name`) from the active profile.
The OS uses the designated status page. Products use their portfolio entry page when portfolio integration is enabled,
otherwise their designated status page from the profile. The maintainer may
designate another single status page. Articles use a
product's own article database when available, otherwise the configured shared one.
Portfolio database and perspective/start-date fields are needed only when
`registry.portfolio_exists` is true. Missing required destinations withhold the
dependent action; never guess a page or database.

## Registries

The file at `registry.path` (the pilot's [operational registry](../PROJECTS.md)) owns
approved onboarding, onboarding state and repository URLs. When
`registry.portfolio_exists` is true, the configured portfolio owns facts named by
`schema_fields.status`, `type`, `perspective`, and `start_date` below. Registration
still requires the maintainer's confirmation; being in a portfolio is not onboarding.

## Status pages

Use Latest and History sections on the existing designated status page. For each
meaningful confirmed merge, retain the keyed History line and update Latest's
Merged / Current state / Next under the [delivery rules](notes.md#delivery-and-catch-up).
Latest also stores its qualified represented PR key and exact confirmed GitHub
`merged_at` UTC timestamp alongside the text. These are section content, not new
profile fields or Notion database properties. Before merge the timestamp is pending;
finalize it after confirmation and before permitted delivery. Missing or conflicting
existing provenance follows the common preserve/Block/named-repair contract.
No new article per merge is needed. Product STATUS.md owns
operational state unless an accepted decision assigns that authority differently.
The OS uses its PR records and designated page, without a root STATUS.md. Keep
operational state distinct from these human-facing summaries.

## Articles

Prepare confirmed onboarding summaries, milestones, decisions, releases and reusable
guides. Reuse an existing article when it covers the same subject. No routine task
or draft proposal is an article by default.

## Access and handoff

Prepare both exact texts in `language.summaries`, even without connector access.
Before delivery, verify the configured destination, assigned owner and existing
tool/destination authorization. An authorized reviewer or relay may take over from
the implementer; the maintainer is not the default messenger. The writer verifies
full-content readback including Latest's PR key and merge timestamp, preserves
partial success and records separate History and
Latest states in one PR delivery comment. Missing access is `Blocked: <reason>`
with prepared text retained, never a provider fallback. Apply matching-key skips,
explicit mismatch repairs and merge-time ordering from the
[delivery rules](notes.md#delivery-and-catch-up), then the
[confirmation gate](notes.md#confirmation-gate).

## Drift control

Use the field names supplied by `notes.notion.schema_fields`: `repo` for the source
repository, `source` for its file/issue/PR/release, `updated` for the synchronization
date, and `project`, `type`, `status` for filtering. Portfolio fields are `status`,
`type`, `perspective`, `start_date`. Onboarding articles set the configured status
field to Confirmed and populate the configured type/project/repo/source fields.
When the source changes materially, update its existing summary. Link operational
detail to GitHub instead of copying it into a second source of truth.
