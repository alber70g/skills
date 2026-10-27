---
name: compact-for-task
description: Write a /compact command with keep and drop lists for the next task. Use this when the user asks you to start a new bigger task or when the user explicitly asks to create a compaction prompt
argument-hint: <next task>
---

The next task is: $ARGUMENTS

We need to compact first. Write one /compact command for me to run,
in a single code block, in this form:

/compact Keep: ... Drop: ...

- Keep: what the next task needs: the goal, specand file paths,
  decisions made, constraints, progress so far, open questions.
- Drop: what the next task doesn't need: stale logs and test output,
  abandoned approaches, tangents we finished, large file contents.
- End the instructions with: "Next task after compaction: $ARGUMENTS"

Do not start the next task. Do not change files.

Next to the compact command, you write the next prompt that the user can execute based on the next task.

