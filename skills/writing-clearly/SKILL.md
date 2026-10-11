---
name: writing-clearly
description: |
  Keeps any text written for someone else plain, concrete and verified, so the reader gets the
  point at first read: replies to the user, documentation, slides, website and UI copy, emails,
  commit messages, spoken notifications. Use when drafting, editing or reviewing copy, titles,
  headings, slide decks, pages or labels, when the user asks for clearer or less vague wording,
  or when the user points out a vague or guessed phrase.
---

# Writing Clearly

The reader should get the point at first read, trust that it's accurate, and know what to do with
it. A vague phrase feels finished to the writer, who already knows the meaning; the reader has to
reconstruct it. Avoiding that is a habit, so this skill pairs the rules with a feedback loop that
keeps refining them.

## Contents

- [Rules](#rules)
- [Before and after](#before-and-after)
- [Feedback loop](#feedback-loop)
- [Make it always-on](#make-it-always-on)

## Rules

- **Say what it is.** Titles and labels describe their content, like a documentation heading. No
  slogans, puns or statements the reader has to decode.
- **Name the topic it belongs to.** When a piece is part of a group: "Skills: …".
- **Reason first,** in one line. Then the guidance.
- **Concrete over figurative.** The exact command, number, name, place or step, not a turn of
  phrase that stands in for it.
- **Only state what's checked.** Mark anything unverified as such. Never assume people's
  pronouns or roles, or what a file or slide says without reading it.
- **What the reader acts on is visible,** not tucked in notes, links or footnotes. Background can
  go there.
- **Every line adds something new.** No filler, no repetition, no hype.
- **Same patterns throughout:** naming, structure, emphasis.
- **Last step before sending:** could the reader act on each sentence without asking what was
  meant? If not, replace the phrase with the plain fact it stands for.

## Before and after

Real slips, caught in use. Add new ones as they're caught.

| Vague or guessed | Plain |
| --- | --- |
| "A skill that *triggers*" / "Will it *fire*?" | "Skills: writing effective *descriptions*" |
| "Before it goes out" | "After writing, before it's sent, published or committed" |
| "Background can live a layer down" | "Background can go in speaker notes, linked pages or an appendix" |
| "Every line does work" / "dresses things up" | "Each line adds something new" / "no hype" |
| Describing a slide without reading it | Read it first, or say "not checked" |
| "He" for someone whose pronouns are unknown | "They" |

## Feedback loop

When the user points out vague or guessed wording:

1. Rewrite the phrase plainly, right away, in the text it came from.
2. Add the pair to the "Before and after" table where the rules live for this user: their
   `CLAUDE.md` / `AGENTS.md` (see below), or this file.
3. If the agent has persistent memory, save or update one `feedback` memory with the phrase, the
   plain version and why it was vague. Update the existing memory rather than adding a new one
   per slip.
4. If the same kind of slip recurs, sharpen the rule it falls under so the rule covers it.

## Make it always-on

A skill loads only when its description matches the task, and "every reply" rarely looks like a
specific task. For the rules to apply to everything, copy the [Rules](#rules) and
[Before and after](#before-and-after) sections into the always-loaded instructions file under a
heading such as `# Writing for readers`:

- Claude Code: `~/.claude/CLAUDE.md` (all projects) or `AGENTS.md` in a repo (legacy projects use `CLAUDE.md`)

Then point the feedback loop at that file, so new pairs land where they're always read.
