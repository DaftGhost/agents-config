#!/usr/bin/env bash
set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BASE_PROMPT="$REPO_ROOT/.agents/AGENTS.md"
TONES_DIR="$REPO_ROOT/tones"

if [[ ! -t 0 ]]; then
  printf 'Run this prompt generator in an interactive terminal.\n' >&2
  exit 1
fi
if [[ ! -f "$BASE_PROMPT" ]]; then
  printf 'Shared prompt file not found: %s\n' "$BASE_PROMPT" >&2
  exit 1
fi

TARGET_NAMES=("Claude" "Codex" "Shared agents" "DSH")
TARGET_PATHS=(
  "$HOME/.claude/CLAUDE.md"
  "$HOME/.codex/AGENTS.md"
  "$HOME/.agents/AGENTS.md"
  "$HOME/.dsh/AGENTS.md"
)
TONE_FILES=()
for tone in "$TONES_DIR"/*.md; do
  [[ -f "$tone" ]] && TONE_FILES+=("$tone")
done

stage() { printf '\n== %s ==\n' "$1"; }
confirm() {
  local answer
  read -r -p "$1 [y/N] " answer
  [[ "$answer" =~ ^[Yy]$ ]]
}

expand_destination_path() {
  local input="$1"
  case "$input" in
    '~') EXPANDED_PATH="$HOME" ;;
    '~/'*) EXPANDED_PATH="$HOME/${input:2}" ;;
    /*) EXPANDED_PATH="$input" ;;
    *)
      printf 'Use an absolute path or a path beginning with "~/".\n' >&2
      return 1
      ;;
  esac
}

add_destination() {
  local label="$1" input="$2" existing source_file parent
  if ! expand_destination_path "$input"; then return 1; fi
  if [[ "$input" == */ ]]; then
    printf 'That path is a directory path. Enter a file path instead: %s\n' "$EXPANDED_PATH" >&2
    return 1
  fi
  if [[ ! -L "$EXPANDED_PATH" && -d "$EXPANDED_PATH" ]]; then
    printf 'That path is a directory. Enter a file path instead: %s\n' "$EXPANDED_PATH" >&2
    return 1
  fi
  if [[ ! -L "$EXPANDED_PATH" && -e "$EXPANDED_PATH" && ! -f "$EXPANDED_PATH" ]]; then
    printf 'That path is not a regular file. Enter a file path instead: %s\n' "$EXPANDED_PATH" >&2
    return 1
  fi
  parent="$(dirname "$EXPANDED_PATH")"
  if [[ -e "$parent" && ! -d "$parent" ]]; then
    printf 'The parent path is not a directory. Enter a file path under a directory: %s\n' "$EXPANDED_PATH" >&2
    return 1
  fi
  if [[ "$EXPANDED_PATH" == "$BASE_PROMPT" ]]; then
    printf 'Cannot use a source prompt as an output destination: %s\n' "$EXPANDED_PATH" >&2
    return 1
  fi
  for source_file in "${TONE_FILES[@]}"; do
    if [[ "$EXPANDED_PATH" == "$source_file" ]]; then
      printf 'Cannot use a source prompt as an output destination: %s\n' "$EXPANDED_PATH" >&2
      return 1
    fi
  done
  for existing in "${DEST_PATHS[@]}"; do
    if [[ "$existing" == "$EXPANDED_PATH" ]]; then
      printf 'Already selected: %s\n' "$EXPANDED_PATH"
      return 0
    fi
  done
  DEST_NAMES+=("$label")
  DEST_PATHS+=("$EXPANDED_PATH")
}

select_destinations() {
  local choice token index number valid duplicate existing
  local -a tokens
  SELECTED=()
  CUSTOM_SELECTED=false
  printf 'Choose one or more destinations:\n'
  for index in "${!TARGET_NAMES[@]}"; do printf '  %d) %s → %s\n' "$((index + 1))" "${TARGET_NAMES[$index]}" "${TARGET_PATHS[$index]}"; done
  printf '  5) Add a custom file path\n'
  printf 'Enter numbers separated by commas, or "all" for presets 1–4.\n'
  while true; do
    read -r -p '> ' choice
    SELECTED=()
    CUSTOM_SELECTED=false
    if [[ "$choice" == all ]]; then
      for index in "${!TARGET_NAMES[@]}"; do SELECTED+=("$index"); done
      return
    fi
    if [[ -z "$choice" ]]; then printf 'Choose at least one destination.\n'; continue; fi
    IFS=',' read -r -a tokens <<< "$choice"
    valid=true
    for token in "${tokens[@]}"; do
      token="${token//[[:space:]]/}"
      if [[ ! "$token" =~ ^[0-9]+$ ]]; then
        valid=false
        break
      fi
      number=$((10#$token))
      if (( number < 1 || number > 5 )); then
        valid=false
        break
      fi
      if (( number == 5 )); then
        CUSTOM_SELECTED=true
        continue
      fi
      index=$((number - 1))
      duplicate=false
      for existing in "${SELECTED[@]}"; do
        if [[ "$existing" == "$index" ]]; then duplicate=true; fi
      done
      if [[ "$duplicate" == false ]]; then SELECTED+=("$index"); fi
    done
    if [[ "$valid" == true ]]; then return; fi
    printf 'Invalid selection. Enter one or more numbers from 1 to 5.\n'
  done
}

select_many() {
  local title="$1" allow_empty="$2" choice token index number valid duplicate existing
  shift 2
  local -a options=("$@") tokens
  SELECTED=()
  printf '%s\n' "$title"
  for index in "${!options[@]}"; do printf '  %d) %s\n' "$((index + 1))" "${options[$index]}"; done
  if [[ "$allow_empty" == true ]]; then
    printf 'Enter numbers separated by commas, "all", or press Enter for none.\n'
  else
    printf 'Enter numbers separated by commas, or "all".\n'
  fi
  while true; do
    read -r -p '> ' choice
    SELECTED=()
    if [[ "$choice" == all ]]; then
      for index in "${!options[@]}"; do SELECTED+=("$index"); done
      return
    fi
    if [[ -z "$choice" && "$allow_empty" == true ]]; then return; fi
    if [[ -z "$choice" ]]; then printf 'Choose at least one item.\n'; continue; fi
    IFS=',' read -r -a tokens <<< "$choice"
    valid=true
    for token in "${tokens[@]}"; do
      token="${token//[[:space:]]/}"
      if [[ ! "$token" =~ ^[0-9]+$ ]]; then valid=false; break; fi
      number=$((10#$token))
      if (( number < 1 || number > ${#options[@]} )); then valid=false; break; fi
      index=$((number - 1))
      duplicate=false
      for existing in "${SELECTED[@]}"; do
        if [[ "$existing" == "$index" ]]; then duplicate=true; fi
      done
      if [[ "$duplicate" == false ]]; then SELECTED+=("$index"); fi
    done
    if [[ "$valid" == true ]]; then return; fi
    printf 'Invalid selection. Use the listed numbers, separated by commas.\n'
  done
}

stage '1/3 Choose destination agents and paths'
select_destinations
SELECTED_TARGETS=("${SELECTED[@]}")
DEST_NAMES=()
DEST_PATHS=()
for index in "${SELECTED_TARGETS[@]}"; do add_destination "${TARGET_NAMES[$index]}" "${TARGET_PATHS[$index]}"; done
if [[ "$CUSTOM_SELECTED" == true ]]; then
  printf 'Enter a custom output file path (absolute path or ~/path). Existing directories are rejected; a new file may be created at a path that does not exist yet.\n'
  custom_added=false
  while true; do
    read -r -p 'Custom file path: ' custom_path
    if [[ -z "$custom_path" ]]; then
      if [[ "$custom_added" == true ]]; then break; fi
      printf 'Option 5 requires a file path. Enter a file path or press Ctrl-C to cancel.\n'
      continue
    fi
    if add_destination 'Custom' "$custom_path"; then custom_added=true; fi
  done
fi
if (( ${#DEST_PATHS[@]} == 0 )); then
  printf 'Choose at least one preset or custom destination.\n' >&2
  exit 1
fi

stage '2/3 Choose tone files'
TONE_OPTIONS=()
for tone in "${TONE_FILES[@]}"; do TONE_OPTIONS+=("$(basename "$tone" .md)"); done
select_many 'The shared behavior prompt is always included. Choose optional tone files:' true "${TONE_OPTIONS[@]}"
SELECTED_TONES=("${SELECTED[@]}")

CONTENT_FILE="$(mktemp "${TMPDIR:-/tmp}/agent-prompt.XXXXXX")"
trap 'rm -f "$CONTENT_FILE"' EXIT
cat "$BASE_PROMPT" > "$CONTENT_FILE"
for index in "${SELECTED_TONES[@]}"; do
  printf '\n\n' >> "$CONTENT_FILE"
  cat "${TONE_FILES[$index]}" >> "$CONTENT_FILE"
done

stage '3/3 Review and write'
printf 'Included files:\n  %s\n' "$BASE_PROMPT"
for index in "${SELECTED_TONES[@]}"; do printf '  %s\n' "${TONE_FILES[$index]}"; done
  printf '\nDestinations:\n'
for index in "${!DEST_PATHS[@]}"; do
  target="${DEST_PATHS[$index]}"
  printf '  %s → %s\n' "${DEST_NAMES[$index]}" "$target"
  if [[ -L "$target" ]]; then
    printf '    (symbolic link; replacement will make this path a regular file and leave its target unchanged)\n'
  elif [[ -e "$target" ]]; then
    if [[ ! -f "$target" ]]; then printf 'Destination is not a regular file: %s\n' "$target" >&2; exit 1; fi
    printf '    (file exists; you will choose whether to replace it)\n'
  else
    printf '    (new file)\n'
  fi
done
printf '\nGenerated prompt (%s bytes):\n\n' "$(wc -c < "$CONTENT_FILE" | tr -d '[:space:]')"
cat "$CONTENT_FILE"
printf '\n'

WRITE_PATHS=()
WRITE_ACTIONS=()
SKIPPED_PATHS=()
for target in "${DEST_PATHS[@]}"; do
  if [[ -L "$target" ]]; then
    if confirm "Replace symbolic link $target with a regular file? Its linked target will remain unchanged."; then
      WRITE_PATHS+=("$target")
      WRITE_ACTIONS+=(replace-link)
    else
      SKIPPED_PATHS+=("$target")
    fi
  elif [[ -e "$target" ]]; then
    if confirm "Replace existing file $target?"; then
      WRITE_PATHS+=("$target")
      WRITE_ACTIONS+=(replace)
    else
      SKIPPED_PATHS+=("$target")
    fi
  else
    if confirm "Create new file $target?"; then
      WRITE_PATHS+=("$target")
      WRITE_ACTIONS+=(create)
    else
      SKIPPED_PATHS+=("$target")
    fi
  fi
done
if (( ${#SKIPPED_PATHS[@]} > 0 )); then
  printf '\nWill leave unchanged:\n'
  for target in "${SKIPPED_PATHS[@]}"; do printf '  %s\n' "$target"; done
fi
if (( ${#WRITE_PATHS[@]} == 0 )); then
  printf '\nNo destinations were selected for writing.\n'
  exit 0
fi

for index in "${!WRITE_PATHS[@]}"; do
  target="${WRITE_PATHS[$index]}"
  action="${WRITE_ACTIONS[$index]}"
  if [[ "$action" == replace-link && ! -L "$target" ]]; then
    printf 'The symbolic link changed after review; refusing to replace it: %s\n' "$target" >&2
    exit 1
  fi
  if [[ "$action" != replace-link && -L "$target" ]]; then
    printf 'Destination became a symbolic link after review: %s\n' "$target" >&2
    exit 1
  fi
  if [[ ! -L "$target" && -e "$target" && ! -f "$target" ]]; then
    printf 'Destination is no longer a regular file: %s\n' "$target" >&2
    exit 1
  fi
  if [[ "$action" == create && ( -e "$target" || -L "$target" ) ]]; then
    printf 'Destination appeared after review; refusing to replace it: %s\n' "$target" >&2
    exit 1
  fi
  target_dir="$(dirname "$target")"
  mkdir -p "$target_dir"
  target_tmp="$(mktemp "$target_dir/.agent-prompt.XXXXXX")"
  if ! cp "$CONTENT_FILE" "$target_tmp"; then rm -f "$target_tmp"; printf 'Failed to prepare destination: %s\n' "$target" >&2; exit 1; fi
  chmod 0644 "$target_tmp"
  if [[ "$action" == replace-link ]]; then
    link_backup="$(mktemp "$target_dir/.agent-prompt-link.XXXXXX")"
    if ! mv -f "$target" "$link_backup"; then
      rm -f "$link_backup" "$target_tmp"
      printf 'Failed to move the symbolic link before replacement: %s\n' "$target" >&2
      exit 1
    fi
    if ! mv -f "$target_tmp" "$target"; then
      if ! mv -f "$link_backup" "$target"; then
        printf 'Failed to write %s and could not restore its original symbolic link at %s\n' "$target" "$link_backup" >&2
        exit 1
      fi
      rm -f "$target_tmp"
      printf 'Failed to write destination: %s\n' "$target" >&2
      exit 1
    fi
    rm -f "$link_backup"
  elif ! mv -f "$target_tmp" "$target"; then
    rm -f "$target_tmp"
    printf 'Failed to write destination: %s\n' "$target" >&2
    exit 1
  fi
  cmp -s "$CONTENT_FILE" "$target" || { printf 'Verification failed after writing: %s\n' "$target" >&2; exit 1; }
  printf 'Wrote %s\n' "$target"
done
printf '\nPrompt generation complete.\n'
