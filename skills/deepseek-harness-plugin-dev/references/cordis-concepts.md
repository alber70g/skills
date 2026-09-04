# Cordis concepts for DSH plugin authors

Read this before designing a non-trivial DeepSeek Harness plugin. It is a mental-model reference, not an API catalog.

## The central idea

DeepSeek Harness is a Cordis plugin tree. Capabilities are not expected to find one another through global imports or manual boot order. A plugin is mounted into a `Context`, consumes named services from that context, registers lifecycle-owned effects, and may announce or intercept behavior through events.

A useful model is:

```text
cordis.yml / patches
        |
        v
   plugin tree
        |
        +--> Fiber: plugin A
        |      +--> effects
        |      +--> child Fibers
        |
        +--> Fiber: plugin B --inject--> ctx.tools
        |
        +--> Fiber: provider ---------> ctx.myService

shared/scoped Context
  ctx.tools
  ctx.llm
  ctx.myService
  events + effect ownership
```

## 1. Plugin

A plugin is a lifecycle-owned unit. The common form is a function plugin:

```ts
import type { Context } from '@deepseek-ai/cordis'

export const name = 'my-plugin'

export function apply(ctx: Context) {
  // Register behavior through ctx.
}
```

A `Service` subclass is also a plugin. Prefer function form for behavior/registration; use service form when the plugin provides a stable capability on `ctx`.

Do not manually invoke another plugin's `apply(ctx)` as a composition mechanism. Mount a child with `ctx.plugin(childPlugin)` so it gets its own Fiber and cleanup boundary.

## 2. Context

`Context` is more than a convenience argument. It is the service repository and lifecycle-aware API surface visible to the plugin.

Think of `ctx.tools`, `ctx.llm`, or `ctx.myService` as capability slots. Consumers depend on the slot; configuration/provider plugins decide which implementation fills it.

This decouples:

```text
consumer --> service key <-- provider
```

instead of:

```text
consumer --> concrete provider import
```

## 3. Service and `inject`

A service is a named callable capability. A required dependency is declared with `inject`:

```ts
export const inject = ['tools', 'myService']
```

Cordis keeps the plugin PENDING until all required services are available. If a required service later disappears, the consumer unloads; it can load again when the dependency returns.

Consequences:

- YAML row order is not a dependency mechanism.
- Do not poll for a required service.
- Do not cache a required service into process-global state that outlives the plugin Fiber.
- Provider replacement can be safe because consumers follow lifecycle transitions.

Use an optional lookup only when the capability is genuinely optional; verify the current `ctx.get()` typing/behavior in the checked-out Cordis version.

## 4. Fiber and lifecycle

Every mounted plugin instance owns a Fiber. The core states are:

```text
PENDING -> LOADING -> ACTIVE
                \-> FAILED
ACTIVE -> UNLOADING -> DISPOSED
```

PENDING is not inherently an error: it commonly means a required injected service has no provider yet.

The Fiber is the ownership boundary for plugin registrations and child plugins. This is why DSH plugins should be written as reloadable units rather than process-lifetime singletons.

Read `lifecycle-effects.md` when the plugin owns resources or HMR/unload behavior matters.

## 5. Effects

An effect is work/resource registration owned by the plugin lifecycle. Cordis-managed APIs already create effects for their registrations, including common listeners and Harness registries.

For unmanaged resources, use `ctx.effect()`:

```ts
ctx.effect(() => {
  const watcher = createWatcher()
  return () => watcher.close()
})
```

The disposer belongs to Cordis; do not manually invoke it for ordinary plugin-lifetime cleanup.

A useful rule:

```text
If it must disappear when this plugin unloads,
it must be owned by this plugin's Cordis lifecycle.
```

## 6. Service vs event

Choose based on coupling and result semantics.

Use a **service** when another plugin needs to call a stable capability and receive a direct result:

```text
consumer --call--> ctx.search.search(query) --> result
```

Use an **event** when something happened, there may be zero/many observers, or plugins may cooperate around a decision/pipeline:

```text
producer --emit--> event --> listener A
                         --> listener B
```

Some Cordis event modes can short-circuit or wrap downstream behavior. The dispatch mode is part of the event contract, not an implementation detail.

Read `services.md` or `events.md` for mechanics.

## 7. Composition

`cordis.yml` and applied patch layers select the running plugin tree. Composition entries have identity, configuration, enable/disable state, grouping, and optional service isolation.

`ctx.plugin(child)` is runtime composition inside a parent plugin. The child gets an independent Fiber and unloads recursively with its parent.

Use groups/isolation when separate subtrees need different providers of the same service name rather than adding global mutable routing to one provider.

Read `composition-hmr.md` for stable `id`, groups, isolation, HMR, and diagnosing PENDING plugins.

## 8. Type declarations are not runtime wiring

This is a frequent coding-agent failure.

```ts
declare module '@deepseek-ai/cordis' {
  interface Context {
    greeter: GreeterService
  }
}
```

only teaches TypeScript that `ctx.greeter` is a valid property. It does not create or register the service.

Likewise:

```ts
declare module '@deepseek-ai/cordis' {
  interface Events {
    'greeter/used'(name: string): void
  }
}
```

only declares the event's type signature. Runtime code must still emit/listen.

Keep compile-time augmentation and runtime registration visibly paired in designs and reviews.

## Architecture decision checklist

Before generating code, answer:

1. What is the plugin's lifecycle boundary?
2. Which services are required vs genuinely optional?
3. Does it provide a new `ctx.<key>` capability?
4. Does it need direct calls (service) or loose coupling/interception (event)?
5. Which resources must disappear on unload?
6. Does it compose child plugins?
7. Does deployment need separate service instances through isolation?
8. Are any TypeScript declarations being confused with runtime wiring?
9. Is a three-role service/provider/consumer split actually justified?

If these answers are simple, keep the implementation simple.
