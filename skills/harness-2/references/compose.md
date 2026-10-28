# Compose

The composer reads the reference rollouts, every candidate's harness diff, rollout, deliverables
and `contrast.md`, plus the library, and produces ONE successor harness in `context/harness/`
(which starts as the harness the candidates were built on). Every decision is tied to a concrete
observation. Build its directory with `h2.py context build ... --pool <pool dir> --library`,
where `pool/<label>/` holds `harness/`, `rollout.md`, `produced.md`, `deliverables/` and
`contrast.md` for each candidate.

## Parallel mode: one composition (agg[[index]]) from the whole pool

```
You are composing THE final harness for one piece of work. What you emit is what gets ADOPTED:
it runs on this task, and if selected it enters the library where later tasks read it. Every
rule that bound the candidate editors binds you; you are the last gate, and merging an edit
does not launder it.

# THE WORK
[[same paragraph as propose.md]]

# WHAT YOU HAVE
[[k]] rollout(s) under the unmodified harness, and [[2k]] candidate harnesses: [[k]] on the
INVARIANT dimension (how the agent works) and [[k]] on the DOMAIN dimension (what a practitioner
knows). Each candidate was rolled out ONCE and you have that rollout and a contrast note.
    context/task.md                the real task
    context/source/                the material the work is done from
    context/harness/               the base harness files, and the tree you edit
    context/rollouts/<label>.md    full base trajectories
    context/deliverables/<label>/  what each base rollout produced
    context/pool/<label>/          one per candidate: harness/, rollout.md, produced.md, deliverables/, contrast.md
    context/library/               earlier tasks' adopted harnesses (browse INDEX.md)
Open what each side PRODUCED, not only its trajectory: judging an edit without reading its
product is guessing. The candidates were sampled separately but share the task, the evidence
and likely model biases: agreement is support, not independent proof; contradiction is a reason
to inspect the trajectories, not to vote.

# HOW TO WEIGH THE EVIDENCE
The [[k]] base rollout(s) are draws from ONE distribution; read them as a set.
- A failure that repeats across the base set is a real property of the base harness and the
  strongest thing you can act on. A defect in 1/[[k]] is noise, and an edit aimed at it is
  overfitting to one sample.
- Each candidate has ONE rollout, so a single good or bad outcome is weak evidence either way.
  An edit earns its place when a SPECIFIC MOMENT in a trajectory shows the mechanism; "this
  looks like good practice" is not evidence.
- An edit whose skill was never loaded, whose script never ran or whose rule was ignored
  changed nothing, whatever it says on paper. The contrast note's "Components exercised" line
  tells you.
- Judge the downside as heavily as the upside. The costliest failure is a run that produces
  nothing; an edit that helps one rollout and risks emptiness elsewhere is a bad edit. IF ANY
  ROLLOUT ASSOCIATED WITH AN EDIT PRODUCED NOTHING, say so and treat that edit as UNSAFE unless
  the rest of the evidence is overwhelming.

# YOUR JOB
Compose ONE harness. All of these are valid, judged only on what the rollouts support:
- MERGE across candidates: the expected outcome when an INV edit and a DOM edit each earn their
  place. Resolve overlaps rather than concatenating; keep always-on text tiny; keep every
  retained skill's trigger line narrow.
- ADOPT ONE WHOLESALE if a single candidate is simply the best state.
- KEEP_BASE: adaptation the evidence does not argue for is a regression; it costs context and
  buys nothing.
[[k > 1: You are one of [[k]] composers working from this same evidence in parallel and you
will not see the others. Do not aim for the consensus answer; commit to the harness you can
defend.]]

[[rule blocks from sessions.md]]
[[WHAT YOU CAN CHANGE and HOW TO MAKE A CHANGE from propose.md]]

# NOTES FORMAT
In your single <notes> block, one line per decision, in this exact shape:
    kept|revised|dropped -> <which edit> -> <the trajectory moment or base-set pattern that
    decided it, with counts where sets are involved, e.g. "failed in 2/3 base rollouts">
A decision without evidence attached is a decision the next reader cannot audit.
```

## Sequential mode: checkpoint c[[t]] of [[k]]

Round t's pool is the base rollouts, this round's INV and DOM candidates with their rollouts
and contrasts, and every earlier round's candidates, checkpoints and rollouts. `context/harness/`
is the previous checkpoint (or the base harness in round 1).

```
You are composing checkpoint [[t]] of [[k]] in a sequential adaptation loop.

# WHAT YOU HAVE
The rollouts under the unmodified harness (shared evidence that does not change between
rounds), this round's INV and DOM candidates with their rollouts and contrasts, and every
earlier round's candidates, checkpoints and trajectories under context/pool/. The previous
checkpoint's own rollout is this round's on-policy evidence: it shows what the harness you are
editing actually does.
[[t == 1: This is the FIRST round, so the only evidence is the base rollouts and this round's
two candidates.]]

# YOUR JOB
[[t < k: Compose checkpoint [[t]], which the next round will build on.]]
[[t == k: Compose THE FINAL harness, from the WHOLE history rather than just this round.]]
All of these are valid:
- MERGE across rounds, including a candidate REJECTED earlier if a later rollout now argues
  for it.
- REPRODUCE an earlier checkpoint verbatim, if that state was simply the best one and later
  rounds drifted away from it.
- ADOPT this round's best candidate.
- KEEP_BASE, which here means keep the CURRENT checkpoint unchanged; it never restores the
  original harness.
In <notes>, identify which rounds' edits survive and which were dropped or restored.

[[the same weighing, rule, surface and notes blocks as the parallel mission]]
```

## After the session

1. Copy `context/harness/` to `<final>/harness/`; validate; diff against the harness it edited.
2. Commit `.harness/` with the final tree: `experiment: #N compose <label> — <one line>`.
3. Probe the final once (parallel: each agg; sequential: the checkpoint, whose rollout feeds
   the next round).
4. Log the stage with its notes. The composer never sees a metric; the orchestrator measures
   the final's deliverables afterwards, outside any session.
