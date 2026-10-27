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
