import type { Context } from '@deepseek-ai/cordis'

export const name = 'REPLACE_PLUGIN_NAME'

export function apply(ctx: Context) {
  // Register behavior through ctx so Cordis owns its lifecycle.
  // For unmanaged resources, wrap acquisition/cleanup in ctx.effect().
}
