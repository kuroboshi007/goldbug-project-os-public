#!/usr/bin/env bash
set -euo pipefail
if [[ $# != 2 ]]; then echo 'usage: check-commits.sh <base> <head>' >&2; exit 2; fi
base=$1
head=$2
git rev-parse --verify "$base^{commit}" >/dev/null 2>&1 || { echo 'error: invalid base revision' >&2; exit 2; }
git rev-parse --verify "$head^{commit}" >/dev/null 2>&1 || { echo 'error: invalid head revision' >&2; exit 2; }
source "$(dirname "${BASH_SOURCE[0]}")/project-os-config.sh"
trap os_config_cleanup EXIT
os_config_resolve "$base"
enforce=false
expected=""
if [[ -n "$OS_CONFIG_FILE" ]]; then
  enforce=$(jq -r '.commit_email.enforce // false' "$OS_CONFIG_FILE")
  if [[ "$enforce" == true ]]; then expected=$(jq -r '.commit_email.address' "$OS_CONFIG_FILE"); fi
fi
status=0
count=0
commits=$(git rev-list --no-merges "$base..$head")
for commit in $commits; do
  count=$((count + 1))
  if [[ "$enforce" == true && "$(git log -1 --format='%ae' "$commit")" != "$expected" ]]; then
    echo "error: $commit author email violates configured policy" >&2
    status=1
  fi
  agent=$(git log -1 --format='%(trailers:key=Agent,valueonly)' "$commit")
  coauthor=$(git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)' "$commit")
  if [[ -n "$agent" && -z "$coauthor" || -z "$agent" && -n "$coauthor" ]]; then
    echo "error: $commit Agent and Co-Authored-By trailers must both be present or both absent" >&2
    status=1
  fi
done
if [[ "$status" == 0 ]]; then echo "checked $count commits; PASS"; else echo "checked $count commits; FAIL"; fi
exit "$status"
