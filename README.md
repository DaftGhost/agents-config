# Agent prompt generator

This repository stores shared agent instructions in `.agents/AGENTS.md` and optional modules in `aside/`, including response and writing style rules in `aside/tones/`. Use the interactive generator to compose them and write the same prompt to one or more agent configuration paths.

```bash
./scripts/generate-agent-prompts.sh
```

The shared instructions are always included. The generator discovers Markdown files directly inside each `aside/` subfolder and lists them as `<subfolder>/<filename>`, for example `tones/warm.md`. Add a Markdown file under any `aside/` subfolder to make it available automatically. Choose any optional files in the terminal; enter their numbers in the order they should appear, separated by commas. Destination options 1–4 select preset paths; option 5 opens custom file path entry. Custom paths must be absolute or begin with `~/`. You can enter more than one custom file path, one per line.

The custom path prompt rejects existing directories, directory paths ending in `/`, and paths whose parent is an existing file; it asks for a file path again. A symbolic link is accepted as an output path. Replacing it turns that path into a regular file while leaving the link's former target unchanged. A path that does not exist yet is accepted as a new file destination. The generator previews the complete result before writing, then asks individually whether to replace each existing file or create each new file. Answering no skips that destination. It verifies every written file. Source prompt files cannot be selected as output destinations.

Supported destinations:

| Agent | Output path |
| --- | --- |
| Claude | `~/.claude/CLAUDE.md` |
| Codex | `~/.codex/AGENTS.md` |
| Shared agents | `~/.agents/AGENTS.md` |
| DSH | `~/.dsh/AGENTS.md` |

Every selected destination receives the same composition. Run the script again to choose a different set of optional modules or destinations.
