---
name: harness-2
description: Improve an agent execution harness through contrastive Propose–Probe–Compose experiments and retain evidence-backed lessons across tasks. Use for recursive harness optimization, harness-2 status, or improvement-library management; ordinary task execution alone does not need this skill.
---

# Harness-2

Optimize an editable harness around a frozen model. Run task-level Propose → Probe → Compose, then reflect into a persistent improvement library. This is a practical adaptation of [Harness²](https://arxiv.org/abs/2610.14224), not a bundled benchmark runner.

## Commands

Interpret arguments after `/harness-2` (or `$harness-2` on hosts using skill mentions):

| Arguments | Action / reference |
|---|---|
| `optimize-task <description-or-path>` | Read [workflow.md](references/workflow.md); discover settings, baseline, improve, reflect. |
| `resume` | Read workflow; summarize existing lab and continue its next incomplete phase. Explicit resume needs no further resume question. |
| `status` | Read [operations.md](references/operations.md); report state without executing experiments. |
| `library [list\|show <id>\|export <id> <destination>\|prune <id>]` | Read operations; list by default. |
| `reset` | Read operations; archive current task state while preserving the library. |

If no action is supplied, infer it from the request; ask for the task if none is available. These are agent-interpreted commands, not shell executables or automatic host command registration.

## Invariants

- Every new task starts from the saved base H₀. Adopted harnesses in the library guide selective reuse; they never silently replace H₀.
- Keep the model, inputs, tools, environment, and execution budget matched across reference and candidates. Record unavoidable drift; do not attribute it to harness edits.
- The eight editable component slots are system prompt, guardrails, memory, tool guidance, skills, scripts, subagents, and plugin/hooks. Map them to host files in config. Unavailable slots remain explicitly unavailable; do not invent runtime capabilities or alter higher-priority instructions.
- A tree of files is executable only when a documented host adapter loads it. Verify that adapter with the baseline. Edits outside the permitted components are invalid experiments.
- `.harness2/` is ignored local evidence: preserve it and its archives during Git operations. Never use broad clean or hard-reset commands to discard a candidate; keep rejected commits in isolated experiment branches/worktrees.
- Commit the exact in-scope harness before every real execution, including baseline and composed successors; record its commit and parent. Never stage unrelated user changes. Use isolation when the workspace is dirty.
- Keep scores, private rubrics, evaluator feedback, and answer keys out of editor/composer/reflector inputs. Observable failures and task source material are usable evidence. The selector sees anonymized deliverables and the original task/materials only.
- Probe execution must use fresh contexts. Use host subagents or CLI sessions when available and authorized; otherwise explain the limitation before experiments. Separate role passes in a contaminated conversation do not provide independent probes or blinded selection.
- Continue autonomously within the agreed scope and budget. Ask only for missing required configuration, scope expansion, additional authorization, or a genuine dead end. Give concise progress updates and log decisions.

## Resources

Read [sessions.md](references/sessions.md) when preparing editor, probe, composer, selector, or reflector sessions. Evidence travels through reviewed files in dedicated input directories, not embedded trajectories in prompts.

Use Python 3 standard-library helper [scripts/lab.py](scripts/lab.py) for initialization, append-only logging, snapshots, evidence checks, and archival. See [operations.md](references/operations.md) for syntax and file conventions. It does not launch models or grant filesystem isolation; use the host's supported runtime and permissions.

For a small real-model trial and a second-task transfer check, see [example.md](references/example.md). Report observed outcomes; a larger k does not guarantee improvement.
