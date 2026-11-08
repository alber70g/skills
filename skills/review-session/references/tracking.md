---
description: Where /review-session stores statistics per review, how to record them with scripts/stats.py, and how past statistics change the next change plan.
connections: [six-questions, claude-code-sessions]
---

# Review statistics

Every record is stored in the project the reviewed session worked on. That includes findings about a skill: a skill's history belongs to the project it was applied to, and skill folders stay free of records. The next review in the same project finds the history, and a fix that didn't stick shows up. The helper is `scripts/stats.py` in this skill's folder. It uses only the Python 3 standard library and makes no Git commits. See [[six-questions]] for the Q numbers and [[claude-code-sessions]] for finding the session ID.

## Where records go

All files are in `<project>/.review-session/`. `<project>` is `--project` if given, else the Git root of the current directory, else the current directory. For a past session in another directory, pass `--project`.

| Record | File | Distinguished by |
|---|---|---|
| The review itself: agent, session ID, session working directory, message count, mistake score, skills used | `sessions.tsv` | One row per review |
| A finding about a skill (its SKILL.md, references, evals or scripts) | `findings.tsv` | `target=skill`, `skill=<name>` |
| A skill's usage outcome (success, partial, failed) | `findings.tsv` | `kind=usage`, `skill=<name>` |
| A finding about CLAUDE.md, AGENTS.md, memory, settings, hooks or other project files, or a mistake with no file to fix | `findings.tsv` | `target=claude-md`, `agents-md`, `memory`, `settings`, `hook`, `other` or `none`; `skill` empty |

- `.review-session/` contains its own `.gitignore` (`*`), so it stays local without editing the project's `.gitignore`.
- The record goes to the project. The fix itself still goes where it takes effect: the skill's source `SKILL.md`, the CLAUDE.md, the memory file.

**Readable log of the change.** If the project already has a `WORKLOG.md` or `CHANGELOG.md`, add one dated line there describing what changed. If it has neither, don't create one.

## Commands

```bash
S=<this skill>/scripts/stats.py

# 1. Before the change plan (Step 2): read history
python3 $S --project <project> status

# 2. Step 4b: record the review; prints REVIEW_ID
python3 $S --project <project> session --agent claude-code --session-id <id> \
  --session-cwd <session working directory> --messages 42 --mistake-score 3 --skills commit,build

# 3. One row per change-plan row
python3 $S --project <project> finding --review-id <REVIEW_ID> --target skill --skill commit \
  --file SKILL.md --q 1 --action TUNE --eval-added yes --note "add branch check before commit"
python3 $S --project <project> finding --review-id <REVIEW_ID> --target claude-md --file CLAUDE.md \
  --action TUNE --note "read callers before editing exports"

# 4. One row per skill used
python3 $S --project <project> usage --review-id <REVIEW_ID> --skill commit --outcome partial --note "missed branch check"
```

Actions: `TUNE`, `GROW`, `RETIRE`, `NONE`. A Grok session without a known session ID uses `--session-id unknown`.

## How past statistics change the change plan

`status` prints JSON with `instructions` (findings without a skill) and `skills` (one summary per skill name). Apply these rules in Step 2, before writing the change plan:

| Status field | Meaning | Rule |
|---|---|---|
| `repeat_tunes` lists a file | The file was tuned in 2 or more reviews and the mistake came back | Don't patch it again. Rewrite the whole section, or enforce the rule another way: an eval, a script, or a hook for "every time X". |
| `tunes_without_eval` is not empty | An earlier TUNE has no regression eval | Add the missing eval in this review. |
| `mistake_scores` not falling over 5+ reviews | Fixes aren't reaching the cause | Check that fixes land where the agent reads them: top of the section, the right CLAUDE.md, not an installed copy. |
| `usage` has mostly `failed` or `partial` for a skill | The skill isn't helping in this project | Consider Q7: retire it, or tune it heavily. |
| `by_target` shows many `none` findings | Mistakes with no file to fix | Look for a missing CLAUDE.md rule or a missing skill. |
