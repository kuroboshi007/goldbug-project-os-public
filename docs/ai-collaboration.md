# AI Collaboration Protocol

Agents communicate through repository artifacts, not assumed shared chat context.

| Need | Artifact |
| --- | --- |
| Persistent constraints | `AGENTS.md` |
| Product definition and state | `PROJECT.md`, `STATUS.md` |
| Accepted choices | `DECISIONS.md` or ADR |
| Bounded work | GitHub issue or task file |
| Implementation and review | Branch and PR |
| Continuation context | Handoff |
| Reusable lesson | `knowledge/` PR |

## Agents without GitHub access

Some agents cannot read a private repository's issues or pull requests. The maintainer relays the task content to them and pastes their output back as a GitHub issue or pull request comment, which is where the record lives. Do not mirror an issue into a file in the repository.

An agent working this way states in its handoff that it worked from a relay rather than from the issue itself, and re-reads the relayed content after any reported update. The GitHub issue remains authoritative if the two disagree.

## Roles

Role assignment follows the [`AGENTS.md` collaboration rule](../AGENTS.md#collaboration-and-records).

### Planner

Define one outcome, constraints, acceptance criteria, non-goals, and any decisions required before work starts.

### Implementer

Follow the task and repository rules, validate the result, and explain deviations in the PR.

### Reviewer

Read the task before the diff and follow [`playbooks/review-change.md`](../playbooks/review-change.md). Review against accepted intent, not personal preference.

## Handoffs

The PR is the normal implementer-to-reviewer handoff. Use [`templates/HANDOFF.md`](../templates/HANDOFF.md) only when work must continue outside that PR or across sessions.

## Disagreement

Use acceptance criteria, accepted decisions, tests, and diffs as evidence. Prefer the smaller reversible option when both satisfy the task. Ask the maintainer when the choice changes behavior, risk, or long-term direction.

Parallel agents use separate branches or worktrees and rerun relevant validation after integrating changes.
