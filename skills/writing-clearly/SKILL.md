---
name: writing-clearly
description: |
  Keeps any text written for someone else plain, concrete and verified, so the reader gets the
  point at first read: replies to the user, documentation, slides, website and UI copy, emails,
  messages, commit messages, spoken notifications. Use when drafting, editing or reviewing copy,
  titles, headings, slide decks, pages or labels; when the user asks for clearer or less vague
  wording or points out a vague or guessed phrase; or when the user asks to make a message
  sendable, distill a text or draft an email to a group.
---

# Writing Clearly

For anyone who writes or edits text with or for the user: documentation, slides, web and UI copy,
emails, messages and commit messages. Collected from writing instructions and from corrections
made during a review of training material.

The reader should get the point at first read, trust that it's accurate, and know what to do with
it. A vague phrase feels finished to the writer, who already knows what it means; the reader has
to find out what it means.

## Contents

- [Rules](#rules)
- [Messages and emails](#messages-and-emails)
- [Before and after](#before-and-after)
  - [Say what it is (titles and labels)](#say-what-it-is-titles-and-labels)
  - [Describe, don't sell or nag](#describe-dont-sell-or-nag)
  - [Prefixes and titles that repeat the body](#prefixes-and-titles-that-repeat-the-body)
  - [Only state what's checked](#only-state-whats-checked)
  - [Concrete over figurative](#concrete-over-figurative)
  - [Professional register (slogans, punchlines, drama)](#professional-register-slogans-punchlines-drama)
- [Feedback loop](#feedback-loop)

## Rules

1. **Say what it is.** Titles and labels describe their content, like a documentation heading. No
   slogans, puns or statements the reader has to decode.
2. **Describe, don't sell or nag.** Everywhere, not only in titles: say what something is or does,
   not that it's good, important or a must. Test: negate the qualifier. "Writing skills that work"
   becomes "Writing skills that don't work"; nobody writes that, so the qualifier adds nothing:
   "Writing skills". If the negated version is something people actually do or believe ("review
   only the code"), the qualifier draws a real distinction and stays.
3. **Name the topic it belongs to,** when a piece is part of a group: "Skills: writing
   descriptions". Leave the prefix out when it adds nothing, and don't repeat the topic word after
   it.
4. **The title doesn't repeat the body.** If the list of questions is on the slide, the title is
   "Introduction", not "Introductions: name, role and three questions".
5. **Reason first,** in one line. Then the guidance.
6. **Concrete over figurative.** The exact command, number, name, place or step, not a turn of
   phrase that stands in for it.
7. **Professional register.** This is not a poem, a rap or a chat with classmates. Use established
   terms with no hidden meaning: no wordplay, metaphors, dramatic lines, punchlines or in-group
   slang. Established technical terms are fine ("lethal trifecta", "red/green", "slopsquatting").
8. **Only state what's checked.**
   - Verify facts against a primary source before they go in; mark anything unverified as such.
   - No rankings or superlatives nobody measured ("the most important", "the highest-value").
   - Read a file, slide or page before describing it; otherwise say "not checked".
   - Don't assume people's roles or pronouns. Use "they" unless pronouns are stated.
9. **What the reader acts on is visible,** not tucked in notes, links or footnotes. Background can
   go in speaker notes, linked pages or an appendix.
10. **Every line adds something new.** No filler, no repetition, no hype.
11. **Same patterns throughout:** naming, structure, emphasis.
12. **No italics in titles.** They're obtrusive. Use bold in body text for the word that carries
    the point.
13. **When editing someone else's material, move rather than delete.** Content that doesn't fit
    one place (speaker notes, background) goes somewhere else, not away. Keep facts, names,
    numbers and quotes intact.
14. **Last check before sending:** could the reader act on each sentence without asking what was
    meant? If not, replace the phrase with the plain fact it stands for.

## Messages and emails

When the user asks to make a message sendable, distill a text or write an email to a group, read
[references/messages-and-emails.md](references/messages-and-emails.md) first.

## Before and after

Corrections from real use, grouped by the rule they fall under. Add new ones as they're caught.

### Say what it is (titles and labels)

| Before | After |
| --- | --- |
| "A skill that *triggers*" / "Will it *fire*?" | "Skills: writing descriptions" |
| "Gate 1: ask for the evidence, not the claim" | "Gate 1: ask for the test output" |
| "Don't reinvent the wheel" | "Libraries: adopt, extend, fork or avoid" |
| "The day's spine (know it cold)" | "Structure of the day" |

### Describe, don't sell or nag

| Before | After |
| --- | --- |
| "Writing skills that work" | "Writing skills" |
| "Context discipline" | "Context management" |
| "Never accept a bare 'done'." | "Don't accept 'done' without that evidence." |
| "Memorize these, because the exercise grades on them." | "Four properties; the exercise grades on them." |

### Prefixes and titles that repeat the body

| Before | After |
| --- | --- |
| "Introductions: name, role and three questions" (the questions are on the slide) | "Introduction" |
| "Instruction layers: …" (prefix adds nothing) | "CLAUDE.md instruction layers" |
| "Test a skill like code" (in a group of skill slides) | "Skills: test them like code" |

### Only state what's checked

| Before | After |
| --- | --- |
| "The highest-value line you can write." (unmeasured, no reason, no place) | "Add this to CLAUDE.md: an edit that looks isolated can break callers the agent never read." |
| "The most important thing we saw was…" | "The topic that came up most was…" |
| "`~/.ssh` and `~/.aws` unreadable inside the sandbox" (checked: wrong) | "`~/.ssh` and `~/.aws` are readable by default until you add credential entries." |
| "He" for someone whose pronouns are unknown | "They" |
| Describing a slide without reading it | Read it first, or say "not checked" |

### Concrete over figurative

| Before | After |
| --- | --- |
| "Before it goes out" | "After writing, before it's sent, published or committed" |
| "the agent walks in blind" | "the agent starts without instructions" |
| "understand the blast radius first" | "check what depends on the code before changing it" |
| "A criterion without a command is a wish." | "A criterion without a command can't be verified." |
| "Background can live a layer down" | "Background can go in speaker notes, linked pages or an appendix" |
| "Every line does work" / "dresses things up" | "Each line adds something new" / "no hype" |

### Professional register (slogans, punchlines, drama)

| Before | After |
| --- | --- |
| "Generation got cheap. The verdict is your job." | "Agents write code quickly. Deciding whether it is correct is your job." |
| "A claim is not an artifact." | "The agent's summary is not evidence. Read the tool output." |
| "CLAUDE.md asks. A hook runs every time." | "CLAUDE.md is an instruction the agent can skip. A hook runs on every stop." |
| "Still green? Theater." | "Still green? The test can't detect this defect." |

## Feedback loop

When the user points out vague or guessed wording:

1. Rewrite the phrase plainly, right away, in the text it came from.
2. Add the pair to the "Before and after" table where the rules live for this user: their
   `CLAUDE.md` / `AGENTS.md` if the rules were copied there, otherwise this file.
3. If the agent has persistent memory, save or update one `feedback` memory with the phrase, the
   plain version and why it was vague. Update the existing memory rather than adding a new one
   per slip.
4. If the same kind of slip recurs, sharpen the rule it falls under so the rule covers it.
