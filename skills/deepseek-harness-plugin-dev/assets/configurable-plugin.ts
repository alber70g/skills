import type { Context } from '@deepseek-ai/cordis'
import Schema from '@deepseek-ai/schemastery'

export const name = 'REPLACE_PLUGIN_NAME'

export interface Config {
  enabled: boolean
  timeoutMs: number
}

export const Config: Schema<Config> = Schema.object({
  enabled: Schema.boolean().default(true),
  timeoutMs: Schema.number().default(30_000),
})

export function apply(ctx: Context, config: Config) {
  if (!config.enabled) return
  // Register behavior here.
}
