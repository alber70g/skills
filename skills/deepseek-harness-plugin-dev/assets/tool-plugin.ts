import type { Context } from '@deepseek-ai/cordis'
import { defineTool } from '@deepseek-ai/dsh-tools'

export const name = 'REPLACE_PLUGIN_NAME'
export const inject = ['tools']

export function apply(ctx: Context) {
  ctx.tools.register(defineTool({
    name: 'REPLACE_TOOL_NAME',
    description: 'REPLACE_DESCRIPTION',
    parameters: {
      input: {
        type: 'string',
        required: true,
        description: 'Input value',
      },
    },
    output: {
      schema: { type: 'string' },
      render: (_args, value) => [{ type: 'text', text: value }],
    },
    async execute(args, exec) {
      if (exec.signal.aborted) throw exec.signal.reason
      return args.input
    },
  }))
}
