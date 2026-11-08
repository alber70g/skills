# Optimization workflow

## Discover and resume

If a lab exists, read config, results, branch registry, and recent log. Summarize objective, baseline/best, library size, last experiment, active branch, and incomplete phase. For an ambiguous new invocation ask resume or fresh; honor an explicit resume/reset or already-authorized choice. Fresh archives task state, preserving the library. A resumed task continues H and experiment numbering; a different task restarts from H₀.

Ask only for missing settings, in small batches:

- Task description/path, fixed inputs, source materials, and any ordered workflow to preserve.
- Primary success measure and direction; a numeric command or agreed qualitative criteria. Secondary measures optional. Without a verifier, compare observable execution behavior and deliverables against the task; do not fabricate numeric precision.
- Editable component paths and exclusions (default all eight slots, subject to actual host support), immutable constraints, and allowed external effects.
- H₀ location and host adapter: how the runtime loads each supported component, pinned model/settings, tools, environment, and fresh-session invocation.
- Budget `k` (default 1), mode (parallel default, sequential optional), time/cost per probe, and stopping condition (target, maximum executions, or explicit until stopped). Count baseline, both candidate families, compositions, and retries toward total execution/cost caps. Never infer an unlimited paid budget.

Repeat the resolved configuration for confirmation unless it is already authorized in context. A user should approve concrete settings, not an unspecified future experiment. Store them in `.harness2/config.md`; keep private scoring criteria in a controller-only location outside handoff directories.

## Setup and baseline

1. Inspect Git status. Create `research/<task-slug>` from current HEAD, or use an isolated worktree if user changes would overlap. Do not switch or reset a dirty checkout. Register all experiment branches in `branches.md`.
2. Run `lab.py --root <project-root> init`; fill config using the fields above. This creates ignored local logs, library, runs, and base directories. Keep lab evidence centralized if worktrees are used.
3. Map the eight slots to actual files and snapshot the complete H₀ with the snapshot helper. Store the immutable base under `.harness2/base/harness`; remember its path in config. On later tasks reuse this saved base unless the user explicitly changes H₀. Never silently snapshot last task's adopted state as a new base.
4. Commit only permitted harness paths with an explicit path list, recording the resulting SHA. An unchanged baseline may use an existing commit after verifying those paths are clean and tracked. Ignored live harnesses need an in-scope tracked experimental copy that the adapter loads; do not force-add secrets.
5. Execute reference H₀ in a fresh context on fixed inputs. Write trajectory, deliverable, environment/model fingerprint, duration, commit, and any failures under `runs/000/`. Record experiment 0. Store metrics separately in controller-only files and `results.tsv`. Confirm the adapter actually loaded H₀; stop if it did not.

## Task recursion

Read the session contracts before each phase. Save the current reference H, its run, and all candidate parent SHAs.

**Propose:** Prepare a score-free evidence package: original task/materials, reference trajectory/deliverable, current harness, selected library entries, scope/constraints. Create two complete candidate trees per step: invariant improvements and domain improvements. Each editor writes a hypothesis and component diff. Verify scope, immutable guardrails, adapter support, and absence of answer-key memorization; commit before execution.

**Probe:** Run each candidate with the same model, inputs, tools, initial external state, limits, and host adapter as the reference. Reset mutable task state in a sandbox between probes; replay or mock external effects rather than repeating unauthorized live actions. Record trajectories and deliverables. Write contrasts referencing concrete events: reference path/event → candidate path/event → behavior change → consequence → uncertainty. Scores are optional controller bookkeeping, never the contrast supplied to editors.

**Compose:** Give a fresh composer the reference, candidate trees/diffs, observed contrasts, and selected library guidance. It merges, revises, rejects, or preserves each proposed change with evidence pointers. Commit its full successor H′, execute it under matched conditions, and log the result. A composition is a hypothesis until its own execution supports it.

- **Parallel k:** Produce k invariant and k domain candidates from the same H and reference, probe all 2k. Run k independent composers, each seeing the full candidate/contrast pool. Execute all k successors. With the baseline this costs 1 + 3k executions, before retries. Independent sessions can be scheduled serially when simultaneous capacity is unavailable; record scheduling and keep inputs fixed.
- **Sequential k:** Repeat the two-editor, two-probe, one-composer cycle k times. Adopt a supported successor or preserve H after each cycle; the next cycle uses the resulting H and its execution as reference, retaining prior evidence. Total baseline plus 3k executions. Keep the task's H₀ immutable.
- **Selection when k > 1:** Compare final successor deliverables and the reference through a fresh selector using opaque labels, randomized presentation, and no harness identities, metrics, contrasts, or production history. In sequential mode include executed intermediate successors. Keep the label→run/commit mapping controller-only. Resolve ties in favor of the unchanged reference or simpler harness; log reasoning. For k=1 compare the executed successor against the reference directly. Crashed/invalid executions cannot win.

Respect total caps before starting another cycle; stop if insufficient budget remains for its probes and composition. A target reached early can terminate after recording the evidence. Log thought experiments without counting them as real runs.

## Failure and recovery

Use unique branches/worktrees for each candidate so rejection means recording `discard` and returning to the known reference, leaving evidence and commits intact. Do not hard-reset or delete unrelated work. Record crashes/timeouts with an empty metric, not zero. A trivial failure may receive one logged, committed repair within the remaining budget; recurring fundamental failures require a new hypothesis or stopping. Record interrupted runs and finish or explicitly abandon their incomplete phase on resume; never mark an unexecuted composition adopted.

## Reflect and wrap up

After choosing H★, run the reflector with the full score-free execution record and adoption decisions. Separate task-local observations from transferable lessons. Add a library entry only when execution contrasts support a lesson; selecting an output alone is insufficient. Follow the entry schema in operations. If evidence is weak, retain run history and report no new lesson.

Snapshot the complete adopted tree and supporting contrast evidence in the entry; update the library index. Write `summary.md` with baseline → adopted result, measurement limits, component changes, experiment genealogy, failures, library entry/no-entry, and deferred ideas. Update config pointers, branches, and log. Report results concisely and leave the selected commit on its research branch; deploying it into a global/live harness requires the user's scope to include that action.
