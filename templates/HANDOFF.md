# Handoff: <task or milestone>

- Date: YYYY-MM-DD
- From: <mark> (<stable product name>) · Role: <role> · Session: YYYY-MM-DD r<n>
- To: <agent or maintainer>; for an agent, use the same Agent · Role · Session fields
- Issue/PR:

OS revision: <commit>
configuration source: <label>

## Outcome

<What is now true.>

## Changed

- <Files, components, or behavior>

## Validation

| Criterion | PASS · FAIL · NOT RUN | Evidence |
| --- | --- | --- |
| <Expected result, including Must not change constraints> | <Result> | <Command, exit status, excerpt, or other inspectable evidence; reason and gap for NOT RUN> |

## Notes status update

<Apply the configured notes mode. None records both artifacts Not applicable and
needs no prepared text. Otherwise prepare both exact texts in language.summaries;
translate Merged / Current state / Next. Drafts do not claim merge or delivery.
For notion/markdown, retain the qualified represented PR key and confirmed GitHub
merged_at alongside Latest. Keep the timestamp pending before merge; finalize it
after confirmation, before permitted delivery, in the PR body or an authorized PR
comment by the assigned deliverer. A comment links to retained prepared text and
supersedes pending provenance only; preserve prepared summary content in the body.
Link the finalization record from the single delivery-result comment.
Read back both values and all text.
With none, omit prepared-text/provenance fields. Preserve unknown/conflicting
existing Latest; its metadata repair needs explicit named authorization.
Follow docs/notes.md for ownership, matching-key skips, explicit repairs,
merge-time ordering, full-content readback and the merged PR delivery comment.>

- Prepared History: <YYYY-MM-DD · owner/repo#<PR> · one-line outcome [· decision id]>
- Prepared Latest: <Merged / Current state / Next, pending confirmed merge>
- Prepared Latest PR key: <owner/repo#<assigned-PR-number>; omit for none>
- Prepared Latest merge timestamp: <Pending — unconfirmed; exact confirmed GitHub merged_at UTC after merge; omit for none>
- History state: Not applicable | Prepared — delivery outstanding | Blocked: <reason> | Delivered
- Latest state: Not applicable | Prepared — delivery outstanding | Blocked: <reason> | Delivered
- Overall state / remaining delivery: <least complete applicable state and gap>
- Destination: <safe label; no private IDs or URLs>
- Assigned deliverer: <mark> (<stable product name>) · Role: <role> · Session: YYYY-MM-DD r<n>
- Provenance finalization record: <public PR-body or authorized comment link; omit for none>
- Readback time / delivery comment: <verified time and public PR comment link, when applicable>

## Assumptions and unresolved items

- None

## Next action

1. <One concrete step>

## Findings

- None

Outcome: Done | Blocked: <reason> | Stopped by stop-loss: <line>
Reusable lesson: <one line — target playbook or knowledge file> | None
