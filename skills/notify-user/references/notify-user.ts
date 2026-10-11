#!/usr/bin/env bun
import { parseArgs } from "node:util";
import { spawn, spawnSync } from "node:child_process";
import { closeSync, openSync, unlinkSync } from "node:fs";

const DEFAULT_ENDPOINT = "http://127.0.0.1:7860";
const API_PATH = "/gradio_api";
const STARTUP_LOG = "/tmp/soprano-webui-notify-user.log";
const STARTUP_TIMEOUT_MS = 180_000;

const HELP = `Usage: ./notify-user.ts --text "message to speak"
       ./notify-user.ts --project "Project Name" --did "thing done" --need "where help is needed"

Synthesize speech via the local soprano-webui Gradio server and play it with afplay.

Options:
  -t, --text <string>       Text to speak
      --say  <string>       Alias for --text
      --project <string>    Project name for the generated sentence
      --did <string>        Work completed; may be passed more than once
      --need <string>       Help needed; may be passed more than once
      --endpoint <url>      Gradio server base URL (default: ${DEFAULT_ENDPOINT})
      --backend <name>    soprano (default), or say (macOS built-in)
      --keep                Keep the downloaded wav file instead of deleting it
  -h, --help                Show this help and exit
`;

const { values } = parseArgs({
  args: Bun.argv.slice(2),
  options: {
    text: { type: "string", short: "t" },
    say: { type: "string" },
    project: { type: "string" },
    did: { type: "string", multiple: true },
    need: { type: "string", multiple: true },
    endpoint: { type: "string", default: DEFAULT_ENDPOINT },
    backend: { type: "string", default: "soprano" },
    keep: { type: "boolean", default: false },
    help: { type: "boolean", short: "h", default: false },
  },
  strict: true,
});

if (values.help) {
  console.log(HELP);
  process.exit(0);
}

function cleanList(items: string[] | undefined): string[] {
  return (items ?? []).map((item) => item.trim()).filter(Boolean);
}

function formatList(items: string[]): string {
  if (items.length === 1) return items[0]!;
  if (items.length === 2) return `${items[0]} and ${items[1]}`;
  return `${items.slice(0, -1).join(", ")}, and ${items.at(-1)}`;
}

function buildNotificationText(): string | undefined {
  const project = values.project?.trim();
  const did = cleanList(values.did);
  const need = cleanList(values.need);
  if (!project && did.length === 0 && need.length === 0) return undefined;

  const sentences = [`Hey, I worked on ${project ?? "this project"}.`];
  if (did.length > 0 && need.length > 0) {
    sentences.push(`I did ${formatList(did)}, and now I need some help for ${formatList(need)}.`);
  } else if (did.length > 0) {
    sentences.push(`I did ${formatList(did)}.`);
  } else {
    sentences.push(`Now I need some help for ${formatList(need)}.`);
  }
  return sentences.join(" ");
}

const text = values.text ?? values.say ?? buildNotificationText();
if (!text || text.trim() === "") {
  console.error(HELP);
  process.exit(1);
}

// Resolve tools consistently in terminals and launchd environments on either Mac.
process.env.PATH = [process.env.HOME + "/.local/bin", process.env.HOME + "/.bun/bin",
  "/opt/homebrew/bin", "/usr/local/bin", process.env.PATH ?? ""].join(":");
const backend = values.backend;
if (!["soprano", "say"].includes(backend!)) {
  console.error("--backend must be soprano or say");
  process.exit(1);
}
if (backend === "say") {
  if (process.platform !== "darwin") {
    console.error("The built-in speech fallback requires macOS; install Soprano.");
    process.exit(2);
  }
  const play = spawnSync("/usr/bin/say", ["--", text], { stdio: "inherit" });
  process.exit(play.status ?? 3);
}
if (!Bun.which("soprano-webui", { PATH: process.env.PATH })) {
  console.error("soprano-webui is missing; install soprano-tts or use --backend say.");
  process.exit(2);
}

const baseUrl = values.endpoint!.replace(/\/+$/, "");
const apiUrl = `${baseUrl}${API_PATH}`;
const schemaUrl = `${apiUrl}/info`;

async function isReady(): Promise<boolean> {
  try {
    const res = await fetch(schemaUrl, { signal: AbortSignal.timeout(1_500) });
    if (!res.ok) return false;
    const info = await res.json() as { named_endpoints?: Record<string, unknown> };
    return Boolean(info.named_endpoints?.["/generate_speech"]);
  } catch {
    return false;
  }
}

function startBackend() {
  const logFd = openSync(STARTUP_LOG, "a");
  // CPU preserves the Soprano voice and avoids PyTorch Metal startup crashes.
  const args = process.platform === "darwin" ? ["--device", "cpu"] : [];
  const child = spawn("soprano-webui", args, {
    detached: true,
    env: { ...process.env, PYTHONUNBUFFERED: "1" },
    stdio: ["ignore", logFd, logFd],
  });
  child.on("error", (error) => {
    console.error(`Could not start soprano-webui: ${error.message}. See ${STARTUP_LOG}`);
    process.exit(2);
  });
  child.unref();
  closeSync(logFd);
  return child;
}

async function ensureReady(): Promise<void> {
  if (await isReady()) return;
  if (baseUrl !== DEFAULT_ENDPOINT) {
    console.error(`Soprano is not ready at ${baseUrl}; start that server before using --endpoint.`);
    process.exit(2);
  }
  const child = startBackend();
  const deadline = Date.now() + STARTUP_TIMEOUT_MS;
  while (Date.now() < deadline) {
    await Bun.sleep(1_000);
    if (await isReady()) return;
    if (child.exitCode !== null || child.signalCode !== null) {
      console.error(`soprano-webui exited (${child.exitCode ?? child.signalCode}). See ${STARTUP_LOG}`);
      process.exit(2);
    }
  }
  console.error(`soprano-webui did not become ready. See ${STARTUP_LOG}`);
  process.exit(2);
}

async function callTool(): Promise<string> {
  const res = await fetch(`${apiUrl}/call/generate_speech`, {
    signal: AbortSignal.timeout(30_000),
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ data: [text, 0.0, 0.95, 1.2, 1, false] }),
  });
  if (!res.ok) throw new Error(`Soprano request failed: ${res.status} ${await res.text()}`);
  const { event_id } = await res.json() as { event_id?: string };
  if (!event_id) throw new Error("Soprano returned no generation event ID");

  const result = await fetch(`${apiUrl}/call/generate_speech/${event_id}`, {
    signal: AbortSignal.timeout(120_000),
  });
  if (!result.ok) throw new Error(`Soprano result failed: ${result.status}`);
  const body = await result.text();
  for (const event of body.split(/\r?\n\r?\n/)) {
    if (!event.includes("event: complete")) continue;
    const line = event.split(/\r?\n/).find((line) => line.startsWith("data:"));
    if (!line) continue;
    const [audio, status] = JSON.parse(line.slice(5).trim()) as [{ url?: string } | null, string];
    if (!audio?.url) throw new Error(`Soprano produced no audio: ${status}`);
    return new URL(audio.url, baseUrl).href;
  }
  throw new Error(`Soprano generation failed: ${body}`);
}

async function downloadWav(url: string): Promise<string> {
  const res = await fetch(url, { signal: AbortSignal.timeout(30_000) });
  if (!res.ok) {
    console.error("Failed to download wav:", res.status, url);
    process.exit(2);
  }
  const buf = Buffer.from(await res.arrayBuffer());
  const path = `${require("node:os").tmpdir()}/notify-user-${Date.now()}.wav`;
  require("node:fs").writeFileSync(path, buf);
  return path;
}

const LAST_WAV_PATH = "/tmp/notify-user-last.wav";

await ensureReady();
const audioUrl = await callTool();
const wavPath = await downloadWav(audioUrl);
try { require("node:fs").copyFileSync(wavPath, LAST_WAV_PATH); } catch { /* best effort */ }
const play = spawnSync("afplay", [wavPath], { stdio: "inherit" });
if (play.status !== 0) {
  console.error(`afplay exited with status ${play.status}`);
  process.exit(play.status ?? 3);
}
if (!values.keep) {
  try { unlinkSync(wavPath); } catch { /* best effort */ }
}
