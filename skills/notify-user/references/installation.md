# Install spoken notifications

Adapted from `ai-proficient-software-developer-training/bonus-gift.md`, lines 25–230. The bundled [notify-user.ts](notify-user.ts) preserves the old MacBook's `--text`, `--project`, `--did`, and `--need` interface, supports an explicit macOS speech fallback, and accepts `--backend soprano|say`. Soprano is the default and preferred voice.

## macOS: install the notifier

Install Bun if missing. With Homebrew:

```sh
brew install oven-sh/bun/bun
```

Alternatively use the installer documented at [bun.sh](https://bun.sh). From this skill's directory, run:

```sh
mkdir -p "$HOME/.codex"
install -m 755 references/notify-user.ts "$HOME/.codex/notify-user.ts"
"$HOME/.codex/notify-user.ts" --help
```

The installed script uses `#!/usr/bin/env bun`, so Bun must be on the invoking shell's PATH. If needed, invoke `bun "$HOME/.codex/notify-user.ts" --text "message"` directly. Continue with the Soprano installation below before sending a notification. Missing Soprano is reported as an error; there is no automatic switch to native speech.

If the user explicitly prefers native speech, `--backend say` uses `/usr/bin/say` without a model or server. For a zero-dependency option without Bun, copy [notify-user.sh](notify-user.sh) to `~/bin/notify-user`, make it executable, and call it with plain text:

```sh
mkdir -p "$HOME/bin"
install -m 755 references/notify-user.sh "$HOME/bin/notify-user"
"$HOME/bin/notify-user" "Testing one two three"
```

This small fallback does not accept the TypeScript script's flags.

## Install the preferred local Soprano voice

[Soprano](https://github.com/ekwek1/soprano) provides local speech through its bundled Gradio web UI. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if missing, then:

```sh
uv tool install soprano-tts
```

On a supported NVIDIA machine, the source training document instead uses `uv tool install 'soprano-tts[lmdeploy]'`. The bundled notifier's playback requires macOS; a Linux port also needs a different player.

Ensure the uv tool bin directory (normally `~/.local/bin`) is on PATH. The notifier adds it for its subprocesses, alongside both Intel and Apple Silicon Homebrew locations.

The script starts `soprano-webui --device cpu` on demand on macOS, then calls `generate_speech` through its standard Gradio HTTP API, downloads the WAV, and plays it with `afplay`. CPU inference uses the same Soprano voice and avoids the PyTorch Metal startup crash observed with automatic MPS selection. No optional MCP package is needed. The initial model download requires internet access. Startup waits at most three minutes; inspect `/tmp/soprano-webui-notify-user.log` if it fails.

For a manual server check:

```sh
soprano-webui --device cpu
```

The UI should be at `http://127.0.0.1:7860`. Stop this manual server before testing automatic startup, or leave it running to reuse it:

```sh
"$HOME/.codex/notify-user.ts" --backend soprano --text "Testing the local Soprano voice"
```

Diagnose and repair Soprano if it fails; use `--backend say` only with an explicit request for the native voice. `--endpoint` selects an already configured server; automatic startup targets the default local server. `--keep` retains the generated temporary WAV, and Soprano playback also keeps `/tmp/notify-user-last.wav` for troubleshooting.

## Agent use and optional Claude hooks

Install this skill through the usual skill installer, or link its directory into `~/.codex/skills/notify-user`. The skill tells an agent when to speak and how to compose contextual messages. The agent's written response should still contain the result.

For Claude Code, the training document additionally recommends a global `~/.claude/CLAUDE.md` instruction to use the installed notifier when attention helps. Use `"$HOME/.codex/notify-user.ts" --text "message" &` rather than the training example's positional TypeScript invocation.

If every completed turn should speak, merge this optional hook into the existing `~/.claude/settings.json`; preserve other settings and hooks. It requires `jq` and duplicates contextual notifications unless the agent suppresses its own completion speech:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "input=$(cat); proj=$(basename \"$(printf '%s' \"$input\" | jq -r .cwd)\"); \"$HOME/.codex/notify-user.ts\" --text \"Claude is done in $proj and waiting for you\" >/tmp/notify-user-hook.log 2>&1 & exit 0"
          }
        ]
      }
    ]
  }
}
```

The background command keeps speech from holding up the hook, and `exit 0` prevents notifier failure from blocking completion. The training document also suggests a `Notification` hook for permission prompts. Hooks are optional and are not installed by this skill. After adding them, use `/hooks` in Claude Code and complete a small task to verify playback.

## Sharing between laptops with YADM

Track the notifier file, not copied uv tool environments, speech model caches, or generated launchd files:

```sh
yadm add "$HOME/.codex/notify-user.ts"
```

Each laptop installs its own dependencies. The dotfiles bootstrap installs Bun and uv alongside the hotkey tools, then installs Soprano with `uv tool install soprano-tts` when it is missing. Run the bootstrap on each laptop, or install these dependencies manually before using the notifier. Review and commit the intended YADM changes, then push/pull through your existing dotfiles workflow. Both native speech and Soprano still need an audible output device and suitable system volume.
