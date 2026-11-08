# Small task for a real trial

Use this only as an optional fixture; it does not demonstrate empirical improvement by itself.

Task A: Extract each explicit action item, its stated owner (or `unknown`), and stated due date (or `unspecified`) from these notes. Cite the source sentence. Preserve uncertainty.

```text
Maya will send the draft on Friday. The dashboard needs review, but nobody volunteered.
Leo asked whether the launch should move; no decision was made.
```

Task B (transfer check): Same request, different source:

```text
Nora agreed to review the contract tomorrow. Someone should book a room; the group left ownership open.
The team discussed a migration but agreed to wait for the budget decision.
```

Run A with k=1 on a small user-provided base harness and a real fresh-session adapter. Propose, probe both candidates, compose, and execute; retain only observed lessons. Run B from the exact same H₀, allowing selective library reuse. Compare against B's own baseline. Log failures or no improvement honestly. To investigate k>1, use the same A inputs, model, and limits in a separate fresh task lab and compare executed deliverables anonymously. Never assert that a larger k guarantees improvement. Keep any private scoring rubric/answer key outside session inputs.

Run helper tests separately with:

```bash
python3 -m unittest discover -s /path/to/harness-2/tests -v
```
