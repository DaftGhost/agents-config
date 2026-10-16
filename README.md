# Agent prompt generator

This repository stores the base prompt heading in `.agents/AGENTS.md` and optional instruction modules in `aside/`, including coding guidance in `aside/coding/` and response and writing style rules in `aside/tones/`. Use the interactive generator to replace prompts or merge selected modules into existing agent configuration files.

Select `coding/coding-guideline.md` to include the coding guidelines in a generated prompt.

```bash
./scripts/generate-agent-prompts.sh
```

See [the complete functionality and test reference](scripts/generate-agent-prompts.md) for write modes, destinations, selection rules, section merging, write safeguards, dependencies, and standalone test case specifications.

## Skill links

Run the [skill-link wizard](scripts/link-skills.sh) in an interactive Bash terminal:

```bash
./scripts/link-skills.sh
```

Run from the project directory whose skills you want to link, or any of its subdirectories (including `scripts/`). Starting from the current working directory obtained with `pwd -P`, the script searches upward and uses the nearest `.agents/skills/` directory. It stops with an error if none is found before reaching the filesystem root; it does not use the script's location as the source project. Choose `~/.claude/skills/`, `~/.agents/skills/`, or both, then select individual skills or all skills containing `SKILL.md`. Review the links and confirm before creating them.

The wizard requires Bash and GNU coreutils `realpath` with `-m` and `--relative-to` support. Missing destination directories are created, and correct relative links are retained. Existing absolute links are offered for replacement individually, even when they point to the correct skill. For each conflicting file, directory, or link (including broken links), the wizard shows the existing entry and intended link, then asks whether to overwrite it; Enter skips it. Confirmed overwrites move the original entry to a unique `.skill-link-backup.XXXXXX/original` path inside the destination directory before creating the link, and print the backup path. Directory contents and symbolic-link targets are preserved. If link creation fails, the original entry is restored when the destination remains free; otherwise the backup is retained and its path is reported.

Links use paths relative to the destination directory and reflect subsequent skill edits immediately. Moving the repository and destination directories together preserves links when their relative layout stays the same. If that layout changes, run the wizard again and approve replacement of its old links. Choices are not saved to `.env`.
