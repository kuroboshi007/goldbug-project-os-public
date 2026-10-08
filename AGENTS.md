# Agent Instructions

This repository is read from local clones that drift. Before relying on anything below, run `git fetch && git status -sb` here and pull if the checkout is behind `origin/main`. State `OS revision: <commit>` and `configuration source: <label>` in your handoff; see [configuration](docs/configuration.md).

These instructions apply to every agent working in `goldbug-project-os`.

## Purpose and authority

Maintain a small, practical operating system for the maintainer's AI-assisted projects. Optimize for continuity, traceability, and low coordination cost.

- The maintainer decides product direction, meaningful scope changes, destructive actions, publication, and merges.
- GitHub is authoritative for operational content.
- A configured notes provider holds human-facing summaries of confirmed information; [notes mode](docs/notes.md) defaults to `none`.
- Durable decisions must leave chat and enter the relevant repository.

## Required read order

Before changing this repository:

1. Read `AGENTS.md`.
2. Resolve the active profile by the [configuration precedence](docs/configuration.md); state its label in the handoff. Withhold dependent actions on errors.
3. Read `README.md`.
4. Read [`docs/operating-model.md`](docs/operating-model.md).
5. Read the relevant playbook.
6. Read the assigned issue, task, or PR.

In an onboarded product repository, read `AGENTS.md`, `PROJECT.md`, `STATUS.md`, the assigned issue or task, then relevant decisions.

Fast path: typo, formatting, and broken-link fixes that change no behavior or policy may skip steps 3–5. They still use a branch and PR. `archive/` is historical and excluded from required reading.

## Working rules

`AGENTS.md` contains only rules that apply to every agent on every task. Role protocols, procedures, and artifact formats live in [`docs/`](docs/), [`playbooks/`](playbooks/), and [`templates/`](templates/).

Some of the rules below are also carried in [`templates/AGENTS.md`](templates/AGENTS.md), as the compact fallback set a product repository relies on when it cannot reach this repository. That subset is deliberately small. When a rule that appears in the fallback set changes, update the template copy in the same PR.

- Make the smallest coherent change that satisfies the task; do not silently expand scope.
- Preserve unrelated work and existing project structure.
- Never commit secrets, credentials, tokens, private keys, or unnecessary personal data.
- Use a branch and PR; never push directly to the default branch.
- Never force push, and never rewrite pushed history unless the maintainer asks for it.
- Commit messages state what that commit changed; a series does not repeat one subject line.
- Validate the changed behavior and report checks not run.
- Record uncertainty as an assumption, not a decision.
- Ask the maintainer only when a missing choice materially changes behavior, risk, cost, scope, or public output.
- Shared rules belong here; project facts belong in the product repository.
- Link to one authoritative document instead of duplicating it.
- Operational documents and summaries use the active profile’s language settings; both default to concise English.

## Identifiers

- The number GitHub assigns is the task id; issues and pull requests share one sequence.
- Create the issue first, then the branch `agent/<issue-number>-<short-slug>`; never predict a number and never rename existing issues or branches to fit this rule.
- Titles are descriptive, with no prefix.
- An issue the maintainer opened, or that the planner opened from the maintainer's confirmed request, is accepted work. An issue or pull request opened by anyone else is a request until the maintainer accepts it.
- Refer to another repository's issue or pull request as `owner/repo#<n>`.
- Decisions: `D-<YYYYMMDD>-<nn>`.
- ADRs: `ADR-<nnn>`, sequential per repository.

## Collaboration and records

One agent may plan and implement. Review must be performed by an agent that did not write the change. Follow [`docs/ai-collaboration.md`](docs/ai-collaboration.md) and [`playbooks/review-change.md`](playbooks/review-change.md).

Follow [`templates/DECISIONS.md`](templates/DECISIONS.md) for decision records and ADR use.

Use [`templates/HANDOFF.md`](templates/HANDOFF.md) when a durable handoff is useful. Follow [`docs/notes.md`](docs/notes.md) for the selected notes mode, confirmation gate, and delivery state.

## Authorship marks

Marks are `C` for Claude, Claude Code, or Cowork; `X` for ChatGPT, ChatGPT Work, or Codex; and the active profile’s `maintainer.mark` (default `M`) for the human maintainer; `C` and `X` remain reserved for the vendor families.

Qualify the `Agent:` trailer with the stable product name on every agent commit: `Agent: C (Cowork)`, `Agent: C (Claude Code)`, `Agent: X (ChatGPT)`, or `Agent: X (Codex)`. This is unconditional, because at commit time an agent cannot know whether another agent sharing its mark will join the task later, and commits are not rewritten to add it.

In review findings use the same notation as a prefix (`C (Cowork): ...`). A bare mark is acceptable there when only one agent of that mark is involved, because a finding is written knowing who else is on the pull request.

Agent commits end with both trailers: one qualified `Agent:` value from the rule above, plus `Co-Authored-By: Claude <noreply@anthropic.com>` for C agents or `Co-Authored-By: OpenAI Codex <noreply@openai.com>` for X agents. Use stable product names, not model versions; the maintainer's own commits need neither trailer. The trailers are not duplicates, and `Agent:` is authoritative if they disagree. If the active profile enforces an author email, run `git config user.email` before the first commit and set it for this repository only when it differs; never `--global`. Display names are unrestricted. The two trailers are the last paragraph of the message on consecutive lines with no blank line between them; verify with `git log -1 --format='%(trailers:key=Agent,valueonly)%(trailers:key=Co-Authored-By,valueonly)'`. Never execute a placeholder as a Git identity.
Documents are collectively owned unless they contain an `Author:` field. Another mark may not rewrite or delete a signed document; its only permitted in-file change is a separately signed response section. It may instead respond on the PR or issue. Only the maintainer may delete or supersede a signed document.
Shared policy files may not be signed: `AGENTS.md`, `README.md`, `PROJECTS.md`, and policy documents in `docs/`, `playbooks/`, and `templates/`.

## Learning loop

The learning loop runs in both directions. Use [`playbooks/harvest-learning.md`](playbooks/harvest-learning.md) in a separate OS PR to promote recurring lessons or retire obsolete scaffolding; keep project-specific lessons in the product repository.
