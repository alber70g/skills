# Lab operations

Resolve the helper relative to the installed skill, not the task checkout. Commands below abbreviate its absolute path as `lab.py`. Python 3.9+ and Git are required. Run one controller writer at a time; workers write separate output directories, never shared logs.

```bash
python3 /path/to/harness-2/scripts/lab.py --root /project init
python3 /path/to/harness-2/scripts/lab.py --root /project status
python3 /path/to/harness-2/scripts/lab.py snapshot /project/.harness /project/.harness2/base/harness
python3 /path/to/harness-2/scripts/lab.py guard /project/.harness2/handoffs/editor-01/input
python3 /path/to/harness-2/scripts/lab.py --root /project record --status baseline --commit <sha> --duration 12 --description 'H0 reference; runs/000'
python3 /path/to/harness-2/scripts/lab.py --root /project record --status keep --commit <sha> --parent 0 --duration 10 --metric 4 --description 'Composed successor; runs/003'
python3 /path/to/harness-2/scripts/lab.py --root /project archive
```

The helper records a supplied commit but cannot prove a runtime loaded it. Before each probe, verify all mapped component paths match that SHA and the adapter loads those files. Commit only the explicit permitted paths (`git add -- <paths>` then `git commit`); inspect the staged diff for unrelated content first. Baseline may reuse an unchanged tracked commit. Commit IDs must be available in the controller's repository; worktrees share that object store.

## Files

| Path under `.harness2/` | Contents |
|---|---|
| `config.md` | Agreed settings, component mapping and unavailable slots, adapter, base/current/best commits and paths, next phase, remaining caps. Controller-only. |
| `results.tsv` | experiment, branch, parent, commit, metric, status, duration_s, description. IDs start at 0 and increase; missing measurements stay empty. |
| `log.md` | Hypothesis, changed paths, run/evidence pointers, contrast, decision, duration, insight and next phase per experiment. Helper appends minimal metadata; controller adds the substantive analysis. |
| `branches.md` | Branch/worktree, parent, active/closed, experiments, best result, notes. |
| `parking-lot.md` | Deferred ideas with reasons. |
| `base/harness/` | Immutable H₀ with full supported component tree. |
| `runs/<id>/` | Committed harness pointer, trajectory, deliverable, environment/settings, contrasts; evaluations kept separate from handoffs. |
| `library/index.md` | Entry IDs, dates, task slugs, one-line lessons and relative links. |
| `summary.md` | Adopted result and limitations, changes, history, insights. |

Snapshotting preserves executable file modes and refuses overwrites, symlinks, and recursive copies. For a host spread across locations, assemble a complete tree of the mapped eight components first, plus an adapter mapping; explicitly mark unavailable slots. Do not copy secrets, model weights, or private evaluations. A library snapshot must include the adapter mapping to make later reuse possible.

A conventional mapped tree is:

```text
harness/
  systemprompt.md
  guardrails.md
  LongTermMEMORY.md
  tool_guidance.md
  skills/
  scripts/
  sub_agents/
  plugin/
  adapter.md          # loading/mapping metadata, not a ninth editable component
```

`adapter.md` lists each slot's real host path, activation method and supported/unavailable state. Keep its runtime contract fixed during matched probes. For a project using AGENTS.md, record which parts represent system/tool guidance rather than pretending an additional system prompt can override the host.

## Status

Read config, results, branches, recent log, library index, and parking lot. Show objective, baseline versus adopted best (respect direction; for qualitative results report criteria and uncertainty), number of completed/failed/interrupted runs, latest experiment, active branch and next phase, library size, latest insight, deferred ideas. The helper returns raw config, count, baseline, latest, and entry IDs; the agent synthesizes the remaining files. Do not infer best from the last row or run new experiments.

## Library

- `list`: read index; show ID, date, task and lesson. Missing library means no entries, not a request to initialize one.
- `show <id>`: restrict IDs to existing `entry-NNN` directories; read EXPERIENCE.md and summarize the component tree and supporting contrasts.
- `export <id> <destination>`: copy that entry's harness with `snapshot`; require a nonexisting destination and never silently replace an active harness. Include its adapter mapping. If no destination was provided, ask for it.
- `prune <id>`: describe the exact entries and ask confirmation unless already explicitly authorized. Move selected entries to `library/archive/` and remove their index links; preserve evidence instead of permanently deleting it.

Create monotonically numbered entries, checking archived IDs too:

```text
library/entry-001/
  harness/            # complete adopted tree, including adapter mapping
  evidence/           # minimal self-contained, score-free contrasts and artifacts
  EXPERIENCE.md
```

EXPERIENCE.md records task/date, applicable situation, observed deficiency, intervention, observed consequence, supporting relative evidence paths, limitations, and conditions for reuse. Check all evidence links. Do not claim cross-task transfer until a second task demonstrates it. Update index only after snapshot and evidence are complete. No supported lesson means no entry; log the reason.

## Reset / fresh task

Explicit reset authorizes archival. For an ambiguous resume/fresh choice get the choice first. `archive` moves the entire lab to a unique ignored `.harness2.bak.<UTC>/` and initializes fresh logs while copying library and immutable base forward. It never checks out or resets Git. Record the archive path, restore H₀ through a new isolated research branch/worktree, and redo discovery for the new task. Existing archives retain their original evidence. Never use `git clean -x` against this project.
