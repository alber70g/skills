# Capability design and layering

Read this only when a capability needs replaceable providers or independently evolving components.

## Three-role pattern

DeepSeek Harness commonly separates a general capability into:

1. **Service definition** — stable contract and request/result types.
2. **Service provider** — concrete implementation of that contract.
3. **Consumer** — for example a model-callable tool exposing the service.

This is useful when providers must be replaceable without changing consumers.

## Example structure

```text
@my/dsh-capability        # service definition + types
@my/dsh-capability-local  # provider
@my/dsh-tool-capability  # consumer/tool
```

Service definition:

```ts
import { Service, type Context } from '@deepseek-ai/cordis'

declare module '@deepseek-ai/cordis' {
  interface Context {
    myCap: MyCapService
  }
}

export abstract class MyCapService extends Service {
  constructor(ctx: Context) {
    super(ctx, 'myCap')
  }

  abstract execute(request: MyCapRequest): Promise<MyCapResult>
}

export interface MyCapRequest {
  input: string
}

export interface MyCapResult {
  output: string
}
```

Provider:

```ts
import type { Context } from '@deepseek-ai/cordis'
import { MyCapService } from '@my/dsh-capability'

class LocalMyCap extends MyCapService {
  async execute(request: { input: string }) {
    return { output: request.input.toUpperCase() }
  }
}

export function apply(ctx: Context) {
  ctx.plugin(LocalMyCap)
}
```

Consumer/tool:

```ts
export const inject = ['tools', 'myCap']
```

The consumer calls `ctx.myCap` and does not import the provider.

## Do not split preemptively

Keep a capability in one plugin/package when there is only one implementation and no meaningful independent evolution boundary. Splitting everything into definition/provider/consumer adds dependency and release overhead.

Split when at least one of these is true:

- multiple providers are expected
- provider security/execution model differs by deployment
- consumer surfaces evolve independently from execution
- the service contract is reused by several plugins
- separate packages reduce coupling in a real way

## Contract ownership

The service definition package owns request/result types. Providers and consumers depend on that definition, not on each other.

Prefer explicit normalization/resolution functions for complex defaults before provider execution. Keep public service behavior predictable and testable.
