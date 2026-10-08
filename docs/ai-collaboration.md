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

Some agents cannot read a repository's issues or pull requests. An authorized agent with the required access relays task content and publishes the signed review on the PR with verified readback. The maintainer relays only by explicit choice, not as the default messenger. Follow the [review delivery contract](../AGENTS.md#collaboration-and-records), preserving authorship, verdict, reviewed head/scope and provenance and marking necessary redactions. Do not mirror an issue into a file in the repository.

An agent working this way states in its handoff that it worked from a relay rather than from the issue itself, and re-reads the relayed content after any reported update. The GitHub issue remains authoritative if the two disagree.

## Roles

Role assignment follows the [`AGENTS.md` collaboration rule](../AGENTS.md#collaboration-and-records).

### Planner

Define one outcome, constraints, acceptance criteria, non-goals, and any decisions required before work starts.

### Implementer

Follow the task and repository rules, validate the result, and explain deviations in the PR.

### Reviewer

Read the task before the diff and follow [`playbooks/review-change.md`](../playbooks/review-change.md). Review against accepted intent, not personal preference.

State author, Role, public Session discriminator, reviewed head/scope and implementation participation. Independence is based on no implementation participation, not a different account, product or Role; two sessions of the same product can be independent. Publish and verify delivery under the [review contract](../AGENTS.md#collaboration-and-records).

## Handoffs

The PR is the normal implementer-to-reviewer handoff. Use [`templates/HANDOFF.md`](../templates/HANDOFF.md) only when work must continue outside that PR or across sessions.

## Disagreement

Use acceptance criteria, accepted decisions, tests, and diffs as evidence. Prefer the smaller reversible option when both satisfy the task. Ask the maintainer when the choice changes behavior, risk, or long-term direction.

Parallel agents use separate branches or worktrees and rerun relevant validation after integrating changes.
