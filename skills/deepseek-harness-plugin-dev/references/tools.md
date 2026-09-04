# Model-callable tools

Read this when the plugin exposes a capability to the model through the Harness tool registry.

## Minimal tool plugin

```ts
import type { Context } from '@deepseek-ai/cordis'
import { defineTool } from '@deepseek-ai/dsh-tools'

export const name = 'greet-tool'
export const inject = ['tools']

export function apply(ctx: Context) {
  ctx.tools.register(defineTool({
    name: 'greet',
    description: 'Greet someone by name.',
    parameters: {
      name: {
        type: 'string',
        required: true,
        description: 'The name to greet',
      },
    },
    output: {
      schema: { type: 'string' },
      render: (_args, value) => [{ type: 'text', text: value }],
    },
    async execute(args, exec) {
      if (exec.signal.aborted) throw exec.signal.reason
      return `Hello, ${args.name}!`
    },
  }))
}
```

## Design the output as an API

The tool has two different outputs:

1. **Canonical value** returned by `execute()` and validated against `output.schema`.
2. **Model-facing content** produced by `output.render(args, value)`.

Keep ids, paths, handles, structured status, and other machine-consumable facts in the canonical value. Do not make callers recover data by parsing rendered prose.

Example:

```ts
output: {
  schema: {
    type: 'object',
    properties: {
      id: { type: 'string' },
      count: { type: 'number' },
    },
    required: ['id', 'count'],
  },
  render: (_args, value) => [{
    type: 'text',
    text: `Created ${value.count} records as ${value.id}.`,
  }],
}
```

Verify the exact schema DSL supported by the current `@deepseek-ai/dsh-tools` version before inventing complex nested schemas.

## Validation

`defineTool` validates declared argument types before `execute()` runs, but semantic constraints that are not represented in the schema still belong in executor logic. Examples: non-empty trimmed strings, positive ranges, mutual constraints across fields, or resource existence.

## Cancellation

Foreground tools should honor `exec.signal`. Forward it to APIs such as `fetch`, filesystem functions, subprocess helpers, or client libraries when they support an AbortSignal.

Do not reuse an outer signal as the lifetime owner for work that has already been published as a background job. Background work needs its own job-controlled lifetime.

## Error semantics

Throw for infrastructure/execution failures. For a successful domain outcome that is merely undesirable (for example a command completed with a non-zero exit status), return a valid canonical result that represents that outcome if the tool contract considers the execution successful.

## Policy and observation

Do not hardwire broad deployment policy into individual tools when Harness policy hooks can own it. Relevant extension points may include pre-execution policy, guards, execution wrappers, post-execution transformation, and result observation. Verify current signatures in the current `dsh-tools` package before implementing an interceptor.

## UI presentation

Tool UI and model content are separate concerns. Presentation functions may be replayed from persisted session data, so they must be deterministic and pure:

- no I/O
- no current clock
- no randomness
- no live session lookup

If result-time facts are required for replayable UI, project bounded structured metadata from the canonical result using the current supported presentation metadata API.

## Verification

For a user-visible tool:

1. Start Harness with the plugin loaded.
2. Confirm the tool appears in the tool registry/system prompt path.
3. Call it through the model or the Harness tool execution path.
4. Verify argument validation.
5. Verify canonical output shape.
6. Verify rendered content.
7. Verify cancellation if the operation can block.
8. Verify unload/HMR removes the registration.
