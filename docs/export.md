# Sanitized export candidate

Run `bash scripts/export-candidate.sh [new-directory]` from a committed source checkout or an initialized downstream checkout.
Use a clean checkout at the reviewed commit and record `git rev-parse HEAD` in the
export review. The script captures that commit, refuses staged or unstaged changes
to the manifest or any included source (including the synthetic registry and embedded archive template), and copies
bytes and executable modes from the captured commit. Unlisted local/private files
do not affect the candidate. This keeps later working-tree edits out of the export.

It creates a fresh directory and exports only committed files listed explicitly in
`export/manifest.txt`; it refuses an existing destination, missing/untracked sources,
symlinks, duplicate or unsafe paths, and excluded credential/private/history paths.
`PROJECTS.md` is a special synthetic entry sourced from `export/PROJECTS.example.md`,
never the real operational registry. `archive/README.md` is rendered from the generic
`# archive-readme:` block in the captured commit's `scripts/export-candidate.sh`,
with mode 644. It never reads or falls back to the original archive README; the
protected archive remains untouched. A missing embedded template fails before
creating a destination. Every other output retains its committed bytes and mode.

This local candidate's manifest contains exactly 45 files, including the three
language READMEs and the maintainer-approved standard MIT `LICENSE`. This expanded
inventory requires its own review; earlier 42-file hashes do not approve these
additions or changed documents. Preserve required legal notices when exporting.
The archive template travels inside the
already included exporter, so there is no omitted fixture dependency. A fresh
candidate initialized and committed as a downstream Git repository can run both
`python3 tests/test-export.py` and the exporter again. Export regressions exercise
that actual downstream re-export, with changed and omitted display attribution;
tests impose no particular credit. No Git metadata or private profile is copied.

Adding a file to Git does not admit it to the export. Review its current contents and
dependencies before explicitly adding it to the allowlist. The manifest is the one
export list; the script applies safety guards, not an inferred list of public files.
No scanner substitutes for inspecting the candidate's included content.

Check the candidate with the same offline link command as OS checks:

```bash
lychee --offline --no-progress --include-fragments --exclude-path 'archive/' './**/*.md'
```

Run it with the candidate as working directory, then inspect its filenames, text,
links, metadata and synthetic registry. Test exclusion regressions with
`python3 tests/test-export.py` in the OS checkout. The script creates only a local
candidate; it never initializes new history or publishes a repository.

Before any later public release, separately review history/issues/PRs/logs/artifacts,
choose public author identity, license and notices, verify the README and public
upstream, and obtain the maintainer's approval. Preserve private history; initialize
fresh history only in an independently approved sanitized repository. Rollback of
this migration is a revert, never deletion or rewriting existing history.
