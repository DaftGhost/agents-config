#!/usr/bin/env bash
#
# Interactive wizard that writes the shared agent instructions and selected
# aside modules into agent prompt files, or merges aside sections into them.

set -euo pipefail

if [[ -t 1 ]] && command -v tput >/dev/null 2>&1 && [[ "$(tput colors 2>/dev/null || echo 0)" -ge 8 ]]; then
  BOLD=$(tput bold); DIM=$(tput dim); RESET=$(tput sgr0)
  BLUE=$(tput setaf 4); GREEN=$(tput setaf 2)
else
  BOLD=""; DIM=""; RESET=""; BLUE=""; GREEN=""
fi

TOTAL_STAGES=4
_STAGE_INDEX=0

# Wipe the terminal so only the current step is on screen; no-op off a terminal.
_clear() {
  [[ -t 1 ]] || return 0
  if command -v tput >/dev/null 2>&1; then tput clear; else printf '\033[2J\033[3J\033[H'; fi
}

# stage "Name" — clear the screen, then announce the stage and show progress.
stage() {
  _clear
  _STAGE_INDEX=$((_STAGE_INDEX + 1))
  printf '\n%s%s▸ Stage %s/%s · %s%s\n' "$BOLD" "$BLUE" "$_STAGE_INDEX" "$TOTAL_STAGES" "$1" "$RESET"
}

die() { printf '%s: %s\n' "$1" "$2" >&2; exit 1; }
say()  { printf '  %s\n' "$1"; }
note() { printf '  %s%s%s\n' "$DIM" "$1" "$RESET"; }

# ask VAR "Prompt" — read a visible value into $VAR.
ask() {
  local input
  printf '  %s%s%s ' "$BOLD" "$2" "$RESET"
  read -r input || true
  printf -v "$1" '%s' "$input"
}

# finish — clear, then print the closing line.
finish() {
  _clear
  printf '\n%s%s  ✓ Setup complete%s\n\n' "$BOLD" "$GREEN" "$RESET"
}

merge_error() {
  printf 'Cannot merge aside sections: %s\n' "$1" >&2
  return 1
}

scan_headings() {
  local file="$1" line content fence='' marker info title
  local heading_re='^ {0,3}(#{1,6})([[:blank:]]+(.*))?$'
  local fence_re='^ {0,3}(`{3,}|~{3,})(.*)$'
  local closing_re='(^|[[:blank:]]+)#+[[:blank:]]*$'
  HEADING_LINES=(); HEADING_LEVELS=(); HEADING_TITLES=()
  LINE_COUNT=0; FIRST_CONTENT_LINE=0; LAST_CONTENT_LINE=0
  while IFS= read -r line || [[ -n "$line" ]]; do
    LINE_COUNT=$((LINE_COUNT + 1))
    if [[ "$line" =~ [^[:space:]] ]]; then
      if (( FIRST_CONTENT_LINE == 0 )); then FIRST_CONTENT_LINE=$LINE_COUNT; fi
      LAST_CONTENT_LINE=$LINE_COUNT
    fi
    content="$line"
    while [[ "$content" == *$'\r' ]]; do content="${content%$'\r'}"; done
    if [[ -n "$fence" ]]; then
      if [[ "$content" =~ $fence_re ]]; then
        marker="${BASH_REMATCH[1]}"; info="${BASH_REMATCH[2]}"
        if [[ "${marker:0:1}" == "${fence:0:1}" && ${#marker} -ge ${#fence} && "$info" =~ ^[[:space:]]*$ ]]; then
          fence=''
        fi
      fi
      continue
    fi
    if [[ "$content" =~ $fence_re ]]; then
      marker="${BASH_REMATCH[1]}"; info="${BASH_REMATCH[2]}"
      if [[ "$marker" != '`'* || "$info" != *'`'* ]]; then fence="$marker"; fi
      continue
    fi
    if [[ "$content" =~ $heading_re ]]; then
      marker="${BASH_REMATCH[1]}"; title="${BASH_REMATCH[3]}"
      if [[ "$title" =~ $closing_re ]]; then title="${title%"${BASH_REMATCH[0]}"}"; fi
      title="${title#"${title%%[![:blank:]]*}"}"
      title="${title%"${title##*[![:blank:]]}"}"
      HEADING_LINES+=("$LINE_COUNT")
      HEADING_LEVELS+=("${#marker}")
      HEADING_TITLES+=("$title")
    fi
  done < "$file"
  if [[ -n "$fence" ]]; then
    merge_error 'Unclosed fenced code block; refusing an ambiguous section merge'
    return 1
  fi
}

ensure_final_newline() {
  if [[ "$(tail -c 1 "$1" | wc -l)" -eq 0 ]]; then printf '\n' >> "$1"; fi
}

merge_sections() (
  set -euo pipefail
  export LC_ALL=C
  local original="$1" output="$2" aside result section old_section next
  local start level title core_lines source_blanks match end index existing_blanks
  shift 2
  local work_dir
  work_dir="$(mktemp -d "${TMPDIR:-/tmp}/agent-merge.XXXXXX")"
  trap 'rm -rf "$work_dir"' EXIT
  trap 'exit 130' INT
  trap 'exit 143' TERM
  result="$work_dir/result"
  cp "$original" "$result"
  for aside in "$@"; do
    if ! iconv -f UTF-8 -t UTF-8 "$aside" >/dev/null; then
      merge_error "Cannot read UTF-8 aside: $aside"; exit 1
    fi
    scan_headings "$aside"
    if (( ${#HEADING_LINES[@]} == 0 )); then
      merge_error 'Aside must start with an ATX heading'; exit 1
    fi
    start="${HEADING_LINES[0]}"; level="${HEADING_LEVELS[0]}"; title="${HEADING_TITLES[0]}"
    if (( FIRST_CONTENT_LINE != start )); then
      merge_error 'Aside must contain one main heading and its child sections'; exit 1
    fi
    for (( index=1; index<${#HEADING_LINES[@]}; index++ )); do
      if (( HEADING_LEVELS[index] <= level )); then
        merge_error 'Aside must contain one main heading and its child sections'; exit 1
      fi
    done
    section="$work_dir/section"
    tail -n "+$start" "$aside" > "$section"
    ensure_final_newline "$section"
    scan_headings "$section"
    core_lines=$LAST_CONTENT_LINE
    source_blanks=$((LINE_COUNT - LAST_CONTENT_LINE))
    if ! iconv -f UTF-8 -t UTF-8 "$result" >/dev/null; then
      merge_error "Cannot read UTF-8 original: $original"; exit 1
    fi
    scan_headings "$result"
    match=-1
    for index in "${!HEADING_LINES[@]}"; do
      if [[ "${HEADING_LEVELS[$index]}" == "$level" && "${HEADING_TITLES[$index]}" == "$title" ]]; then
        match=$index; break
      fi
    done
    next="$work_dir/next"
    if (( match >= 0 )); then
      start="${HEADING_LINES[$match]}"
      end=$((LINE_COUNT + 1))
      for (( index=match+1; index<${#HEADING_LINES[@]}; index++ )); do
        if (( HEADING_LEVELS[index] <= level )); then end="${HEADING_LINES[$index]}"; break; fi
      done
      old_section="$work_dir/old-section"
      head -n "$((end - 1))" "$result" | tail -n "+$start" > "$old_section"
      scan_headings "$old_section"
      existing_blanks=$((LINE_COUNT - LAST_CONTENT_LINE))
      {
        head -n "$((start - 1))" "$result"
        if (( source_blanks > 0 )); then
          cat "$section"
        else
          head -n "$core_lines" "$section"
          if (( existing_blanks > 0 )); then tail -n "$existing_blanks" "$old_section"; fi
        fi
        tail -n "+$end" "$result"
      } > "$next"
    else
      cp "$result" "$next"
      if [[ -s "$next" ]]; then
        ensure_final_newline "$next"
        if ! cmp -s <(tail -c 2 "$next") <(printf '\n\n') && ! cmp -s <(tail -c 3 "$next") <(printf '\n\r\n'); then
          printf '\n' >> "$next"
        fi
      fi
      cat "$section" >> "$next"
    fi
    mv -f "$next" "$result"
  done
  cp "$result" "$output"
)

# Only a single "y" or "Y" confirms; any other reply, including "yes", declines.
confirm_write() {
  local reply='' IFS=''
  ask reply "$1 [y/N]"
  [[ "$reply" =~ ^[Yy]$ ]]
}

expand_destination_path() {
  local input="$1"
  case "$input" in
    '~') EXPANDED_PATH="$HOME" ;;
    \~/*) EXPANDED_PATH="$HOME/${input:2}" ;;
    /*) EXPANDED_PATH="$input" ;;
    *)
      printf 'Use an absolute path or a path beginning with "~/".\n' >&2
      return 1
      ;;
  esac
}

dest_error() { printf '%s: %s\n' "$1" "$EXPANDED_PATH" >&2; }

add_destination() {
  local label="$1" input="$2" existing parent
  if ! expand_destination_path "$input"; then return 1; fi
  if [[ "$input" == */ ]]; then
    dest_error 'That path is a directory path. Enter a file path instead'; return 1
  fi
  if [[ ! -L "$EXPANDED_PATH" ]]; then
    if [[ -d "$EXPANDED_PATH" ]]; then
      dest_error 'That path is a directory. Enter a file path instead'; return 1
    fi
    if [[ -e "$EXPANDED_PATH" && ! -f "$EXPANDED_PATH" ]]; then
      dest_error 'That path is not a regular file. Enter a file path instead'; return 1
    fi
  fi
  parent="$(dirname "$EXPANDED_PATH")"
  if [[ -e "$parent" && ! -d "$parent" ]]; then
    dest_error 'The parent path is not a directory. Enter a file path under a directory'; return 1
  fi
  for existing in "$BASE_PROMPT" ${ASIDE_FILES[@]+"${ASIDE_FILES[@]}"}; do
    if [[ "$EXPANDED_PATH" == "$existing" ]]; then
      dest_error 'Cannot use a source prompt as an output destination'; return 1
    fi
  done
  for existing in ${DEST_PATHS[@]+"${DEST_PATHS[@]}"}; do
    if [[ "$existing" == "$EXPANDED_PATH" ]]; then
      printf 'Already selected: %s\n' "$EXPANDED_PATH"
      return 0
    fi
  done
  DEST_NAMES+=("$label")
  DEST_PATHS+=("$EXPANDED_PATH")
}

# parse_numbers CHOICE MAX [CUSTOM]: fill SELECTED with unique zero-based indexes
# for comma-separated numbers 1..MAX; number CUSTOM sets CUSTOM_SELECTED instead.
parse_numbers() {
  local token number seen=' '
  local -a tokens
  SELECTED=()
  CUSTOM_SELECTED=false
  IFS=',' read -r -a tokens <<< "$1"
  for token in "${tokens[@]}"; do
    token="${token//[[:space:]]/}"
    if [[ ! "$token" =~ ^[0-9]+$ ]]; then return 1; fi
    number=$((10#$token))
    if (( number < 1 || number > $2 )); then return 1; fi
    if (( number == ${3:-0} )); then CUSTOM_SELECTED=true; continue; fi
    if [[ "$seen" != *" $number "* ]]; then SELECTED+=("$((number - 1))"); seen+="$number "; fi
  done
}

select_destinations() {
  local choice index
  say 'Choose one or more destinations:'
  for index in "${!TARGET_NAMES[@]}"; do printf '  %d) %s → %s\n' "$((index + 1))" "${TARGET_NAMES[$index]}" "${TARGET_PATHS[$index]}"; done
  printf '  5) Add a custom file path\n'
  printf 'Enter numbers separated by commas, or "all" for presets 1–4.\n'
  while true; do
    ask choice '>'
    SELECTED=()
    CUSTOM_SELECTED=false
    if [[ "$choice" == all ]]; then
      for index in "${!TARGET_NAMES[@]}"; do SELECTED+=("$index"); done
      return
    fi
    if [[ -z "$choice" ]]; then printf 'Choose at least one destination.\n'; continue; fi
    if parse_numbers "$choice" 5 5; then return; fi
    printf 'Invalid selection. Enter one or more numbers from 1 to 5.\n'
  done
}

select_many() {
  local title="$1" allow_empty="$2" choice index
  shift 2
  local -a options=("$@")
  SELECTED=()
  say "$title"
  for (( index=0; index<${#options[@]}; index++ )); do printf '  %d) %s\n' "$((index + 1))" "${options[$index]}"; done
  if [[ "$allow_empty" == true ]]; then
    printf 'Enter numbers separated by commas, "all", or press Enter for none.\n'
  else
    printf 'Enter numbers separated by commas, or "all".\n'
  fi
  while true; do
    ask choice '>'
    SELECTED=()
    if [[ "$choice" == all ]]; then
      for (( index=0; index<${#options[@]}; index++ )); do SELECTED+=("$index"); done
      return
    fi
    if [[ -z "$choice" && "$allow_empty" == true ]]; then return; fi
    if [[ -z "$choice" ]]; then printf 'Choose at least one item.\n'; continue; fi
    if parse_numbers "$choice" "${#options[@]}"; then return; fi
    printf 'Invalid selection. Use the listed numbers, separated by commas.\n'
  done
}

# Sourcing exposes the merge functions without starting the interactive wizard.
if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then return 0; fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BASE_PROMPT="$REPO_ROOT/.agents/AGENTS.md"
ASIDE_DIR="$REPO_ROOT/aside"

if [[ ! -t 0 ]]; then
  printf 'Run this prompt generator in an interactive terminal.\n' >&2
  exit 1
fi

WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/agent-prompt.XXXXXX")"
target_tmp=''
cleanup() {
  rm -rf "$WORK_DIR"
  if [[ -n "$target_tmp" ]]; then rm -f "$target_tmp"; fi
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
# The library needs terminal clearing; fall back to ANSI capabilities for dumb PTYs.
if [[ -t 1 ]] && command -v tput >/dev/null 2>&1 && ! tput clear >/dev/null 2>&1; then
  export TERM=xterm
fi

TARGET_NAMES=("Claude" "Codex" "Shared agents" "DSH")
TARGET_PATHS=(
  "$HOME/.claude/CLAUDE.md"
  "$HOME/.codex/AGENTS.md"
  "$HOME/.agents/AGENTS.md"
  "$HOME/.dsh/AGENTS.md"
)
ASIDE_FILES=()
for file in "$ASIDE_DIR"/*/*.md; do
  [[ -f "$file" ]] && ASIDE_FILES+=("$file")
done

stage 'Choose write mode'
printf '  1) Replace with shared instructions and selected aside files (default)\n'
printf '  2) Append selected aside sections to existing regular files only\n'
while true; do
  ask mode_choice 'Write mode [1]:'
  # shellcheck disable=SC2154 # ask assigns mode_choice indirectly via printf -v
  case "$mode_choice" in
    ''|1) WRITE_MODE=replace; break ;;
    2) WRITE_MODE=append; break ;;
    *) printf 'Invalid mode. Enter 1 or 2.\n' ;;
  esac
done
if [[ "$WRITE_MODE" == replace && ! -f "$BASE_PROMPT" ]]; then
  die 'Shared prompt file not found' "$BASE_PROMPT"
fi

stage 'Choose destination agents and paths'
select_destinations
DEST_NAMES=()
DEST_PATHS=()
for target_index in ${SELECTED[@]+"${SELECTED[@]}"}; do
  add_destination "${TARGET_NAMES[$target_index]}" "${TARGET_PATHS[$target_index]}"
done
if [[ "$CUSTOM_SELECTED" == true ]]; then
  printf 'Enter a custom output file path (absolute path or ~/path). Existing directories are rejected; a new file may be created at a path that does not exist yet.\n'
  custom_added=false
  while true; do
    ask custom_path 'Custom file path:'
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

stage 'Choose aside files'
ASIDE_OPTIONS=()
for file in ${ASIDE_FILES[@]+"${ASIDE_FILES[@]}"}; do ASIDE_OPTIONS+=("${file#"$ASIDE_DIR/"}"); done
if [[ "$WRITE_MODE" == append ]]; then
  aside_title='Choose aside files to append or replace matching sections; shared instructions will not be added:'
else
  aside_title='The shared behavior prompt is always included. Choose optional aside files:'
fi
select_many "$aside_title" true ${ASIDE_OPTIONS[@]+"${ASIDE_OPTIONS[@]}"}
SELECTED_ASIDE_FILES=()
for aside_index in ${SELECTED[@]+"${SELECTED[@]}"}; do SELECTED_ASIDE_FILES+=("${ASIDE_FILES[$aside_index]}"); done
if [[ "$WRITE_MODE" == append ]] && (( ${#SELECTED[@]} == 0 )); then
  printf '\nNo aside files selected; no files will be written.\n'
  exit 0
fi

CONTENT_FILE="$WORK_DIR/content"
if [[ "$WRITE_MODE" == replace ]]; then
  cat "$BASE_PROMPT" > "$CONTENT_FILE"
  for file in ${SELECTED_ASIDE_FILES[@]+"${SELECTED_ASIDE_FILES[@]}"}; do
    printf '\n\n' >> "$CONTENT_FILE"
    cat "$file" >> "$CONTENT_FILE"
  done
fi

stage 'Review and write'
printf 'Write mode: %s\nIncluded files:\n' "$WRITE_MODE"
if [[ "$WRITE_MODE" == replace ]]; then printf '  %s\n' "$BASE_PROMPT"; fi
for file in ${SELECTED_ASIDE_FILES[@]+"${SELECTED_ASIDE_FILES[@]}"}; do printf '  %s\n' "$file"; done
printf '\nDestinations:\n'
DEST_CONTENTS=()
DEST_SNAPSHOTS=()
SKIPPED_PATHS=()
for index in "${!DEST_PATHS[@]}"; do
  target="${DEST_PATHS[$index]}"
  DEST_CONTENTS+=("")
  DEST_SNAPSHOTS+=("")
  printf '  %s → %s\n' "${DEST_NAMES[$index]}" "$target"
  if [[ ! -L "$target" && -e "$target" && ! -f "$target" ]]; then
    die 'Destination is not a regular file' "$target"
  fi
  if [[ "$WRITE_MODE" == append ]]; then
    if [[ -L "$target" ]]; then
      printf '    (symbolic link; append mode skips this destination)\n'
      SKIPPED_PATHS+=("$target")
      continue
    fi
    if [[ ! -e "$target" ]]; then
      printf '    (does not exist; append mode skips this destination)\n'
      SKIPPED_PATHS+=("$target")
      continue
    fi
    snapshot="$WORK_DIR/snapshot.$index"
    content="$WORK_DIR/content.$index"
    cp -p "$target" "$snapshot"
    merge_sections "$snapshot" "$content" ${SELECTED_ASIDE_FILES[@]+"${SELECTED_ASIDE_FILES[@]}"}
    DEST_CONTENTS[$index]="$content"
    DEST_SNAPSHOTS[$index]="$snapshot"
    printf '    (existing regular file; matching sections will be replaced, other content retained)\n'
  else
    DEST_CONTENTS[$index]="$CONTENT_FILE"
    if [[ -L "$target" ]]; then
      printf '    (symbolic link; replacement will make this path a regular file and leave its target unchanged)\n'
    elif [[ -e "$target" ]]; then
      printf '    (file exists; you will choose whether to replace it)\n'
    else
      printf '    (new file)\n'
    fi
  fi
  printf '\nPreview for %s (%s bytes):\n\n' "$target" "$(wc -c < "${DEST_CONTENTS[$index]}" | tr -d '[:space:]')"
  cat "${DEST_CONTENTS[$index]}"
  printf '\n'
done

WRITE_PATHS=()
WRITE_ACTIONS=()
WRITE_CONTENTS=()
WRITE_SNAPSHOTS=()
for index in "${!DEST_PATHS[@]}"; do
  target="${DEST_PATHS[$index]}"
  if [[ -z "${DEST_CONTENTS[$index]}" ]]; then continue; fi
  if [[ "$WRITE_MODE" == append ]]; then
    action=append
    prompt="Append selected aside sections to $target?"
  elif [[ -L "$target" ]]; then
    action=replace-link
    prompt="Replace symbolic link $target with a regular file? Its linked target will remain unchanged."
  elif [[ -e "$target" ]]; then
    action=replace
    prompt="Replace existing file $target?"
  else
    action=create
    prompt="Create new file $target?"
  fi
  if confirm_write "$prompt"; then
    WRITE_PATHS+=("$target")
    WRITE_ACTIONS+=("$action")
    WRITE_CONTENTS+=("${DEST_CONTENTS[$index]}")
    WRITE_SNAPSHOTS+=("${DEST_SNAPSHOTS[$index]}")
  else
    SKIPPED_PATHS+=("$target")
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
  content="${WRITE_CONTENTS[$index]}"
  snapshot="${WRITE_SNAPSHOTS[$index]}"
  if [[ "$action" == replace-link && ! -L "$target" ]]; then
    die 'The symbolic link changed after review; refusing to replace it' "$target"
  fi
  if [[ "$action" != replace-link && -L "$target" ]]; then
    die 'Destination became a symbolic link after review' "$target"
  fi
  if [[ ! -L "$target" && -e "$target" && ! -f "$target" ]]; then
    die 'Destination is no longer a regular file' "$target"
  fi
  if [[ "$action" == create && ( -e "$target" || -L "$target" ) ]]; then
    die 'Destination appeared after review; refusing to replace it' "$target"
  fi
  target_dir="$(dirname "$target")"
  mkdir -p "$target_dir"
  target_tmp="$(mktemp "$target_dir/.agent-prompt.XXXXXX")"
  if ! cp "$content" "$target_tmp"; then rm -f "$target_tmp"; die 'Failed to prepare destination' "$target"; fi
  if [[ "$action" == append ]]; then
    permissions="$(stat -c '%a' "$snapshot" 2>/dev/null || stat -f '%Lp' "$snapshot")"
    chmod "$permissions" "$target_tmp"
    if [[ -L "$target" || ! -f "$target" ]] || ! cmp -s "$snapshot" "$target"; then
      die 'Destination changed after review; refusing to append' "$target"
    fi
  else
    chmod 0644 "$target_tmp"
  fi
  if [[ "$action" == replace-link ]]; then
    link_backup="$(mktemp "$target_dir/.agent-prompt-link.XXXXXX")"
    if ! mv -f "$target" "$link_backup"; then
      rm -f "$link_backup" "$target_tmp"
      die 'Failed to move the symbolic link before replacement' "$target"
    fi
    if ! mv -f "$target_tmp" "$target"; then
      if ! mv -f "$link_backup" "$target"; then
        printf 'Failed to write %s and could not restore its original symbolic link at %s\n' "$target" "$link_backup" >&2
        exit 1
      fi
      rm -f "$target_tmp"
      die 'Failed to write destination' "$target"
    fi
    rm -f "$link_backup"
  elif ! mv -f "$target_tmp" "$target"; then
    rm -f "$target_tmp"
    die 'Failed to write destination' "$target"
  fi
  target_tmp=''
  cmp -s "$content" "$target" || die 'Verification failed after writing' "$target"
  printf 'Wrote %s\n' "$target"
done
finish
say 'Prompt generation complete.'
for target in "${WRITE_PATHS[@]}"; do say "Wrote $target"; done
for (( index=0; index<${#SKIPPED_PATHS[@]}; index++ )); do
  target="${SKIPPED_PATHS[$index]}"
  note "Left unchanged: $target"
done
