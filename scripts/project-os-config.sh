#!/usr/bin/env bash
# Source for the resolved file and source label; execution prints the label only.
set -euo pipefail
OS_CONFIG_DIR=""
OS_CONFIG_FILE=""
OS_CONFIG_SOURCE=""
os_config_cleanup() {
  if [[ -n "$OS_CONFIG_DIR" ]]; then rm -rf -- "$OS_CONFIG_DIR"; fi
}
os_config_fail() {
  printf 'configuration source: error — %s\n' "$1" >&2
  return 1
}
os_config_temp() {
  OS_CONFIG_DIR=$(mktemp -d "${TMPDIR:-/tmp}/project-os.XXXXXX")
  OS_CONFIG_FILE="$OS_CONFIG_DIR/profile.json"
}
# Schema checking establishes the string type; installed IANA data establishes names.
os_config_timezone() {
  local timezone zone_dir zone_file
  local zone_dirs=()
  # Validate the exact JSON string before raw output can lose newline/NUL bytes.
  jq -e '(.timezone // "Etc/UTC") | test("\\A[A-Za-z0-9_+-]+(/[A-Za-z0-9_+-]+)*\\z")' \
    "$OS_CONFIG_FILE" >/dev/null 2>&1 || {
    os_config_fail 'invalid timezone'; return 1;
  }
  timezone=$(jq -r '.timezone // "Etc/UTC"' "$OS_CONFIG_FILE")
  # The documented UTC default is known without any external timezone data.
  [[ "$timezone" != Etc/UTC ]] || return 0
  case "$timezone" in
    localtime|posixrules|posix/*|right/*) os_config_fail 'invalid timezone'; return 1 ;;
  esac
  if [[ "${TZDIR+x}" == x ]]; then
    zone_dirs=("$TZDIR")
  else
    zone_dirs=(/usr/share/zoneinfo /usr/share/lib/zoneinfo /usr/lib/zoneinfo)
  fi
  for zone_dir in "${zone_dirs[@]}"; do
    [[ -d "$zone_dir" && -r "$zone_dir/Etc/UTC" ]] || continue
    [[ "$(LC_ALL=C head -c 4 2>/dev/null < "$zone_dir/Etc/UTC")" == TZif ]] || continue
    zone_file="$zone_dir/$timezone"
    if [[ -f "$zone_file" && -r "$zone_file" &&
          "$(LC_ALL=C head -c 4 2>/dev/null < "$zone_file")" == TZif ]]; then
      return 0
    fi
    os_config_fail 'invalid timezone'; return 1
  done
  os_config_fail 'timezone data unavailable'; return 1
}
os_config_resolve() {
  command -v jq >/dev/null 2>&1 || { os_config_fail 'jq unavailable'; return 1; }
  local base="${1:-}" kind profile
  if [[ "${PROJECT_OS_CI:-0}" == 1 ]]; then
    if [[ -n "${PROJECT_OS_COMMIT_EMAIL:-}" ]]; then
      if [[ -z "${PROJECT_OS_COMMIT_EMAIL//[[:space:]]/}" ]]; then
        os_config_fail 'invalid repository variable'
        return 1
      fi
      os_config_temp
      jq -n --arg address "$PROJECT_OS_COMMIT_EMAIL" \
        '{schema_version:1,commit_email:{enforce:true,address:$address}}' > "$OS_CONFIG_FILE"
      OS_CONFIG_SOURCE='on — repository variable'
    else
      profile="${PROJECT_OS_PROFILE-private/project-os.json}"
      if [[ -z "$profile" || "$profile" == /* || "$profile" == *..* ]]; then
        os_config_fail 'invalid CI profile path'; return 1
      fi
      if git cat-file -e "$base:$profile" 2>/dev/null; then
        os_config_temp
        git show "$base:$profile" > "$OS_CONFIG_FILE" || { os_config_fail 'unreadable base profile'; return 1; }
        if [[ "${PROJECT_OS_PROFILE+x}" == x ]]; then
          OS_CONFIG_SOURCE='on — PROJECT_OS_PROFILE'
        else
          OS_CONFIG_SOURCE='on — tracked profile'
        fi
      elif [[ "${PROJECT_OS_PROFILE+x}" == x ]]; then
        os_config_fail 'missing selected base profile'; return 1
      fi
    fi
  elif [[ "${PROJECT_OS_PROFILE+x}" == x ]]; then
    OS_CONFIG_FILE="$PROJECT_OS_PROFILE"
    OS_CONFIG_SOURCE='on — PROJECT_OS_PROFILE'
  elif [[ -e .config/project-os.local.json || -L .config/project-os.local.json ]]; then
    OS_CONFIG_FILE='.config/project-os.local.json'
    OS_CONFIG_SOURCE='on — local profile'
  elif [[ -e private/project-os.json || -L private/project-os.json ]]; then
    OS_CONFIG_FILE='private/project-os.json'
    OS_CONFIG_SOURCE='on — tracked profile'
  fi
  if [[ -z "$OS_CONFIG_SOURCE" ]]; then
    OS_CONFIG_SOURCE='off — no configuration'
  else
    [[ -f "$OS_CONFIG_FILE" && -r "$OS_CONFIG_FILE" ]] || { os_config_fail 'missing or unreadable selected profile'; return 1; }
    jq -e . "$OS_CONFIG_FILE" >/dev/null 2>&1 || { os_config_fail 'malformed JSON'; return 1; }
    kind=$(jq -r -f "$(dirname "${BASH_SOURCE[0]}")/profile.jq" "$OS_CONFIG_FILE" 2>/dev/null) || { os_config_fail 'invalid profile'; return 1; }
    [[ "$kind" == valid ]] || { os_config_fail "$kind"; return 1; }
    os_config_timezone || return 1
  fi
  printf 'configuration source: %s\n' "$OS_CONFIG_SOURCE"
}
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  trap os_config_cleanup EXIT
  os_config_resolve "${1:-}"
fi
