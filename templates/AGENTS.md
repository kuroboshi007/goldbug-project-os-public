# Agent Instructions — <project name>

These instructions apply to every agent working in this product repository.

Shared rules live at `<upstream-url>`; the OS checkout hint is `<os-checkout-hint>`.
Bootstrap substitutes these from the active profile, or withholds a missing clone
destination. Never execute unresolved placeholders. Fetch and inspect status in the
existing OS checkout; pull if behind its origin/main before relying on policy.
Resolve the active profile in full by the shared configuration precedence: explicit
`PROJECT_OS_PROFILE` (CLI/CI only), local profile, tracked private profile, then defaults.
Profile errors withhold dependent work. State which OS commit you read and which
configuration label in the handoff: `OS revision: <commit>` and `configuration source: <label>`.

## Shared fallback rules

Use these invariants if the shared repository is temporarily unavailable:

- Always work on a branch and open a pull request; never push directly to the default branch.
- Never force push, and never rewrite pushed history unless <maintainer> asks for it.
- Agent commits end with both trailers: a qualified `Agent: <mark> (<stable product name>)` using the actual product, unconditionally, plus `Co-Authored-By: Claude <noreply@anthropic.com>` for C agents or `Co-Authored-By: OpenAI Codex <noreply@openai.com>` for X agents. Examples include `Agent: C (Claude)`, `Agent: C (Claude Code)`, `Agent: X (ChatGPT)` and `Agent: X (Codex)`; these are not a closed list or an allowlist. Role, model and session stay outside the parentheses; existing commits and signed documents are not rewritten. <maintainer>'s own commits need neither trailer. The trailers are not duplicates, and `Agent:` is authoritative if they disagree. If the active profile enforces an author email, run `git config user.email` before the first commit and set it for this repository only when it differs; never `--global`. Display names are unrestricted. The two trailers are the last paragraph of the message on consecutive lines with no blank line between them; verify with `git log -1 --format='%(trailers:key=Agent,valueonly)%(trailers:key=Co-Authored-By,valueonly)'`. Never execute a placeholder as a Git identity.
- Never commit secrets, credentials, tokens, private keys, or unnecessary personal data.
- Review must be performed by an author who did not implement any part of the change under review. Account, product name and Role do not establish independence; roles are not vendor-bound. State author, public session discriminator, reviewed head and scope.

The human authorship mark is `maintainer.mark` (default `M`); `C` and `X` are reserved. With no profile, email enforcement is off and notes mode is none.

## Authority

- <maintainer> decides <product direction, scope, destructive actions, publication, and merges>.
- This repository is authoritative for <project scope, code, status, and decisions>.
- <Add project-specific authority boundaries.>

## Required read order

1. This file.
2. [`PROJECT.md`](PROJECT.md).
3. [`STATUS.md`](STATUS.md).
4. The assigned issue or pull request.
5. [`DECISIONS.md`](DECISIONS.md) entries relevant to the change.
6. <Add area-specific references.>

## Validation commands

```text
<Commands and manual checks required before opening a pull request>
```

## Load-bearing project rules

- <Rule whose violation is a regression even if the build passes.>

## Shipping paths

| Change | Path | Who may run it |
| --- | --- | --- |
| <change type> | <release or deployment path> | <owner or approval> |

## Secrets

- Never commit secrets, credentials, tokens, or private keys.
- <List ignored secret-bearing paths and the approved external storage locations.>
