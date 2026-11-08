# Session contracts

Use fresh contexts with minimal instructions plus file paths. Do not fork the controller's score-bearing conversation. Each role receives a dedicated `input/` directory and writes to a separate `output/`; review copied evidence and run the evidence guard before handoff. Do not hand over the project root, lab root, config, results.tsv, or entire run directories containing scoring files. If the runtime cannot restrict filesystem access, the guard provides an input audit only: do not claim an information barrier. Remove mounts/access to private evaluators where the host supports it.

The controller constructs an allowlist of relevant artifacts, reviews their content for leaked evaluations and hidden answers, and copies only those files. The helper rejects suspicious filenames, score/rubric field labels, and symlinks; it cannot detect every semantic leak. Public task requirements belong in task.md; private scoring rubrics do not. Do not rename a rubric to evade the guard. Exclude or redact it and preserve the original privately.

## Invariant editor

Session instruction (supply concrete absolute paths for INPUT and OUTPUT):

> Read INPUT/task.md, scope.md, adapter.md, harness/, reference/, and selected library/. Improve general agent behavior: planning, tools, context, delegation, verification, or recovery. Preserve the frozen model, permissions, task inputs, and immutable constraints. Write a complete executable candidate to OUTPUT/harness/ and proposal.md listing each changed component, the observed deficiency, predicted behavioral change, and evidence paths. Reuse library ideas only when applicable. Do not execute the task or read controller/evaluation artifacts.

## Domain editor

> Read the same input artifacts. Improve task-specific procedures or knowledge grounded in the supplied source materials. Write a complete candidate harness and proposal.md with changed components, hypothesis, supporting evidence, and applicability. Preserve model, permissions, and input task. Do not embed hidden answers, scores, or unverified domain facts. Do not execute the task.

## Probe executor

> Load only the committed candidate through INPUT/adapter.md and execute INPUT/task.md on INPUT/materials/ in a fresh context. Follow its ordered workflow, constraints, and limits. Write OUTPUT/deliverable and trajectory.md recording actions, tool results, failures, and verification evidence. Do not inspect reference runs, proposals, improvement history, library lessons outside the loaded harness, or evaluations. Do not edit the harness during execution.

The controller enforces supported timeouts/cost limits and records model/environment/commit metadata. An executor's self-report is not a reliable cost cap; use host limits or supervise accounting and stop at the cap.

## Composer

> Read INPUT/reference/, current-harness/, candidates/, contrasts/, scope.md, adapter.md, task.md, and selected library/. Produce OUTPUT/harness/ as a complete successor. In decisions.md map every accepted, revised, rejected, or preserved candidate change to concrete trajectory/deliverable observations. Distinguish hypotheses from observed consequences. Prefer selective composition over concatenation. Preserve unchanged H when no edit is supported. Do not consume evaluation scores or assume the composition improves until it is probed.

For parallel recursion, each composer sees the full pool but no other composer's draft.

## Selector

> Read INPUT/task.md, materials/, and deliverables/ with opaque labels. Compare completion, factual support, and compliance with the original request using only these files. Write OUTPUT/selection.md with the chosen label (or tie), reasons tied to deliverable passages and task requirements, and uncertainty. Do not seek harness identities, metrics, reference labels, or production history.

Copy deliverables to neutral filenames; remove producer metadata without altering substantive content. Keep random mapping outside INPUT. Do not let the selector inherit a conversation that reveals identities.

## Reflector

> Read INPUT/task.md, harnesses/, executions/, contrasts/, and decisions/. Write OUTPUT/EXPERIENCE.md only if observed execution contrasts support lessons. Include situation, deficiency, intervention, observed consequence, limitations, transfer conditions, and exact relative evidence paths. Distinguish single-task observations from demonstrated transfer. Otherwise write no-entry.md explaining the evidence gap. Output selection alone does not prove a reusable lesson. Never infer improvement from a metric or preserve unsupported advice.

For a valid lesson, the controller adds the adopted full tree plus a minimal, score-free evidence copy to a new immutable library entry. References must resolve inside that entry, so later lab archives do not break them.
