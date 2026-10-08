# Operating Model

Chat is not durable shared memory. Project OS replaces it with a small protocol: repository instructions, explicit state, bounded issues, PR review, and a controlled learning loop.

It is not an application, live agent chat, GitHub replacement, or reason to document every thought.

## Control layers

- **GitHub:** rules, project state, decisions, tasks, diffs, reviews, and history.
- **Configured notes:** confirmed summaries and a per-change history useful to the maintainer; never active implementation state; [mode](notes.md) defaults to none.
- **Chat:** exploration whose durable outcomes move into GitHub.

## Decision ownership

Agents may make reversible implementation choices inside an approved task. The maintainer decides changes to product direction, meaningful scope or cost, data compatibility, privacy, security, monetization, public claims, destructive operations, and OS policy.

When a choice needs the maintainer, present concrete alternatives and impact.

## Source of truth

Each fact has one authoritative home. Other locations link or summarize it. If copies disagree, update the non-authoritative copy.

Examples:

- current product state: product `STATUS.md`
- accepted choice: product `DECISIONS.md` or ADR
- reusable procedure: this repository
- confirmed portfolio facts: configured portfolio when enabled; summaries follow [notes](notes.md)

## Admission test

Before adding a file, status, rule, or required step, ask:

1. Does it prevent a recurring or near-certain failure?
2. Will another agent know when to use it?
3. Is it missing from existing sources?
4. Is maintenance cheaper than the coordination cost removed?

If not, do not add it. An instruction that passes today can stop passing later; retire it through the [`harvest learning`](../playbooks/harvest-learning.md#retire-an-instruction) route.
