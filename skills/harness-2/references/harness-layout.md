# The Harness Tree

An agent is a **frozen model plus an editable harness**. The harness is a tree of exactly eight
component kinds. `.harness/` in the project root is the canonical, git-tracked tree that
`harness-2` edits; `scripts/h2.py render` installs it into whatever layout the host agent reads.

## Canonical tree

| Path | Component | When it is in context |
|---|---|---|
| `systemprompt.md` | c1 persona and top-level procedure | ALWAYS ON: every token competes with the agent's own output budget |
| `guardrails.md` | c6 standing rules | ALWAYS ON, same cost |
| `LongTermMEMORY.md` | c3 durable domain facts | ALWAYS ON, same cost |
| `tool_guidance.md` | c4 when and how to use each existing tool | ALWAYS ON, same cost |
| `skills/<name>/SKILL.md` (+ `skills/<name>/scripts/*`) | c6 reusable workflow | ON DEMAND, only when invoked; costs nothing otherwise |
| `sub_agents/<name>/AGENT.md` | c5 delegated worker | runs in its OWN context, returns text |
| `scripts/<name>.py` or `.sh` | c7 deterministic helper | run on demand via shell |
| `plugin/hooks.json` (Claude Code, Codex) or `plugin/<name>.ts` (OpenCode) | c8 middleware in the tool loop | always registered, acts INSIDE the tool loop |

Context policy (c2, compaction and context assembly) is owned by the host and is not editable.
Anything outside these paths is off the editable surface: `validate` warns about it and `render`
ignores it.

## The cost model, which decides the FORM of every edit

Always-on prose is the expensive option. Every word is in context on every run, and the most
costly failure is a run that reasons until the budget is gone and produces nothing. Adding prose
makes that more likely. An on-demand component costs nothing until it is invoked. So prefer, in
this order:

1. **A skill** for anything with a recognisable trigger: a procedure for a document type, a
   format, a recurring situation. The default form for new instruction.
2. **A script** for a deterministic operation the runs hand-rolled and got wrong or slow.
3. **A subagent** for a bounded investigation whose input is large and whose answer is small
   (read twelve files, return one table). A bad trade when the output is as big as the input.
4. **A hook or plugin** when a recurring mechanical problem in the tool loop is better handled
   there than in prose. It cannot be ignored and costs no always-on budget: trimming oversized
   tool output, appending a hint after a recurring error signature, verifying a write right
   after it happens, blocking a known-bad call with a reason that teaches the fix.
5. **Always-on text** last, only for a short rule that genuinely applies to every run. If you
   add always-on text, cut something else to pay for it.

## Rules that discard a whole proposal

`scripts/h2.py validate <dir> --host <host>` enforces these before any probe. An invalid tree is
never probed; the proposer gets one retry, then the step inherits the current harness.

1. **Every skill needs a trigger line.** The skill's directory name must appear verbatim in an
   always-on file, in the same edit: `When <situation>, load the \`<name>\` skill.` An unnamed
   skill is never opened; the line is what makes it exist.
2. **Every script you name must ship.** A `scripts/<file>.py` invoked from a SKILL.md or from
   always-on text must exist in the same tree, a skill's own helper at
   `skills/<skill>/scripts/<file>.py`. Python scripts must compile.
3. **Frontmatter.** `SKILL.md` needs `name:` matching the directory and a `description:`.
   `AGENT.md` needs a `description:` (and `mode: subagent` on OpenCode).
4. **The always-on cap** (default 8,000 characters, set in `config.md`). Over the cap, cut.
5. **`plugin/hooks.json`** must be a JSON object with a top-level `hooks` key.

Template braces (`{{`, `{%`) in always-on text only warn, but some hosts render them and crash.

## The deliverable's shape belongs to the request

A harness changes HOW the agent works. It must never change WHAT SHAPE it delivers. Where the
task names fields, columns, sheets, sections or an order, that shape is part of the request. A
component that adds explanatory columns, restates a derivation inside the artifact or renames a
header "for clarity" is changing the deliverable, and a downstream reader keys on exact names
and positions. Guidance that makes reasoning visible belongs in the harness or the trajectory,
never in the artifact. A value the task asks for must be delivered as a value, not a formula,
placeholder or described-but-unperformed calculation.

## Workspace facts versus procedure

Verified facts about THIS workspace are the most valuable thing a harness can encode: the exact
join between two files, which entries have no counterpart, what a field's units are. Write the
fact itself into the relevant component, anchored so a reader can tell fact from procedure
("in this workspace, role X maps to position Y"), and only what the evidence establishes. A
guessed fact is worse than none.

Procedure and structure, by contrast, should be written for the domain, because an adopted
harness enters the library where later tasks read it. Never store this task's facts as
durable memory (`LongTermMEMORY.md`): they are wrong anchors for the next task.

```
workspace fact   "attrition role 'HR' maps to position 'HR Manager'"   verified here, labelled here
procedure        "reconcile role names before joining; list unmatched leftovers"
too generic      "be thorough"                                          changes no behaviour
```

## Host mapping

`scripts/h2.py render --harness .harness --workspace <dir> --host <host>` installs the tree:

| Canonical | `claude` | `codex` | `opencode` | `generic` |
|---|---|---|---|---|
| four always-on files, concatenated | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` |
| `skills/<n>/` | `.claude/skills/<n>/` | `.agents/skills/<n>/` | `.opencode/skills/<n>/` | `skills/<n>/` |
| `sub_agents/<n>/AGENT.md` | `.claude/agents/<n>.md` (adds `name:`) | `sub_agents/<n>/AGENT.md` | `.opencode/agent/<n>.md` (adds `mode: subagent`) | `sub_agents/<n>/AGENT.md` |
| `scripts/` | `scripts/` | `scripts/` | `scripts/` | `scripts/` |
| `plugin/hooks.json` | `hooks` key of `.claude/settings.json` | `.codex/hooks.json` | not loaded | copied verbatim |
| `plugin/<n>.ts` | not loaded | not loaded | `.opencode/plugin/<n>.ts` | copied verbatim |

`hooks.json` uses the Claude Code hook schema: a top-level `hooks` object mapping an event
(`PreToolUse`, `PostToolUse`, `SessionStart`, `Stop`) to matcher entries, each with a `matcher`
and a list of `command` hooks. A hook receives the event as JSON on stdin and can print a JSON
`decision` of `block` with a `reason` that goes back to the model. Keep commands fast and
non-interactive; put real logic in a `scripts/` helper the hook calls.

`scripts/h2.py import --workspace . --harness .harness` builds H₀ from an existing project:
`CLAUDE.md` or `AGENTS.md` becomes `systemprompt.md`, the host's skills, agents, scripts and
hooks move to their canonical paths, and the other always-on files start empty.
