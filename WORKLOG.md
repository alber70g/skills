# Work Log

## 2026-10-09

- Reviewed all seven `SKILL.md` files; two exceeded 150 lines before editing.
- Added tables of contents after the titles in `skills/autoresearch/SKILL.md` and `skills/linkedin-post-formatter/SKILL.md`, preserving frontmatter and existing content.
- Verified that all 28 contents links match the section headings, excluding fenced examples; `git diff --check` passed.
- No remaining work.

- Added fsearch to the README contents and skill list, including its description and install command. Preserved existing README edits and CRLF line endings; verified the section anchor and `git -c core.whitespace=cr-at-eol diff --check`.

## general-guidelines: research/ and docs/ documents

- Added section 6 to `skills/general-guidelines/SKILL.md`: research excerpts (own work or Tavily/Exa, with sources) go in `research/`, plans for user review go in `docs/`; check `research/` before new research and reference new documents from WORKLOG.md. Extended the frontmatter description to mention both folders.
- Verified `git diff --check`; skill stays under 100 lines, so no table of contents needed. README unchanged. Committed and pushed to master.

## expert-opinion skill

- Added `skills/expert-opinion/SKILL.md` from user-supplied prompt text: meeting content via `$ARGUMENTS`, asks for it when missing. Fixed output headings: one H1 and seven sections. Added README contents link and section.

## review-session skill

- Copied the Grok bundled postmortem skill from `~/Downloads/bundled__postmortem` to `skills/review-session/` and renamed it to `review-session` (frontmatter, title, evals, triggers, references). The source no longer had `CHANGELOG.md` or `BUILD.bazel` when it was copied.
- Removed `user-invocable: false` so `/review-session` shows in the Claude Code `/` menu. Fixed the evals to match the skill's 7 questions. Removed the changelog step (old Step 4) and renumbered: Step 4 validate, 4b usage log, 5 verify saved.
- Added "Which agent ran the session (ask first)" to `SKILL.md`, plus `references/claude-code-sessions.md`, which is read only for Claude Code sessions. Added two evals for it. Added a README section.
- `CHANGELOG.md` left out, matching the other skills; `validate-skill.py` no longer requires it. Validator passes.
- Checklist: Step 4 now includes the re-read and eval check; Step 4b is the usage log entry, matching the Step 4b section.
- Statistics: added `scripts/stats.py` (standard library) with `session`, `finding`, `usage` and `status`. All records, including skill findings and usage, go to `<project>/.review-session/` (self-ignoring); `<project>` defaults to the Git root of the current directory. Nothing is written into skill folders. `status` reports instruction findings and one summary per skill, and flags files tuned in 2+ reviews and TUNEs without eval. Replaces the Grok `usage.log` in Step 4b. Rules in `references/tracking.md`. 5 tests in `tests/test_stats.py` pass; 2 of them fail against a copy with the project-root default and repeat threshold broken.
