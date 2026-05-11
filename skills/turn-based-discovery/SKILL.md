---
name: turn-based-discovery
description: |
  Enforces strict turn-based conversation using the AskUserQuestion tool (the same multiple-choice mechanism used in plan mode). Every exchange asks ONE incremental-discovery question with
  multiple-choice options plus a free-format "Other" escape. Use when scoping work, gathering 
  requirements, debugging unknowns, or any task where the right next step depends on a user decision.
  Triggers: `/turn-based`, `ask me step by step`, `one question at a time`, `discovery mode`, 
  `interview me`.
---

# Turn-Based Discovery

## Purpose

Replace open-ended interrogation and walls-of-questions with a disciplined loop:
**one question → multiple-choice options → free-format escape → branch on the answer.**

The user should never face more than one question at a time, and should always have a way out of the listed options.

## The Hard Rules

1. **One question per turn.** Never bundle. If a topic has two facets, ask the first, branch on the answer, then ask the second.
2. **Always use the `AskUserQuestion` tool.** Never ask in plain prose when you could ask via the tool. The tool auto-adds the free-format "Other" option — do not list "Other" yourself.
3. **2–4 options, each a real, distinct hypothesis.** Not "Yes / No / Maybe". Each option should represent a concrete branch you can actually act on.
4. **Non-leading.** Options must not all point at your preferred answer. If you genuinely have a recommendation, mark it `(Recommended)` and put it first — but the alternatives must be live, not strawmen.
5. **Exploratory, not confirmatory.** Ask to discover, not to confirm what you already assumed. If you find yourself asking "should I do X?", reframe as "which of these directions fits?".
6. **Branch visibly.** After each answer, state in one short sentence what branch you're now on, then ask the next question (or act).

## Question Shape

Each `AskUserQuestion` question must have:

- **`question`** — open-ended phrasing, ends with a question mark. Avoid yes/no framing.
- **`header`** — ≤12 chars, names the decision axis (e.g. "Scope", "Storage", "Trigger").
- **`options`** — 2–4 mutually exclusive, concrete branches. Each with:
  - `label` — 1–5 words, the choice itself.
  - `description` — one line explaining the implication of picking it (what changes downstream).
- **`multiSelect`** — `false` by default. Only `true` when the axes genuinely combine (e.g. "which platforms").

The tool always appends an "Other" choice for free-format input. Never add your own.

## Good vs Bad Examples

### Bad — leading, binary, confirmatory

> Question: "Should I use Postgres for this?"
> Options: "Yes" / "No"

Problem: binary, leading, no discovery. The user can't tell you what they actually want.

### Good — exploratory, branching

> Question: "What does the data look like at steady state?"
> Header: "Data shape"
> Options:
> - "Mostly relational, joins matter" — Postgres or similar; schema upfront.
> - "Document-shaped, schema varies" — document store; flexible writes.
> - "Append-only event stream" — log-structured; replay-friendly.
> - "Small + in-process, no server" — SQLite or a flat file.

Each option opens a different branch. "Other" lets the user say "it's actually time-series telemetry."

### Bad — bundled

> "What language, what framework, and where will it be deployed?"

Problem: three questions. Ask language first, branch, then framework given language, branch, then deployment.

### Good — single axis

> "Which language are we starting from?"
> Then branch: if Python, next question is Python-specific (FastAPI / Django / Flask / script). If TypeScript, next question is TS-specific.

## The Loop

```
1. Identify the next unknown that actually blocks progress.
2. Frame it as ONE question with 2–4 concrete branches.
3. Call AskUserQuestion.
4. On answer:
   - If user picked an option: state the branch in one sentence, then go to 1.
   - If user picked "Other" / free-format: incorporate, then go to 1.
5. Stop when remaining unknowns are low-risk enough to assume — say so and proceed.
```

## When to Stop Asking

- You can name the next concrete action without guessing on anything load-bearing.
- Remaining unknowns are reversible and low-cost.
- The user signals "just go" / "you decide" / "stop asking".

When stopping, state: "I have enough to proceed. I'm assuming X, Y, Z — say stop if any of those are wrong." Then act.

## Anti-Patterns

- **Wall of questions** — listing 5 bullets in prose. Use the tool, one at a time.
- **Fake choices** — options that are all variants of your preferred answer.
- **Trivia questions** — asking about things you could read from the filesystem or infer.
- **Yes/no when a spectrum exists** — almost every "should I" can be reframed as "which of these".
- **Asking after deciding** — if you've already started implementing, don't pretend to ask.
- **Manually adding "Other"** — the tool does this. Adding it yourself wastes an option slot.

## Interaction with Other Modes

- **Plan mode**: this skill complements plan mode — use it to *gather* the inputs that feed the plan. Do not call `ExitPlanMode` from inside this skill; surface the plan separately.
- **Auto mode**: still applies. Auto mode reduces routine confirmations but does not override an explicit user request for turn-based discovery. When this skill is active, ask.
- **Brainstorming skill**: if `brainstorming` is already running, defer to it; it has its own one-question-at-a-time discipline. Don't double-drive.

## Checklist Before Each Question

- [ ] Is this the single most blocking unknown right now?
- [ ] Are the 2–4 options genuinely different branches?
- [ ] Could a reasonable user pick any of them?
- [ ] Is the phrasing open, not leading?
- [ ] Have I left the free-format escape to the tool (not duplicated it)?

If any answer is no, rewrite the question before calling the tool.
