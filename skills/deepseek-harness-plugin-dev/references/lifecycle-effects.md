# Lifecycle and effects

Read this when a plugin owns timers, sockets, file watchers, subprocesses, clients, child plugins, or anything that must cleanly survive unload/HMR cycles.

## Fiber state machine

Each loaded plugin instance owns a Fiber:

```text
PENDING -> LOADING -> ACTIVE
                \-> FAILED
ACTIVE -> UNLOADING -> DISPOSED
```

- **PENDING** — declared but required `inject` dependencies are not ready.
- **LOADING** — dependencies are ready and `apply` is executing.
- **ACTIVE** — plugin is running.
- **FAILED** — `apply` or configuration validation failed.
- **UNLOADING** — owned registrations/resources are being disposed.
- **DISPOSED** — cleanup is complete.

Required dependencies remain tracked after load. If one disappears, dependent plugins unload and may load again when it returns.

## What Cordis already owns

Common registrations are already lifecycle effects. Examples include:

- `ctx.on(...)` event listeners
- `ctx.plugin(child)` child Fibers
- `ctx.tools.register(...)` tool registrations
- other Harness registries that attach their disposer to the calling plugin

Do not manually duplicate their unregister logic unless the specific API explicitly requires it.

## Unmanaged resources belong in `ctx.effect()`

```ts
import type { Context } from '@deepseek-ai/cordis'

export function apply(ctx: Context) {
  ctx.effect(() => {
    const timer = setInterval(() => tick(), 1_000)

    return () => {
      clearInterval(timer)
    }
  })
}
```

Acquire the resource inside the effect when practical so ownership is obvious. The disposer runs on normal unload, config replacement, dependency loss, HMR, or parent disposal.

Async disposer:

```ts
ctx.effect(() => {
  const client = createClient()
  return async () => {
    await client.close()
  }
})
```

## Cleanup ordering caveat

Disposer invocation begins in reverse registration order, but multiple async disposers may run concurrently. If cleanup must be sequential, put those steps in one disposer:

```ts
ctx.effect(() => {
  const worker = startWorker()
  const db = openDb()

  return async () => {
    await worker.stop()
    await db.close()
  }
})
```

Do not encode correctness in the relative completion order of separate async effects.

## Child plugins and manual disposal

```ts
const fiber = ctx.plugin(childPlugin)
```

The child has its own Fiber but is recursively disposed with its parent. If the parent intentionally stops the child early:

```ts
await fiber.dispose()
```

Treat the Fiber handle as lifecycle control, not as a substitute for direct service APIs.

## HMR discipline

With Cordis HMR, replacement is conceptually:

1. unload old plugin
2. unwind its effects and children
3. load new code
4. run new `apply`

Therefore avoid process-global mutable state that keeps plugin-owned registrations/resources alive across reloads.

For a plugin with lifecycle-sensitive behavior, verify at least one reload/unload cycle and look for:

- duplicate listeners/tools
- timers still firing
- sockets/clients still connected
- orphaned child processes
- child plugins that remain mounted
- consumers retaining a vanished provider

## Resource ownership rule

Ask of every long-lived handle:

> Which Fiber owns this, and what disposes it when that Fiber unloads?

If there is no clear answer, the plugin is not lifecycle-safe yet.
