# Project Lifecycle

## 1. Register

Add a maintainer-approved project and repository to `PROJECTS.md`.

## 2. Bootstrap

Use [`playbooks/bootstrap-project.md`](../playbooks/bootstrap-project.md) to add or map the minimum project kit.

## 3. Plan

Create a bounded GitHub issue, or use [`templates/TASK.md`](../templates/TASK.md) when a durable task file is useful. Include outcome, constraints, acceptance criteria, non-goals, and unresolved decisions.

Open an issue in the repository whose files the work will change. Product work belongs in the product repository; changes to shared rules, templates, or this repository's own records belong here. Work that spans both takes one issue in each repository.

## 4. Implement

Follow [`playbooks/execute-task.md`](../playbooks/execute-task.md), work on the issue branch, validate, and open a draft PR.

## 5. Review

Apply the [`AGENTS.md` collaboration rule](../AGENTS.md#collaboration-and-records) through [`playbooks/review-change.md`](../playbooks/review-change.md).

## 6. Decide and merge

The maintainer resolves meaningful choices and approves the merge.

## 7. Close

For every merge, close the issue, record accepted decisions according to [`templates/DECISIONS.md`](../templates/DECISIONS.md), and apply the configured [notes mode](notes.md).

In a product repository, update `STATUS.md`: add the outcome to Recent outcome,
rotate the oldest beyond three verbatim into `archive/status-log.md`, and move a
newly shipped capability to `PROJECT.md` Shipped. These are operational records;
provider History does not replace them. This OS uses the PR record and configured
status page and does not gain a root `STATUS.md`.

The implementer prepares History and Latest text and separate states in the PR
before merge. After merge, the assigned authorized deliverer performs delivery as
the final Close step, verifying existing access, full-content readback and the PR
delivery comment under [notes](notes.md#delivery-and-catch-up). Catch-up requires
the same provider, ownership and authorization checks. Mode none records both as
Not applicable without text, outstanding sync or a missing-comment blocker.

## 8. Learn

Use [`playbooks/harvest-learning.md`](../playbooks/harvest-learning.md) only for lessons that generalize beyond one repository.

## 9. Summarize

For a configured notes provider, prepare useful confirmed summaries according to
[notes](notes.md), including the first onboarding summary described in
[bootstrap](../playbooks/bootstrap-project.md#deliver-the-summary).
Mode none completes onboarding without an external account, page or summary.
