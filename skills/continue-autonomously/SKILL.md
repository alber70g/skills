---
name: continue-autonomously
description: |
  Work through a task without stopping at every fork. When you hit a genuine ambiguity, record it
  in a decision log — the options you had, the recommended option, and why — then CONTINUE with the
  recommended option instead of pausing to ask. Use whenever the user wants unattended or long-running
  progress over confirmation: "continue autonomously", "keep going", "don't stop to ask me", "work
  independently", "log your assumptions and proceed", "I'll be away / afk", "just decide and move on".
  Still halts for high-risk or human-authority decisions (data loss, spending, credentials, deploys,
  scope changes) — those get logged AND surfaced, not guessed.
---

# Continue Autonomously

## Purpose

Momentum over interruption. The default agent instinct is to stop and ask whenever something is
unclear. That's the right call when a human is watching and a wrong guess is expensive. It's the
*wrong* call when the user has stepped away and wants the task to keep moving — every pause becomes
dead time.

This skill flips the default: instead of blocking on an ambiguity, you **make the best decision you
can, write it down, and keep going.** The human reviews your decisions afterward, not one at a time.

The trade you're managing: a stop costs the user's time; a silent wrong guess costs trust. The
decision log is what makes the trade safe — nothing is silent, so a wrong guess is cheap to catch
and correct.

## The three tiers

Every fork in the road falls into one of three tiers. Sorting the fork correctly is the whole skill.

| Tier | What it is | What you do |
|------|-----------|-------------|
| **1 — Trivial** | Reversible, no reasonable person would care (local names, internal helper shape, idiomatic choices) | Just decide. Don't log. Keep going. |
| **2 — Load-bearing** | A reasonable person could pick differently, and it's costly-ish to reverse, or the user would likely have an opinion (public names, data formats, a new dependency, UX behavior, an API contract) | **Log it** (options + recommended + why), proceed with the recommended option, keep going. |
| **3 — High-risk** | Irreversible, outward-facing, or needs human authority (see below) | **Log it AND stop.** Surface to the human. Do not guess. |

Tier 2 is the heart of this skill. Most forks are tier 1 (just decide) or tier 2 (log and proceed).
Tier 3 should be rare — if you're stopping often, you're mis-sorting tier 2 forks as tier 3.

## Tier 3 — when to stop instead of proceed

These are non-negotiable. When a fork involves any of the following, logging is not enough — halt and
ask the human, because the cost of a wrong guess isn't recoverable by editing a file:

- **Irreversible data loss** — dropping tables, deleting files or branches you didn't create,
  `rm -rf`, rewriting git history, force-push.
- **Spending money** — provisioning paid resources, purchases, anything that bills.
- **Credentials & security** — secrets, auth changes, permission/access changes, anything that
  weakens the security posture.
- **Outward-facing / hard to retract** — deploying to production, sending email, posting publicly,
  opening PRs against shared repos, anything a third party sees.
- **Scope or contract change** — the task would fundamentally differ from what was asked, or you'd
  touch files outside the agreed scope.

**Surface it in writing.** Write the entry to the log *and* state the block in your chat reply —
what's blocked, the option you recommend, and exactly what you need to proceed. The log and your
written summary are the channel; do not rely on audio or desktop notifications to get attention.

**Technique — convert tier 3 into tier 2 when you can.** Often a risky action has a reversible
sibling. Unsure whether to delete? Archive instead (reversible → tier 2, log and proceed). Unsure
whether to deploy? Stage the change and leave it for the human. Preferring the reversible path lets
you keep moving without gambling on something you can't undo.

## What counts as a tier-2 ambiguity worth logging

Log when a decision is **genuinely open** (the user didn't specify, and a reasonable person could
choose differently) *and* **load-bearing** (it shapes the design, crosses an interface, adds a
dependency, or the user would plausibly want a say). If you'd struggle to defend the choice as
"obviously the only sensible option," it's a tier-2 fork.

Do **not** log tier-1 trivia. A log full of "I named the loop variable `i`" buries the two decisions
that actually matter. The signal-to-noise of the log is what makes the human willing to read it —
protect it.

## How to choose the recommended option

Pick the option you'd defend to the user, using these tie-breakers in order:

1. **Reversibility** — prefer the choice that's cheapest to undo if it turns out wrong.
2. **Existing conventions** — match how this codebase already does it, even if you'd personally
   differ. Consistency beats taste inside a codebase.
3. **Least surprise** — the option a maintainer would expect, not the clever one.
4. **Simplicity** — the least code that satisfies what was actually asked. No speculative flexibility.
5. **Stated goal** — alignment with the user's expressed intent over your inferred nice-to-haves.

Then write the *why* in one line. The reasoning is what lets the human agree at a glance — or spot
that you weighed it wrong.

## The decision log

**Location.** Default to a single append-only `DECISIONS.md` at the repo root — visible on purpose,
because the human has to find and skim it. First check whether the project already has a decision or
ADR convention (an existing `DECISIONS.md`, `docs/adr/`, `decisions/`); if so, follow it instead of
inventing a second place. Prefer one scrollable file over scattered notes.

**Create the file once** with this header, then append entries:

```markdown
# Autonomous Decision Log

Decisions made autonomously to keep momentum while working unattended. Each entry is an assumption
I made instead of stopping to ask. Review these and set **Status**: CONFIRMED if you agree, or
OVERRIDDEN (say what to do instead) if not.

Status: PENDING REVIEW (default) · CONFIRMED · OVERRIDDEN
```

**Entry template** — append one per tier-2 (and tier-3) decision:

```markdown
## [#N] <short decision title>
- **Date:** <YYYY-MM-DD>
- **Status:** PENDING REVIEW
- **Where:** <file / area this affects, so it's findable>
- **Context:** <what was ambiguous and why a decision was needed here>
- **Options:**
  1. <Option A> — <one-line tradeoff>
  2. <Option B> — <one-line tradeoff>
- **Chosen:** <Option A> (recommended)
- **Why:** <the tie-breaker that decided it — reversibility / convention / least surprise / ...>
- **Blast radius:** <what breaks if this is wrong, and how to reverse it>
```

Keep entries tight. Two options with real tradeoffs beats five strawmen. The `Blast radius` line is
what tells the human how hard to look — a one-line reversible tweak needs a glance; a data-format
choice needs real attention.

## Keeping momentum

This is the part that's easy to get wrong. After you log a tier-2 decision, **immediately act on the
recommended option and continue.** Do not:

- ask "should I continue?" — continuing is the whole point;
- wait for acknowledgement before the next step;
- pile up questions to batch-ask at the end (that's just a delayed stop).

Log inline mentions *terse* — a single line like `⚖️ Logged decision #3: chose Postgres over SQLite
(durability); continuing.` keeps a watching human oriented without turning your output into a
running commentary.

The only things that legitimately break momentum: a tier-3 fork, or a genuine hard block (you need a
credential, access, or a fact that only the human has — and there's no reversible way forward).

## End-of-run summary

When the task is done (or you hit a hard block), close the loop with a short summary so the human
knows what to review:

> Made N autonomous decisions (logged in `DECISIONS.md`). Highest-impact: **#3** chose Postgres for
> durability, **#5** put auth on the API gateway not per-service. Both PENDING REVIEW — the rest are
> low-stakes. Nothing was destructive or outward-facing.

Lead with the decisions most likely to be wrong or most expensive to unwind. A summary that says
"3 decisions, all reversible, none touch data" earns a quick approval; one that buries a schema
choice at position 7 does not.

## Revisiting decisions

A logged decision isn't frozen. If later work proves an earlier assumption wrong, don't quietly
build on the mistake — go back, mark that entry (e.g. append `→ superseded by #8: <reason>`), and
correct course. The log is a live record of your reasoning, not a paper trail you defend.

## Examples

**Tier 1 — just decide, no log.**
> Need a name for a private helper that formats a timestamp. → Name it `formatTimestamp`, move on.
> Logging this would be noise.

**Tier 2 — log and proceed.**
> The user said "store the results" but not where. Options: SQLite (zero-config, single-file, easy to
> reverse) vs Postgres (durable, concurrent, but adds a service). Recommended: SQLite — reversible and
> the task shows no concurrency need. Log entry #2, proceed building against SQLite, keep going.

**Tier 3 — log and stop.**
> The migration script would `DROP` an existing `users` table to rebuild it. This is irreversible data
> loss on data I didn't create. Log entry #4, then stop and ask the human — do not run it. (If a
> reversible path exists — rename the old table instead of dropping — take that and drop to tier 2.)

**Bad — a stop disguised as autonomy.**
> Logging ten tier-2 decisions and then ending with "let me know how you want to handle these before I
> continue." That's a batched stop. Proceed with the recommended options; the human reviews after.

**Bad — silent guess.**
> Picking Postgres over SQLite and just... not writing it down. If it's wrong, the human finds out by
> reading code. The log is the entire safety mechanism — skipping it defeats the skill.

## Quick checklist

Before you pause to ask a question, run this:

- [ ] Is this actually tier 3 (irreversible / outward / needs authority)? If not, don't stop.
- [ ] Is there a reversible sibling that turns this into tier 2? Prefer it.
- [ ] If tier 2: did I log options + recommended + why, then *keep going*?
- [ ] If tier 1: did I just decide without cluttering the log?
- [ ] At the end: did I summarize the decisions worth reviewing, worst-first?
