# Playbook: Execute a Task

## 1. Orient

Follow the repository read order. Inspect the worktree, relevant implementation, validation commands, and unrelated changes to preserve.

## 2. Confirm readiness

Start when the issue has a concrete outcome, observable acceptance criteria with inspectable evidence, and a stop-loss. For an existing issue lacking the criteria or stop-loss, supply them in a short startup comment without rewriting its body. Pause only for a choice that materially changes behavior, risk, cost, compatibility, or scope.

## 3. Work

- Follow the [`AGENTS.md` identifiers](../AGENTS.md#identifiers).
- Change only required areas.
- Follow existing architecture and style.
- Test behavior changes. Add or update tests only where they protect the changed behavior or a realistic regression; do not build broad test scaffolding to satisfy a generic request for tests.
- Keep factual documentation current.

## 4. Validate

Run the narrowest relevant checks first and complete all required project and CI validation. Broaden or repeat checks when shared or cross-module impact (code, rules, templates, configuration), an observed failure, later changes that invalidate earlier evidence, or a concrete unresolved risk requires it; otherwise stop once the agreed outcome is demonstrated.

Record each acceptance criterion as `PASS` (evidence supports it), `FAIL` (a performed check contradicts it), or `NOT RUN` (not verified; state the reason and gap). Attach commands with exit statuses and relevant output excerpts, diff or file references, screenshot paths with the conditions shown, or query results; record manual verification and omitted checks. Include only necessary evidence; never print secrets or private data.

Do not call work complete while core validation fails.

## 5. Handoff

Review the diff, commit, push, and open a draft PR. Complete the PR template. The PR description opens with a closure block, one `Closes #<issue-number>` line per issue actually completed; a stopped or partial task is not eligible for closure. Use [`templates/HANDOFF.md`](../templates/HANDOFF.md) only when a separate durable handoff is needed.

State `OS revision: <commit>` and `configuration source: <label>` from [configuration](../docs/configuration.md) in the handoff.

A stop is a complete report, not a failure: it does not require opening a PR, and the PR/linkage criterion is then `NOT RUN`. Report acceptance criteria, per-criterion results with evidence, and findings, then end the handoff with:

```text
Outcome: Done | Blocked: <reason> | Stopped by stop-loss: <line>
Reusable lesson: <one line — target playbook or knowledge file> | None
```

`Done` is the implementer's claim, not approval, merge, or publication.
