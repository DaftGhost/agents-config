# Agent prompt generator

This repository stores shared agent instructions in `.agents/AGENTS.md` and optional modules in `aside/`, including response and writing style rules in `aside/tones/`. Use the interactive generator to replace prompts or merge selected modules into existing agent configuration files.

```bash
./scripts/generate-agent-prompts.sh
```

See [the complete functionality and test reference](scripts/generate-agent-prompts.md) for write modes, destinations, selection rules, section merging, write safeguards, dependencies, and standalone test case specifications.
