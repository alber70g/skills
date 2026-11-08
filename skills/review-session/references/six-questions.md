# The 7 Questions Framework

Ask these for EVERY skill used (or should have been used) during the session.

## Q1: Did the instructions work?
**Signal**: You followed a step in SKILL.md and it was wrong, missing, or confusing.
**Action**: TUNE SKILL.md — fix the specific step. Don't append, rewrite.
**Example**: SKILL.md said "query request_metadata" but should have said "filter request_time on both sides of JOIN."

## Q2: Did I learn how something works?
**Signal**: You discovered a field, API, system behavior, or pattern not documented.
**Action**: GROW `references/` — create `references/thing-learned.md`.
**Example**: Discovered that `tool_composer_step_prod_view` has a `client_name` field.

## Q3: Did I solve a problem worth saving?
**Signal**: The solution required non-obvious knowledge. Other users would ask similar things.
**Action**: GROW `examples/` — save using the example format (see `references/example-format.md`).
**Example**: Saved the working BQ query for "error rate by client with JOIN."

## Q4: Did I repeat code I wrote before?
**Signal**: You wrote the same helper script or automation in 2+ sessions.
**Action**: GROW `scripts/` — extract the reusable code.
**Example**: Extracted a `validate_query.py` script that checks partition filters.

## Q5: Did I discover a new trigger phrase?
**Signal**: User phrased a request in a way that should (or shouldn't) have triggered this skill.
**Action**: GROW `evals/triggers.json` — add the trigger phrase.
**Example**: User said "what did we learn?" — should trigger review-session but wasn't listed.

## Q6: Did I find a failure mode to test for?
**Signal**: Something went wrong that the skill's evals should catch. A regression that should never repeat.
**Action**: GROW `evals/evals.json` — add a test case with input and assertions.
**Example**: "JOIN query without partition filter" → add as test case asserting partition filter is present.

## Q7: Did the skill make things WORSE?
**Signal**: The skill gave wrong instructions, loaded irrelevant context, or added confusion instead of clarity.
**Action**: RETIRE — move to `_retired/` if dead weight, or TUNE heavily if the core idea is sound.
**Example**: A skill kept suggesting outdated API endpoints, causing more debugging than it saved.

## Decision Tree
```
User corrected me         → Q1 (tune SKILL.md) + Q6 (add regression eval)
Discovered new info       → Q2 (add reference)
Solved a hard problem     → Q3 (add example)
Wrote same code again     → Q4 (extract script)
New trigger phrase        → Q5 (add to triggers.json)
Something broke/missed    → Q6 (add to evals.json)
Skill made things worse   → Q7 (retire or heavy tune)
Zero mistakes, good work  → Still check Q2-Q6 for growth opportunities
```
