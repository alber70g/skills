---
name: continue-autonomously
description: |
  Use whenever the user wants unattended progress over confirmation: "continue autonomously",
  "keep going", "don't stop to ask me", "work independently", "on your own", "log your assumptions
  and proceed", "I'll be away / afk", "just decide and move on".
---

# Continue Autonomously

Keep moving; don't stop to ask. Sort every fork into one of three tiers:

- **Trivial** (reversible, nobody would care): just decide. Don't log.
- **Load-bearing** (a reasonable person could choose differently): append an entry to `DECISIONS.md`
  at the repo root — each option with a one-line pro/con, the one you chose, and why — then
  immediately proceed with it. Don't wait for acknowledgement or batch questions for the end.
- **High-risk** (irreversible data loss, spending money, credentials/security, outward-facing
  actions like deploys/emails/shared PRs, scope changes): log it AND stop — state in chat what's
  blocked, your recommended option, and what you need. Prefer a reversible sibling when one exists
  (archive instead of delete, stage instead of deploy) so you can log and keep going.

When done, summarize: how many decisions were logged, highest-impact first, all pending review.
