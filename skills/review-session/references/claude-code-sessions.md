---
description: How to run /review-session on a Claude Code session. Covers transcript location, correction signals, skill locations and saving.
connections: [six-questions, example-format, tracking]
---

# Reviewing Claude Code sessions

Read this only when the user says the session being reviewed is a Claude Code session. It replaces the Grok paths, the gcsfuse save step and the validator path in `SKILL.md`. Every other step in `SKILL.md` stays the same. See [[six-questions]] for the audit and [[example-format]] for examples.

## Path mapping

| Grok | Claude Code |
|---|---|
| `.grok/skills/<name>/` | `~/.claude/skills/<name>/` (user) or `<repo>/.claude/skills/<name>/` (project) |
| `/usr/share/grok/bundled-skills/` (read-only) | Plugin skills under `~/.claude/plugins/` and third-party skills installed with `npx skills` (do not edit) |
| `.grok/skills/usage.log` | Not used. Step 4b records with `scripts/stats.py`; see [[tracking]]. |
| gcsfuse auto-save | None. Files are local; commit them yourself. |
| `validate-skill.py` path | `~/.claude/skills/review-session/scripts/validate-skill.py` |

## Step 1: Find the transcript

- If the session being reviewed is the current one and it wasn't compacted, use the conversation in context.
- If it was compacted, or it's a past session, read the JSONL file:
  - Folder: `~/.claude/projects/$(pwd | sed 's/[^A-Za-z0-9]/-/g')/`
  - Newest session: `ls -t <folder>/*.jsonl | head -1`. Previous session: `sed -n 2p` instead of `head -1`.
  - The session ID for `stats.py session --session-id` is the file name without `.jsonl`.
  - A file that starts with "This session is being continued from a previous conversation" has its earlier messages in an older `.jsonl` in the same folder.
- Count these as corrections in the trace table, in addition to explicit corrections:
  - `[Request interrupted by user]` and `[Request interrupted by user for tool use]`
  - "The user doesn't want to proceed with this tool use" (a denied tool call)
- Skip messages inside `<local-command-caveat>`.

## Step 3: Pick where the fix goes

Not every fix belongs in a skill:

| Cause | Target |
|---|---|
| Behaviour rule for all projects | `~/.claude/CLAUDE.md` |
| Rule for one project | `<repo>/CLAUDE.md` |
| User preference not tied to a skill | Feedback memory file plus a line in `MEMORY.md` |
| Same permission prompt repeated | `settings.json` permissions |
| "Every time X, do Y" | Hook in `settings.json` |

Before editing a skill, run `ls -la ~/.claude/skills/<name>`:
- **It links to `~/.agents/skills/`:** look up `sourceUrl` in `~/.agents/.skill-lock.json`.
  - Your own repo: edit in a clone of that repo, commit, then run `npx skills update <name>`.
  - Anyone else's repo: don't edit it, because `npx skills update` overwrites the change. Use a memory or CLAUDE.md instead.
- **Plugin skill:** read-only. Same rule as a third-party skill.

Frontmatter: don't set `user-invocable: false`. In Claude Code it hides the skill from the `/` menu.

## Step 4: Validate

Run the validator only on skills that have `evals/`. `--all` fails on every skill without it. `CHANGELOG.md` is optional. Claude Code has no tool that runs `evals.json`, so treat those cases as a written spec.

## Step 5: Save

- Skill repo: commit on a branch. Ask before pushing.
- Memory files and `~/.claude/CLAUDE.md`: saved as soon as they're written. No commit needed.
