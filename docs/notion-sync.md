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

Update one designated status page in place after each confirmed merge: what merged,
current state and next. The merge confirms this update; do not create an article
for each merge. The repository's STATUS.md owns operational state unless an accepted
decision assigns product-status authority differently. Keep the operational state
and its human-facing summary distinct.

## Articles

Prepare confirmed onboarding summaries, milestones, decisions, releases and reusable
guides. Reuse an existing article when it covers the same subject. No routine task
or draft proposal is an article by default.

## Access and handoff

Prepare the exact update in `language.summaries`, even without connector access.
An authorized agent or the maintainer can relay it. Keep `Prepared — delivery
outstanding` until the actual write is verified; access failure is `Blocked: <reason>`
with the artifact preserved. Follow the [confirmation gate](notes.md#confirmation-gate).

## Drift control

Use the field names supplied by `notes.notion.schema_fields`: `repo` for the source
repository, `source` for its file/issue/PR/release, `updated` for the synchronization
date, and `project`, `type`, `status` for filtering. Portfolio fields are `status`,
`type`, `perspective`, `start_date`. Onboarding articles set the configured status
field to Confirmed and populate the configured type/project/repo/source fields.
When the source changes materially, update its existing summary. Link operational
detail to GitHub instead of copying it into a second source of truth.
