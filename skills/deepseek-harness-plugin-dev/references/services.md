# Services and dependencies

Read this when a plugin provides a reusable capability, consumes a required capability, or needs replaceable providers.

## Consume a required service

```ts
import type { Context } from '@deepseek-ai/cordis'

export const inject = ['tools']

export function apply(ctx: Context) {
  ctx.tools.register(/* ... */)
}
```

When `apply` runs, required injected services are ready. If a required service is absent, the plugin stays PENDING. If it disappears later, the consumer unloads and may reload when the service returns.

Do not fix dependency problems with row ordering, startup delays, or polling.

## Provide a service

A stable capability generally uses a `Service` subclass:

```ts
import { Service, type Context } from '@deepseek-ai/cordis'

declare module '@deepseek-ai/cordis' {
  interface Context {
    metrics: MetricsService
  }
}

export class MetricsService extends Service {
  constructor(ctx: Context) {
    super(ctx, 'metrics')
  }

  record(event: string, value: number) {
    // implementation
  }
}

export const name = 'metrics'

export function apply(ctx: Context) {
  ctx.plugin(MetricsService)
}
```

Two separate things happen:

- `super(ctx, 'metrics')` performs runtime service registration.
- the `declare module` block gives TypeScript compile-time knowledge of `ctx.metrics`.

Declaration merging alone does not create the service.

A service subclass can itself declare dependencies when appropriate; verify the exact static/instance plugin shape against the current Cordis types in the checkout.

## Consumer contract

Consumers depend on the service key/contract, not the provider:

```ts
export const inject = ['metrics']

export function apply(ctx: Context) {
  ctx.metrics.record('loaded', 1)
}
```

The service key is the compatibility seam. Keep its public contract stable when multiple providers or consumers are expected.

## Optional services

If a capability is genuinely optional, do not turn it into a required `inject` merely for convenience. Query at the use site and handle absence explicitly. Verify the current Cordis `ctx.get()` behavior/type surface before generating exact code.

## When to define a service

Prefer a service when:

- callers need a direct result
- several plugins share the capability
- provider implementation may vary by deployment
- the capability has a stable contract worth naming
- lifecycle/provider replacement should be managed by Cordis

Do not create a service for a one-off local helper that never crosses a plugin boundary.

## Isolation

Cordis composition can isolate a service instance for separate plugin groups. Use this when two subtrees need different providers/configurations for the same service name.

Conceptually:

```text
group A -> isolated shell -> plugin A
group B -> isolated shell -> plugin B
```

This is usually better than adding process-global routing switches to one provider. Read `composition-hmr.md` before generating isolation config.

## Replaceable provider layering

When the service definition, provider, and consumer need independent package/version boundaries, read `capability-design.md`. Do not split them preemptively when one plugin is sufficient.
