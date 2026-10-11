---
name: notify-user
description: Speak a short local notification when a task finishes, work is blocked, or the user needs to make a decision, using the installed notify-user script on macOS.
---

# Notify User

Use spoken notifications when the user's attention helps: after substantial work or a milestone, when waiting for input or review, or when a blocker requires their help. For long unattended work, announce a meaningful phase change. Skip routine tool updates and fast back-and-forth conversation when the user is already watching.

Check that `$HOME/.codex/notify-user.ts` exists and Bun and `soprano-webui` are available. If either is missing, read [references/installation.md](references/installation.md), which includes setup instructions and links to the executable files. Do not claim a notification succeeded if the command failed.

Compose one short sentence, two for a blocker. Name the project, say what happened, and state the decision, review, or awareness needed. Spell spoken acronyms with spaces, such as “A P I” or “M C P”. Speak only the context needed to bring the user back to the task.

```sh
"$HOME/.codex/notify-user.ts" --text "In the skills project, the notification skill is ready for your review." >/tmp/notify-user.log 2>&1 &
```

The script also accepts `--project "Project Name"`, repeatable `--did "work completed"`, and repeatable `--need "help needed"` to construct a message. Prefer `--text` for natural wording. Use `--help` to inspect the installed interface.

Use Soprano, the default backend. The user prefers its voice; do not silently substitute macOS speech when Soprano is missing or broken. Read the installation reference to set up or repair Soprano. Use `--backend say` only when the user explicitly requests built-in speech. The first Soprano call can take up to three minutes while the server starts and the model downloads, so send routine notifications in the background. For setup verification, run in the foreground and inspect its exit status.

Keep the ordinary written response: speech supplements it. Avoid duplicate notifications when an existing completion hook already covers the same event.
