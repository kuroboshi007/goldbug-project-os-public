---
name: Task
about: Define a bounded implementation task
title: "TASK-<issue-number>: "
labels: ""
assignees: ""
---

<!-- After creation, replace <issue-number> with this GitHub issue's number. It is the task id. -->

## Outcome

<One concrete result.>

## Context

<Why this is needed; link relevant state or decisions.>

## Scope

- <Included work>

## Non-goals

- <Excluded work>

## Constraints

- <Safety, compatibility, or product constraint>
- Must not change: <Files, areas, and dependencies that stay untouched; part of the acceptance criteria.>

## Acceptance criteria

Each criterion names the expected result and evidence another reviewer can inspect — a command with its exit status and relevant output excerpt, a diff or file reference, a screenshot path with the condition it shows, or a query result. An unsupported self-assessment is not evidence. Include only the necessary excerpt; never print secrets or private data.

- [ ] <Expected result — inspectable evidence>
- [ ] Validation: <named check> exits 0 — result and excerpt attached.
- [ ] The draft PR opens with a closure block containing `Closes #<this issue>`.

## Stop-loss

- The same blocker fails twice → stop; report both attempts, why each failed, and the current hypothesis; ask the maintainer. Attempts are repair attempts — reproduction, deliberately failing tests, and diagnostic reads do not count, and renaming the blocker does not reset the count. Origin: <maintainer>'s global agent instructions.
- A dependency, schema change, or destructive operation outside the expressly approved scope, or a project red line (`AGENTS.md` Load-bearing project rules) → stop and request approval; do not work around. An operation the task expressly approves is in scope; general approval never waives a separately required confirmation (deleting anything the agent did not create) and never authorizes unrelated deletion.
- Hard cap: stop after <N> turns where the agent can observe turns (suggested 20); otherwise stop by <HH:MM> <timezone> written in the task. At the cap, preserve state and report the gap; a runtime resume never renews the cap.

## Open decisions

- None
