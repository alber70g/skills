# Source map

Reviewed 2026-09-04. Prefer the current checked-out DeepSeek Harness source/types when available because the project evolves quickly.

## Agent Skills format

- Specification: https://agentskills.io/specification

Key design principle used by this skill: progressive disclosure. Keep startup metadata small, keep `SKILL.md` focused, and load `references/`, `scripts/`, and `assets/` only when needed.

## Cordis mental model and tutorial

- Cordis primer: https://deepseek-harness.github.io/deepseek-harness/en/reference/cordis-primer
- Cordis tutorial overview: https://deepseek-harness.github.io/deepseek-harness/en/develop/cordis-tutorial/
- Lifecycle and effects tutorial: https://deepseek-harness.github.io/deepseek-harness/en/develop/cordis-tutorial/02-lifecycle-and-effects
- Services tutorial: https://deepseek-harness.github.io/deepseek-harness/en/develop/cordis-tutorial/03-services
- Events tutorial: https://deepseek-harness.github.io/deepseek-harness/en/develop/cordis-tutorial/04-events
- Composition and HMR tutorial: https://deepseek-harness.github.io/deepseek-harness/en/develop/cordis-tutorial/06-composition-and-hmr
- Into the harness tutorial: https://deepseek-harness.github.io/deepseek-harness/en/develop/cordis-tutorial/07-into-the-harness

## DeepSeek Harness official development documentation

- Your first Harness plugin: https://deepseek-harness.github.io/deepseek-harness/en/develop/basic/
- Build a tool: https://deepseek-harness.github.io/deepseek-harness/en/develop/basic/tool
- Plugin configuration: https://deepseek-harness.github.io/deepseek-harness/en/develop/basic/config
- Package and install: https://deepseek-harness.github.io/deepseek-harness/en/develop/basic/publish
- Plugin lifecycle: https://deepseek-harness.github.io/deepseek-harness/en/develop/framework/
- Services and dependencies: https://deepseek-harness.github.io/deepseek-harness/en/develop/framework/service
- Event system: https://deepseek-harness.github.io/deepseek-harness/en/develop/framework/events
- Three-role capability design: https://deepseek-harness.github.io/deepseek-harness/en/develop/practice/
- Runtime Cordis tools: https://deepseek-harness.github.io/deepseek-harness/en/develop/practice/dynamic-cordis
- Tool authoring reference: https://deepseek-harness.github.io/deepseek-harness/en/reference/cookbook/adding-a-tool
- Architecture/reference root: https://deepseek-harness.github.io/deepseek-harness/en/reference/

## Source repository

- https://github.com/deepseek-ai/deepseek-harness

When exact service/event/tool/Fiber signatures are needed, inspect generated `cordis-surface` reference regions and the owning TypeScript package in the current checkout rather than copying an old static list.
