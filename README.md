# goldBug Project OS

`goldBug Project OS` is a small, versioned set of rules, playbooks, and templates for projects built by k.goldbug.studio with AI collaborators. It is not an application or a second project-management system.

Display attribution is optional: downstream users may freely change or omit the
README credit. Customize human-facing labels with `maintainer.name` and optional
`maintainer.handle`; see [display attribution](docs/configuration.md#display-attribution).

## Source of truth

| Information | Authoritative home |
| --- | --- |
| Shared rules and reusable templates | This repository |
| Project scope, status, decisions, tasks, and code | Each product repository |
| Portfolio status, type, perspective, and start date | Configured portfolio, when enabled |
| Confirmed human-facing summaries | Configured notes provider, when enabled |
| Temporary exploration | Chat |

GitHub is authoritative for operational work. Notes must not become a competing copy of work in progress.

## Start here

Follow the single canonical [`AGENTS.md` read order](AGENTS.md#required-read-order).

## Workflow

1. The maintainer approves an outcome.
2. An agent creates a bounded GitHub issue.
3. An agent implements on a branch and opens a draft PR.
4. A different agent reviews the task, diff, and evidence.
5. The maintainer resolves meaningful choices and merges.
6. Apply the configured [notes mode](docs/notes.md) after a confirmed merge; default `none` adds no summary or delivery obligation.
7. Reusable lessons return through a separate OS PR.

See [`project lifecycle`](docs/project-lifecycle.md), [`AI collaboration`](docs/ai-collaboration.md), and [`notes`](docs/notes.md).

## Repository map

```text
AGENTS.md       shared agent instructions
PROJECTS.md     project registry
docs/           stable operating policy
playbooks/      repeatable procedures
templates/      files copied into product repositories
knowledge/      reusable lessons not yet promoted to policy
archive/        signed historical records; never current policy
.github/        issue/PR templates and automated checks
```

The minimum project kit is `AGENTS.md`, `PROJECT.md`, `STATUS.md`, and `DECISIONS.md`. Add task, handoff, or ADR files only when they remove real coordination cost.

## Configuration and current stage

This repository maintains reusable policy and a private pilot profile. Resolve the
[configuration contract](docs/configuration.md) before acting; without a profile, the
documented defaults apply. The operational registry is private and excluded from reusable
exports. A public release requires a separately reviewed sanitized snapshot and
the maintainer's approval.
