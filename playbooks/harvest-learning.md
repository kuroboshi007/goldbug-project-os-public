# Playbook: Harvest or Retire a Reusable Learning

The learning loop runs in both directions: promote evidence-backed lessons and retire scaffolding that no longer earns its context cost.

## Promote a learning

Promote a lesson only when it recurs across projects, prevents meaningful failure or coordination cost, and gives another agent a concrete action. Otherwise keep it in the product repository.

### Destination

- observation or example: `knowledge/`
- repeatable sequence: `playbooks/`
- permanent cross-project policy: `AGENTS.md` or `docs/`
- reusable starting artifact: `templates/`

### Proposal

Use a separate OS PR. Describe the source experience, recurring problem, smallest proposed change, beneficiaries, and maintenance cost.

The maintainer or an independent reviewer confirms that the change is reusable, simple, and compatible with existing workflows.

## Retire an instruction

Retirement candidates compensate for a limitation that is no longer present: an unnecessary step-by-step procedure, an example that no longer teaches, a workaround for changed tool or model behavior, or a skill or template whose capability is now built in.

Never retire authority or risk controls because a model appears more capable. Approval ownership, secrets and destructive-operation safeguards, publication gates, branch and PR requirements, the Notion confirmation gate, and source-of-truth assignments are not candidates.

The confirmation-gate exclusion applies to the [notes confirmation gate](../docs/notes.md#confirmation-gate), when a provider is configured; the excluded controls listed above are preserved.

### Proposal and evidence

**Model-change review.** When a collaborating model family changes major version, or its vendor publishes migration or prompting guidance for a model in use, open one OS improvement issue that walks the instruction set against that guidance. List candidates with traceability: source → exact instruction and location → disposition (`keep`, `rewrite`, `retire`, `defer pending evidence`) → reason → regression symptom for any change. An empty list is a valid result. Each change follows the existing retirement route; the controls excluded above never enter the candidate list.

Use a separate OS PR. Quote the exact instruction and record:

- the limitation it compensated for
- observable evidence that the limitation changed
- the symptom that would reveal a regression

An agent's self-assessment is not evidence. Use a new tool, behavior visible in a diff, a documented platform or model change, or a record showing that the instruction is now followed redundantly.

A vendor's published migration or prompting guidance for a model in use is a documented platform or model change: record the model and version, URL and section, and access date; learning notes summarizing it are intake, not evidence, so link the vendor source.

Retire an instruction shared by more than one model family only when guidance from every family in use supports it, or a walkthrough on the other family shows the adjusted instruction still delivers the required result and respects constraints — not merely that fewer checks ran.

An unconfirmed learning note lives in the configured notes provider's guide entry, or in `knowledge/` when none is configured; adoption is recorded in GitHub and linked from the note.

### Review and approval

The proposing agent may not review its own retirement proposal. A different mark must state the strongest case for keeping the instruction before agreeing to remove it. The maintainer approves the policy change.

Move the retired instruction or its signed proposal to `archive/` so the change remains traceable and reversible. Restore it through another reviewed OS PR if the regression symptom appears.

## Archive a record

Exception: `archive/status-log.md` is the single unsigned, growing file permitted under `archive/`; new closed entries are added at the top, existing entries are never edited, and the file as a whole is not a closed signed record. It contains only the header line specified in [`templates/STATUS.md`](../templates/STATUS.md) and one line per entry. Ordinary archived proposals, reviews, and handoffs remain closed and unchanged under the rules below.

An archived record is closed. Do not edit it after the archiving commit, including to append a signed response. Continue the discussion on the PR or issue, or in a new signed document that references the archived one.

Do not archive a record while any item remains open, including an optional item. Resolve it or explicitly drop it in the same PR that archives the record.

Archive only signed historical records such as proposals, reviews, and handoffs. Do not archive superseded policy; Git already preserves it, and a stale policy copy is hazardous.

Archive a record in the same PR that completes, replaces, rejects, or abandons it. Preserve its filename, use the normal branch and PR flow, and identify a document signed by another mark in the PR description so its author can object during review.

Add this two-line header:

```text
> Archived YYYY-MM-DD. Superseded by PR #N.
> Reason: <category> — <one-sentence explanation>
```

Start the reason with one of these categories:

- `Implemented` — the described work is done
- `Superseded by <what>` — a named document, PR, or issue replaced it
- `Rejected by the maintainer`
- `Obsolete` — the limitation no longer exists; follow the [instruction-retirement route](#retire-an-instruction)
- `Abandoned` — work stopped without a replacement

