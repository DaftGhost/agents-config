# Agent prompt generator

This repository stores the base prompt heading in `.agents/AGENTS.md` and optional instruction modules in `aside/`, including coding guidance in `aside/coding/` and response and writing style rules in `aside/tones/`. Use the interactive generator to replace prompts or merge selected modules into existing agent configuration files.

Select `coding/coding-guideline.md` to include the coding guidelines in a generated prompt.

```bash
./scripts/generate-agent-prompts.sh
```

See [the complete functionality and test reference](scripts/generate-agent-prompts.md) for write modes, destinations, selection rules, section merging, write safeguards, dependencies, and standalone test case specifications.
