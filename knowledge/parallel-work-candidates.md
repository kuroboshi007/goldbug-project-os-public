# Parked Parallel-Work Practices

## Recurring problem

Parallel implementation can leave unclear integration ownership, uneven review coverage, and missing continuation state. The practices below are candidates, not active policy.

## Useful practices and triggers

### Parallel mode with one integration owner

- **Practice:** Define bounded work areas and assign one agent to integrate them under the existing [parallel-agent rule](../docs/ai-collaboration.md#disagreement).
- **Promotion trigger:** Two agents implement concurrently in one repository where their work areas could touch.

### Dual Review

- **Practice:** Use two independent reviewers. With two agent families, one reviewer necessarily shares a family with the implementer; treat that review as the weaker of the two.
- **Promotion trigger:** The change touches a category under [decision ownership](../docs/operating-model.md#decision-ownership) that concerns data compatibility, privacy, security, monetization, or destructive operations.

### Optional execution-state fields

- **Practice:** Add optional state, workspace, and blocker fields to a task or handoff.
- **Promotion trigger:** A task stalls because its state was unclear across sessions.

### Parallel-work handoff details

- **Practice:** Record remaining worktrees, unintegrated branches, and blockers in a handoff.
- **Promotion trigger:** Parallel work crosses sessions or ends before every branch is integrated.

## Evidence

Evidence for these parked practices is external. Local evidence currently supports only the review stop rules and proportionate-testing guidance adopted in the playbooks; it does not yet justify promoting the practices above.

## Limits

These candidates add coordination cost, add no required step to single-agent work, and do not create a dashboard, scheduler, queue, new process layer, or tool-specific rule. Promotion to `docs/`, `playbooks/`, or `templates/` requires a separate OS issue and PR through the [harvest-learning playbook](../playbooks/harvest-learning.md#promote-a-learning).

## Source

David Ondrej, [“Agentic Engineering Setup (after 2,000+ hours)”](https://x.com/davidondrej1/status/2094424967345496191), 2026-09-01.
