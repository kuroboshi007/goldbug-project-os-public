# Playbook: Review a Change

## Inputs

Read the issue, accepted decisions, PR description, complete diff, validation evidence, and repository instructions.

## Review

1. Map every acceptance criterion to evidence.
2. Inspect data mutation, permissions, failure paths, compatibility, state transitions, and destructive behavior.
3. Check tests and factual documentation.
4. Separate required corrections from preferences.

## Finding format

Apply the [`AGENTS.md` authorship marks](../AGENTS.md#authorship-marks) to findings.

Each finding includes:

- severity: `Blocking`, `Important`, `Suggestion`, or `Question`
- exact file and location
- concrete failure or risk
- evidence or reproduction
- smallest correction when known

Do not request refactoring without demonstrated impact.

A finding addresses the diff against the task's acceptance criteria. A proposed change to OS policy discovered during review is not a finding; open an [`OS improvement` issue](../.github/ISSUE_TEMPLATE/os-improvement.md) and reference it. It neither blocks nor extends the PR under review.
No findings is a valid review result. No number of findings is required.
After `Changes required`, re-review the new diff against the findings raised and the areas the fix touched. A new finding outside those areas needs a stated trigger.

## Outcome

Use this fixed output shape with one of the four existing verdicts:

```text
## Acceptance criteria
- <criterion> — <evidence: file, test, command>

## Findings
- None.

## Outcome
<Approve | Approve with suggestions | Changes required | Blocked by missing decision or evidence> — <residual risk, validation gaps>
```

`None.` is a valid fill under Findings.
