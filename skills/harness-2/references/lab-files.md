# Lab Files

`.harness2/` is the untracked, local source of truth for the whole improvement record. Git
tracks `.harness/` (the harness under test); `.harness2/` tracks what was learned. They are
independent. `scripts/h2.py init --slug <slug>` creates everything below except `config.md`
and adds `.harness2/`, `run.log` and `.harness2.bak.*/` to `.gitignore`.

```
.harness2/
  config.md          objective, task, metric, scope, constraints, host, executor, k, mode, termination
  results.tsv        one row per experiment
  log.md             narrative log, one heading per experiment
  branches.md        branch registry
  parking-lot.md     deferred ideas with the evidence that suggested them
  summary.md         written at wrap-up
  library/           the improvement library (harnessing-level recursion), see below
  runs/              per-step evidence: trajectories, deliverables, candidate trees, contexts
```

## `config.md`

Write it from the interview, one `- Key: value` line per field so `h2.py status` can read it.

```markdown
# harness-2 config — <slug>

- Objective: <one line: the task whose harness we improve, and what better means>
- Task file: <path to the task instructions, copied to .harness2/runs/task.md>
- Source material: <path or "none">
- Deliverable word: <e.g. report, workbook, summary>   (used in mission prompts)
- Domain word: <e.g. meeting processing, code review>   (used in mission prompts and the library)
- Primary metric: <name> | <command that prints a number, or "rubric", or "none (blind selection)">
- Direction: higher | lower
- Secondary metrics: <name=command, ...> or none
- Scope: <components that may be edited; default all eight> ; off-limits: <...>
- Constraints: <never touch production data, max cost per probe, ...>
- Host: claude | codex | opencode | generic
- Executor: subagent | <shell command template with [[workspace]] [[task]] [[trajectory]]>
- Probe budget: <wall-clock minutes per probe, default 10>
- Always-on cap: <chars, default 8000>
- Base harness: .harness (origin: imported from <...> | supplied at <...> | empty)
- Base commit: <sha>
- k: <1..5>
- Mode: parallel | sequential
- Termination: <target metric value | N steps | until stopped>
- Baseline: <filled after experiment #0>
- Best: <updated on every keep>

## Rubric (only when the primary metric is qualitative)
| Criterion | Definition | Weight |
|---|---|---|
...
Composite = sum(score × weight) on a 1–10 scale. The rubric is scored by the orchestrator only;
it is NEVER copied into an evidence directory.
```

## `results.tsv`

Tab-separated columns: `experiment`, `branch`, `parent`, `commit`, `metric`,
`secondary_metrics`, `status`, `duration_s`, `description`. Append with
`scripts/h2.py log --experiment N --branch B --parent P --commit C --metric M --status S --duration D --description "..."`.

Status values:

| Status | Meaning |
|---|---|
| `base` | reference execution of H₀ (experiment #0, or the first of k replicates) |
| `probe` | a candidate or checkpoint rollout; metric is `-` because probes are not scored |
| `keep` | a composed successor measured better than the current reference, or chosen by blind selection |
| `keep*` | primary improved but a secondary regressed; trade-off logged |
| `discard` | measured equal or worse; `.harness/` restored to the reference commit |
| `interesting` | not better, but the contrast revealed something; kept or reverted, your call |
| `crash` | probe or session failed; metric `0` |
| `thought` | a thought experiment, no execution |

## `log.md` entry format

```markdown
## Experiment N — <title>
- Branch: research/<slug>   Type: base|probe|compose|select|reflect|thought   Parent: #M
- Commit: <sha>   Stage: propose INV-1 | propose DOM-1 | compose agg1 | checkpoint c2 | select | reflect
- Hypothesis: <what this harness edit should change in behaviour, and why the evidence says so>
- Changes: <component diffs, from h2.py diff>
- Contrast: <behavioural differences versus the reference: tool use, planning, verification, output shape, failures, delivered or not>
- Result: <metric, or "not scored (probe)">   Duration: <s>   Status: <status>
- Insight: <one line that a later step can act on>
```

## `runs/` layout

```
.harness2/runs/
  task.md                        the task instructions, verbatim
  source/                        source material the task is done from (copied or symlinked)
  step-01/
    base-1/  base-2/ ...         k reference rollouts of H₀: workspace/, trajectory.md, produced.md, deliverables/
    INV-1/ DOM-1/ ...            candidates: harness/, workspace/, trajectory.md, produced.md, deliverables/, contrast.md
    agg1/ ... | c1/ ...          finals (parallel compositions or sequential checkpoints), same layout
    ctx/<stage>/                 the evidence directory handed to each session (MISSION.md + context/)
    selection/id_map.json        anonymous id -> label, kept OUTSIDE any context directory
    reflection/                  edits.md and the experience block
```

## Library layout

```
.harness2/library/
  INDEX.md                       generated by `h2.py library index`; one block per entry with cue and lesson
  entry-001/
    harness/                     full adopted tree, validated before storing
    EXPERIENCE.md                header (task, date, commit, components) + "What each edit did" + "Transferable lesson"
```

`h2.py library add --task-slug <slug> --harness .harness --experience <file> --commit <sha>`
refuses a tree that fails validation and an experience file that mentions grading material.
`list`, `show <id>`, `export <id> --to <dir>` and `prune <id>` are the inspection commands.

## `branches.md`

`| Branch | Forked from | Status | Experiments | Best metric | Notes |`. Fork
(`git checkout <commit> && git checkout -b research/<new-slug>`) when a fundamentally different
harness direction deserves its own line of history; mark exhausted branches `closed`.
