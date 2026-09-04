# Events

Read this when a plugin announces runtime behavior, observes another subsystem, or participates in policy/interception/pipeline behavior.

## Service vs event first

Use a **service** for a stable direct call with a result.

Use an **event** when producer and consumers should be loosely coupled, there may be zero/many listeners, or the contract is naturally broadcast/interception/middleware.

Do not use an event as an awkward request/response API when a service is the clearer contract.

## Typed custom event

```ts
import type { Context } from '@deepseek-ai/cordis'

declare module '@deepseek-ai/cordis' {
  interface Events {
    'my-plugin/ready'(id: string): void
  }
}

export function apply(ctx: Context) {
  ctx.on('my-plugin/ready', (id) => {
    console.log('ready', id)
  })

  ctx.emit('my-plugin/ready', 'worker-1')
}
```

Namespace custom events with a `domain/action` or `plugin/action` convention.

The declaration merge is type-only. Runtime code must still emit/listen.

When event declarations live in another module/package, make sure TypeScript actually sees that augmentation, for example with an appropriate type-only import when needed.

## Listener lifecycle

`ctx.on(...)` is lifecycle-owned. The listener is removed when the plugin unloads. Do not add redundant manual event unregistration for normal Cordis listeners.

## Dispatch mode is part of the contract

Cordis supports several dispatch modes. Match the event's documented mode instead of substituting another one:

| Mode | Call | Core semantics |
| --- | --- | --- |
| broadcast | `ctx.emit(...)` | synchronous broadcast; values/promises are not collected |
| parallel | `await ctx.parallel(...)` | listeners run concurrently and are awaited |
| serial | `await ctx.serial(...)` | ordered async listeners; first meaningful result can stop the chain |
| bail | `ctx.bail(...)` | synchronous short-circuiting counterpart |
| waterfall | `ctx.waterfall(...)` | around-middleware with a `next()` continuation |

For built-in Harness events, inspect the generated event surface for the owning subsystem because the mode and signature are contract details.

## Waterfall rule

A waterfall listener that intends downstream behavior to continue must call `next()`:

```ts
ctx.on('demo/transform', async (input, next) => {
  const result = await next()
  return result.toUpperCase()
})
```

Returning without calling `next()` intentionally short-circuits downstream handlers/default behavior. This is appropriate for a veto/decision handler, but a dangerous bug in an observer/logger.

## Services plus events

A common good design is:

```text
service = stable capability
  +
events = observation/policy hooks around that capability
```

For example, a service performs work while events announce results or let policy plugins intercept a decision.

## Durable session records are not automatically Cordis events

Harness also has durable session event records. Do not assume a durable record name is available as a same-named Cordis runtime event. Check the official subsystem/event surface; some durable records are observed through broader runtime streams.
