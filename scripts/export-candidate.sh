#!/usr/bin/env bash
# Copy only reviewed, tracked manifest entries into a fresh directory.
set -euo pipefail
fail() { printf 'export error: %s\n' "$1" >&2; exit 1; }
# Generic archive text travels with this tool; read it from the captured commit.
# archive-readme: # Archive
# archive-readme:
# archive-readme: Nothing in `archive/` is current. Do not cite it as a rule, source of truth, or evidence of present state.
# archive-readme:
# archive-readme: Only the maintainer may delete a file from `archive/`. For the archiving procedure, see [Harvest or Retire a Reusable Learning](../playbooks/harvest-learning.md#archive-a-record).
[[ $# -le 1 ]] || fail 'usage: export-candidate.sh [new-directory]'
root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
revision=$(git -C "$root" rev-parse --verify HEAD)
manifest="$root/export/manifest.txt"
[[ -f "$manifest" && ! -L "$manifest" ]] || fail 'missing or unsafe manifest'
entries=()
sources=()
while IFS= read -r entry || [[ -n "$entry" ]]; do
  [[ -z "$entry" || "$entry" == \#* ]] && continue
  [[ "$entry" =~ ^[A-Za-z0-9._/-]+$ && "$entry" != /* && "$entry" != ./* && "$entry" != *..* && "$entry" != *//* && "$entry" != */./* ]] || fail 'invalid manifest entry'
  case "$entry" in
    .git|.git/*|private|private/*|archive/proposals|archive/proposals/*|.config/project-os.local.json|.env|.env.*) fail 'excluded manifest entry' ;;
  esac
  for previous in "${entries[@]+${entries[@]}}"; do
    [[ "$entry" != "$previous" ]] || fail 'duplicate manifest entry'
  done
  source_entry="$entry"
  [[ "$entry" != PROJECTS.md ]] || source_entry=export/PROJECTS.example.md
  [[ "$entry" != archive/README.md ]] || source_entry=scripts/export-candidate.sh
  cursor="$root"
  IFS=/ read -r -a components <<< "$source_entry"
  for component in "${components[@]}"; do
    cursor="$cursor/$component"
    [[ ! -L "$cursor" ]] || fail 'symlink source withheld'
  done
  [[ -f "$cursor" && -r "$cursor" ]] || fail 'missing manifest source'
  git -C "$root" ls-files --error-unmatch -- "$source_entry" >/dev/null 2>&1 || fail 'untracked manifest source'
  entries+=("$entry")
  sources+=("$source_entry")
done < "$manifest"
[[ ${#entries[@]} -gt 0 ]] || fail 'empty manifest'
git -C "$root" diff --quiet -- export/manifest.txt "${sources[@]}" &&
  git -C "$root" diff --cached --quiet "$revision" -- export/manifest.txt "${sources[@]}" ||
  fail 'uncommitted manifest or export source'
archive_readme=""
for entry in "${entries[@]}"; do
  if [[ "$entry" == archive/README.md ]]; then
    archive_readme=$(git -C "$root" show "$revision:scripts/export-candidate.sh" |
      awk '/^# archive-readme:( |$)/ { sub(/^# archive-readme: ?/, ""); print }')
    [[ -n "$archive_readme" ]] || fail 'missing embedded archive template'
    break
  fi
done
if [[ $# == 1 ]]; then
  destination=$1
  [[ ! -e "$destination" && ! -L "$destination" ]] || fail 'destination already exists'
  mkdir -- "$destination"
else
  destination=$(mktemp -d "${TMPDIR:-/tmp}/project-os-export.XXXXXX")
fi
for ((index=0; index<${#entries[@]}; index++)); do
  mkdir -p -- "$destination/$(dirname "${entries[$index]}")"
  if [[ "${entries[$index]}" == archive/README.md ]]; then
    printf '%s\n' "$archive_readme" > "$destination/${entries[$index]}"
    mode=100644
  else
    git -C "$root" show "$revision:${sources[$index]}" > "$destination/${entries[$index]}"
    mode=$(git -C "$root" ls-tree "$revision" -- "${sources[$index]}")
  fi
  if [[ "$mode" == 100755* ]]; then
    chmod -- 755 "$destination/${entries[$index]}"
  else
    chmod -- 644 "$destination/${entries[$index]}"
  fi
done
printf '%s\n' "$destination"
