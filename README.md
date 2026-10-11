# Skills

A collection of agent skills for Claude Code and other agents, following the [Agent Skills](https://agentskills.io/) spec. Browse and install them with [skills.sh](https://skills.sh/).

- [Skills](#skills)
	- [autoresearch](#autoresearch)
	- [continue-autonomously](#continue-autonomously)
	- [copy-writing-preferences](#copy-writing-preferences)
	- [fsearch](#fsearch)
	- [general-guidelines](#general-guidelines)
	- [linkedin-post-formatter](#linkedin-post-formatter)
	- [notify-user](#notify-user)
	- [turn-based-discovery](#turn-based-discovery)
	- [writing-clearly](#writing-clearly)

Install skills interactively:

```bash
npx skills@latest add alber70g/skills
# you'll be interactively guided to choose skills to install global or locally
bun x skills add alber70g/skills
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

## copy-writing-preferences

Copy-writing preferences as fourteen rules (descriptive titles, no selling or nagging, concrete instead of figurative, only checked facts), plus instructions to make a message sendable, distill a text and match earlier emails to a group. Includes before/after examples for each rule.

```bash
npx skills@latest add alber70g/skills --skill copy-writing-preferences
```

## fsearch

Searches local macOS files with the installed FSearch CLI by fuzzy name, path, indexed contents, symbol definition, size, type, or modification age.

```bash
npx skills@latest add alber70g/skills --skill fsearch
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

## notify-user

Speaks local notifications when a task finishes, work is blocked, or your attention is needed. Includes the macOS notifier and Soprano setup under `references/`.

```bash
npx skills@latest add alber70g/skills --skill notify-user
```

## turn-based-discovery

Replaces prose interrogation with structured multiple-choice questions (via the AskUserQuestion tool) to quickly resolve ambiguity when scoping work.

```bash
npx skills@latest add alber70g/skills --skill turn-based-discovery
```

## writing-clearly

Keeps text written for others plain, concrete and verified: descriptive titles, the reason first, exact commands and numbers instead of figures of speech, and nothing stated that wasn't checked. Comes with a before/after table and a feedback loop that adds each caught slip back into the rules. For rules that apply to every reply, copy them into `CLAUDE.md` or `AGENTS.md`, as the skill explains.

```bash
npx skills@latest add alber70g/skills --skill writing-clearly
```
