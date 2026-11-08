---
name: review-session
description: "Review a finished or ongoing session: trace user corrections, then tune skills, grow references and evals so the same mistakes do not repeat. Use on /review-session, 'postmortem', 'what did we learn', 'session retrospective', or before /compact or the end of a substantial session."
type: workflow
lifecycle: active
capabilities: [session-tracing, skill-auditing, eval-generation, skill-tuning, fitness-logging]
depends_on: []
inputs: [session-transcript]
outputs: [skill-changes, evals, fitness-log]
category: meta/learning
---

# /review-session — Session Learning Engine

**Run after EVERY session.** This is how skills get smarter over time. A session without a review is wasted — the same mistakes will repeat forever.

**When to run**: (1) `/review-session`, (2) end of any substantial session, (3) user says "what did we learn?", (4) before the session ends (automatically prompted)

### Which agent ran the session (ask first)

The user must state which agent ran the session under review. If they haven't, ask before Step 1: "Is this review for a Claude Code session or a Grok session?"

| Session ran in | Instructions |
|---|---|
| Claude Code | Read `references/claude-code-sessions.md` first. It replaces the `.grok/` paths, the gcsfuse save step and the validator path below. |
| Grok | Follow this file as written. |

- [/review-session — Session Learning Engine](#review-session--session-learning-engine)
    - [Which agent ran the session (ask first)](#which-agent-ran-the-session-ask-first)
    - [Quick vs Full Review](#quick-vs-full-review)
  - [Step 1: Trace the Conversation](#step-1-trace-the-conversation)
  - [Step 2: Audit Each Skill (7 Questions)](#step-2-audit-each-skill-7-questions)
  - [Step 3: Apply Every Change](#step-3-apply-every-change)
    - [TUNE (editing SKILL.md)](#tune-editing-skillmd)
    - [GROW files](#grow-files)
    - [NEW SKILL (same pattern 3+ times)](#new-skill-same-pattern-3-times)
  - [Step 4: Validate Changes](#step-4-validate-changes)
  - [Step 4b: Log Skill Usage (Fitness Tracking)](#step-4b-log-skill-usage-fitness-tracking)
  - [Step 5: Verify Changes Are Saved](#step-5-verify-changes-are-saved)
  - [Anti-Patterns (things that make session reviews useless)](#anti-patterns-things-that-make-session-reviews-useless)
  - [Tracking Improvement Over Time](#tracking-improvement-over-time)
  - [Checklist (copy-paste to verify)](#checklist-copy-paste-to-verify)


### Quick vs Full Review

| Session type | Review depth |
|---|---|
| Config change, quick fix (<10 messages) | **Quick**: Steps 1-2 only. If mistake score = 0 and no growth, skip to Step 5 with a one-line summary |
| Normal session (10-50 messages) | **Full**: All 5 steps |
| Major session (50+ messages, oncall, multi-PR) | **Full + deep**: All 5 steps, check AGENTS.md trigger table too |

---

## Step 1: Trace the Conversation

Read the **entire** conversation. For every user correction, repeated instruction, or wasted loop:

```markdown
| # | What I Did Wrong | What User Said | Root Cause | Skill Fix |
|---|-----------------|----------------|------------|-----------|
| 1 | Committed to main | "NEVER commit to main" | Didn't check branch | commit: add branch check |
| 2 | Guessed file path | "read the file first" | Skipped discovery | build: enforce read-before-edit |
```

**Rules:**
- User said something **twice** → 2 rows (first correction failed)
- Went down wrong path for 3+ messages → 1 row even without explicit correction
- Count rows = session **mistake score**

**If mistake score = 0**: Great session! Still proceed to Step 2 — zero mistakes doesn't mean zero learning. Check Q2-Q6 for growth opportunities (new knowledge, reusable solutions, trigger phrases).

---

## Step 2: Audit Each Skill (7 Questions)

For **every skill used** (or that should have been used):

| # | Question | If YES → Action |
|---|----------|-----------------|
| 1 | Did the instructions lead me wrong or miss a step? | **TUNE** SKILL.md — fix the instruction |
| 2 | Did I learn something not documented? | **GROW** `references/` — create `references/what-i-learned.md` |
| 3 | Did I solve a problem worth saving? | **GROW** `examples/` — save request + solution + gotcha |
| 4 | Did I write code I'll need again? | **GROW** `scripts/` — extract and parameterize |
| 5 | Did I discover a new trigger phrase? | **GROW** `evals/triggers.json` — add trigger |
| 6 | Did I find a failure mode to test for? | **GROW** `evals/evals.json` — add test case |
| 7 | Did the skill make things WORSE or not help at all? | **RETIRE** — move to `_retired/` if dead weight |

**Read past statistics first.** Run `scripts/stats.py status` for the project the session worked on (see `references/tracking.md`). It reports CLAUDE.md and other instruction findings, plus one summary per skill used in that project. If a file appears in `repeat_tunes`, don't patch it again: rewrite the section or enforce the rule with an eval, script or hook. Add any eval listed in `tunes_without_eval`.

Produce the **change plan** (do NOT skip this table):

```markdown
| Skill | Q# | Action | File | Change |
|-------|----|--------|------|--------|
| voice-oncall | 1 | TUNE | SKILL.md | Add "check env vars on pods" step |
| axiom | 3 | GROW | examples/voice-clone-debug.md | Axiom query for clone errors |
| build | 6 | GROW | evals/evals.json | Test: must read files before editing |
```

---

## Step 3: Apply Every Change

### TUNE (editing SKILL.md)
1. Read the current SKILL.md fully
2. **Rewrite the section** to be correct — do NOT just append a note
3. If adding a rule, put it where the agent will see it (top of section, not bottom)

### GROW files

**`examples/`** format:
```markdown
# [Title]
## User Request
"the exact thing the user asked"
## Solution
[working code/query/command]
## Key Gotcha
[the non-obvious thing]
## Date
YYYY-MM-DD
```

**`references/`** — explain concept, cite `file:line` or PR numbers.
**When adding a new reference, add it as a graph node:**
1. Add YAML frontmatter: `description` (one-line) + `connections` (related nodes)
2. Weave `[[wikilinks]]` to related nodes in prose
3. Update `references/INDEX.md` (create if missing and skill has 3+ refs)
4. Add backlinks from related nodes to the new one

**`evals/evals.json`** — add to the `test_cases` array:
```json
{
  "name": "descriptive_test_name",
  "input": "what the user would say",
  "assertions": ["what agent must do", "what it must NOT do"]
}
```

**`evals/triggers.json`** — add to `test_cases`:
```json
{"input": "new trigger phrase", "should_trigger": true}
```

### NEW SKILL (same pattern 3+ times)

Use `skill-creator` skill for full guidance. Quick checklist:
1. Create `.grok/skills/new-skill-name/`
2. Write `SKILL.md` with frontmatter:
   ```yaml
   ---
   name: new-skill-name
   description: "What it does. Use when X, Y, Z."
   type: workflow  # knowledge | workflow | orchestrator | tool
   lifecycle: active
   ---
   ```
3. Create `evals/evals.json` (3+ tests), `evals/triggers.json` (3+ triggers)

---

## Step 4: Validate Changes

Run the validator on **every skill you touched**:

```bash
# Validate a single skill
python3 /usr/share/grok/bundled-skills/bundled__postmortem/scripts/validate-skill.py .grok/skills/<skill-name>

# Validate ALL skills (catches collateral damage)
python3 /usr/share/grok/bundled-skills/bundled__postmortem/scripts/validate-skill.py --all .grok/skills/
```

**The validator enforces:**
- All required files exist (SKILL.md, evals/evals.json, evals/triggers.json)
- Frontmatter has name (matches dir), quoted description, type, lifecycle
- evals.json has ≥3 test cases in `{skill, test_cases}` format, no TODOs
- triggers.json has ≥3 triggers with ≥1 negative, in `{skill, test_cases}` format
- No nested duplicate directories, SKILL.md body < 500 lines

**If validation fails, fix before ending the session.** Do NOT skip this step.

Then verify manually:
1. **Re-read the SKILL.md** you tuned — does it read correctly end-to-end?
2. **Check trigger coverage** — would the user's exact phrasing from Step 1 now trigger the right skill?
3. **Check eval coverage** — every Q1 TUNE must have a matching Q6 regression eval

---

## Step 4b: Record the Review (Statistics)

**Before ending, record the review with `scripts/stats.py`** (commands and routing in `references/tracking.md`):

All records go to `<project>/.review-session/` in the project the session worked on, including findings about skills. Nothing is written into skill folders.

1. `session`: one row for the review. It prints the review ID.
2. `finding`: one row per change-plan row. Skill findings use `--target skill --skill <name>`. CLAUDE.md, AGENTS.md, memory, settings and hook findings use their own target.
3. `usage`: one row per skill used, with outcome `success`, `partial` or `failed`.
4. If the project already has a `WORKLOG.md` or `CHANGELOG.md`, add one dated line describing the change. Don't create one.

**Over time this shows which skills and instructions work, and which fixes didn't stick.**

---

## Step 5: Verify Changes Are Saved

**All skill changes are saved automatically when the session ends.**

The `.grok/` directory is backed by gcsfuse — any files written there persist to GCS automatically. Next session restores them.

**Your job in this step:** verify the changes look correct.

```bash
# List your mutable skills (bundled skills live read-only under
# /usr/share/grok/bundled-skills/, not here)
ls -la .grok/skills/

# Verify your new/edited skill has the right content
cat .grok/skills/<skill-name>/SKILL.md
```

---

## Anti-Patterns (things that make session reviews useless)

| Anti-Pattern | Why It Fails | Do This Instead |
|---|---|---|
| Skip the review | Next session repeats the same mistakes | Run /review-session every session. No exceptions. |
| Write stub evals | `"assertions": ["works correctly"]` tests nothing | Write specific assertions: what input → what behavior |
| Append to SKILL.md bottom | Agent reads top-down, may never reach the fix | Rewrite the relevant section in-place |
| Tune SKILL.md without eval | Same bug will recur — nothing prevents regression | Every TUNE gets a matching eval in Q6 |
| Only audit skills you used | Misses skills you SHOULD have used but didn't | Check Step 1's "Skill Fix" column — some fixes target skills not loaded |
| Create new skill for 1 instance | Over-engineering. New skill = 3+ repetitions minimum | Add to existing skill's references/ or examples/ instead |

## Tracking Improvement Over Time

After 5+ reviewed sessions, check trends:

```bash
# Trends for this project: instruction findings plus one summary per skill
python3 <this skill>/scripts/stats.py status

# Count user-created skills (bundled skills are read-only under
# /usr/share/grok/bundled-skills/ and never appear here)
ls -d .grok/skills/*/ | wc -l
```

**Healthy signs:**
- Mistake scores trending down over time
- Fewer Q1 TUNEs (skills getting accurate), more Q2-Q3 GROWs (skills getting richer)
- New skills being created from Q4 patterns (3+ repetitions → extract)

**Unhealthy signs:**
- Same skill getting Q1-tuned repeatedly (`repeat_tunes` in `status`) → the TUNE isn't sticking. Rewrite the whole section, don't patch.
- Mistake score not decreasing → evals are missing. Every TUNE needs a regression eval (Q6).

---

## Checklist (copy-paste to verify)

- [ ] Step 1: Traced all corrections (mistake score: ___)
- [ ] Step 2: Read `stats.py status`, audited all skills with 7 questions, produced change plan
- [ ] Step 3: Applied all TUNE/GROW changes
- [ ] Step 4: Ran `validate-skill.py` — 0 errors on all touched skills; re-read tuned SKILL.md, every TUNE has matching eval
- [ ] Step 4b: Recorded session, findings and skill usage with `stats.py` in `<project>/.review-session/`; added a line to the project's existing CHANGELOG.md or WORKLOG.md
- [ ] Step 5: Verified changes look correct (`ls .grok/skills/`, checked new files)
