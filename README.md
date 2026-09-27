# Skills

A collection of agent skills for Claude Code and other agents, following the [Agent Skills](https://agentskills.io/) spec. Browse and install them with [skills.sh](https://skills.sh/).

- [Skills](#skills)
	- [autoresearch](#autoresearch)
	- [continue-autonomously](#continue-autonomously)
	- [general-guidelines](#general-guidelines)
	- [linkedin-post-formatter](#linkedin-post-formatter)
	- [turn-based-discovery](#turn-based-discovery)

Install skills interactively:

```bash
npx skills@latest add alber70g/skills
# you'll be interactively guided to choose skills to install global or locally
```

## autoresearch

Autonomous experimentation mode: interviews you, sets up a `.lab/` directory, then explores freely — think, test, reflect — until stopped or a target is hit. Works for any domain where results can be measured.

```bash
npx skills@latest add alber70g/skills --skill autoresearch
```

## continue-autonomously

Keeps the agent moving without stopping to ask. Sorts decisions into three tiers: trivial (just decide), load-bearing (log to `DECISIONS.md` and proceed), and high-risk (log and stop).

```bash
npx skills@latest add alber70g/skills --skill continue-autonomously
```

## general-guidelines

Behavioral guidelines to reduce common LLM coding mistakes, derived from Andrej Karpathy's observations: think before coding, keep it simple, make surgical changes, define verifiable success criteria.

```bash
npx skills@latest add alber70g/skills --skill general-guidelines
```

## linkedin-post-formatter

Formats and drafts LinkedIn posts using Unicode bold/italic typography (LinkedIn has no Markdown), visual separators, and engagement-optimized structures.

```bash
npx skills@latest add alber70g/skills --skill linkedin-post-formatter
```

## turn-based-discovery

Replaces prose interrogation with structured multiple-choice questions (via the AskUserQuestion tool) to quickly resolve ambiguity when scoping work.

```bash
npx skills@latest add alber70g/skills --skill turn-based-discovery
```
