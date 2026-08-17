#!/usr/bin/env bash
# Generate registration artifacts for one Kepler survey package.

set -euo pipefail

usage() {
  printf 'Usage: %s PATH/TO/SURVEY\n' "${0##*/}" >&2
}

if [[ $# -ne 1 ]]; then
  usage
  exit 2
fi

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
survey_dir="$(cd -- "$1" && pwd)"

if [[ ! -d "$survey_dir" ]]; then
  printf 'error: survey directory does not exist: %s\n' "$survey_dir" >&2
  exit 1
fi

validation_report_path="$survey_dir/validation-report.json"
registry_path="$survey_dir/registry.json"

existing_artifacts=()
if [[ -e "$validation_report_path" || -L "$validation_report_path" ]]; then
  existing_artifacts+=("validation-report.json")
fi
if [[ -e "$registry_path" || -L "$registry_path" ]]; then
  existing_artifacts+=("registry.json")
fi

if (( ${#existing_artifacts[@]} > 0 )); then
  printf 'warning: existing registration artifact(s) will be deleted and replaced:\n' >&2
  for artifact in "${existing_artifacts[@]}"; do
    printf '  - %s\n' "$survey_dir/$artifact" >&2
  done

  read -r -p 'Continue? [y/N] ' response
  if [[ "$response" != "y" && "$response" != "Y" ]]; then
    printf 'Registration artifact generation cancelled.\n' >&2
    exit 0
  fi
fi

tmp_dir="$(mktemp -d "${TMPDIR:-/tmp}/kepler-registration.XXXXXX")"
trap 'rm -rf "$tmp_dir"' EXIT

python3 "$script_dir/generate-validation-report.py" "$survey_dir" \
  > "$tmp_dir/validation-report.json"

python3 "$script_dir/generate-registry-record.py" "$survey_dir" \
  > "$tmp_dir/registry.json"

if (( ${#existing_artifacts[@]} > 0 )); then
  rm -f -- "$validation_report_path" "$registry_path"
fi

mv "$tmp_dir/validation-report.json" "$validation_report_path"
mv "$tmp_dir/registry.json" "$registry_path"

printf 'Wrote %s\n' "$validation_report_path"
printf 'Wrote %s\n' "$registry_path"