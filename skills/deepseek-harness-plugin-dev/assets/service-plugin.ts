import { Service, type Context } from '@deepseek-ai/cordis'

declare module '@deepseek-ai/cordis' {
  interface Context {
    REPLACE_SERVICE_KEY: REPLACE_SERVICE_CLASS
  }
}

export class REPLACE_SERVICE_CLASS extends Service {
  constructor(ctx: Context) {
    super(ctx, 'REPLACE_SERVICE_KEY')
  }

  async execute(input: string): Promise<string> {
    return input
  }
}

export const name = 'REPLACE_PLUGIN_NAME'

export function apply(ctx: Context) {
  ctx.plugin(REPLACE_SERVICE_CLASS)
}
