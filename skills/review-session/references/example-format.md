# Example File Format

When saving a solution to `examples/`, use this exact format:

```markdown
# Title (descriptive, searchable)

## User Request
"the exact thing the user asked, in their words"

## Working Solution
[the code/query/config/steps that worked]

## Key Gotcha
[what was non-obvious — the thing a future agent needs to know]

## Session Date
YYYY-MM-DD
```

## What Makes a Good Example

Save ONLY when all three are true:
1. **Solved a real user problem** (not a toy exercise)
2. **Required non-obvious knowledge** (the agent needed the skill to get it right)
3. **Can be generalized** (other users would ask similar things)

## What Makes a Bad Example
- Trivial solutions that any agent could figure out
- Overly specific to one user's data (no generalization)
- Missing the key gotcha (the whole point is what's non-obvious)

## File Naming
Use kebab-case describing the problem:
- `error-rate-by-model.md` ✅
- `query1.md` ❌
- `example.md` ❌
