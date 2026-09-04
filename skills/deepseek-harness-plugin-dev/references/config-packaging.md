# Configuration, patches, bundles, and installation

Read this for configurable plugins or anything intended to be installed outside a source checkout.

## Typed plugin configuration

```ts
import type { Context } from '@deepseek-ai/cordis'
import Schema from '@deepseek-ai/schemastery'

export const name = 'my-plugin'

export interface Config {
  timeoutMs: number
  verbose?: boolean
}

export const Config: Schema<Config> = Schema.object({
  timeoutMs: Schema.number().default(30_000),
  verbose: Schema.boolean().default(false),
})

export function apply(ctx: Context, config: Config) {
  // config is validated before use
}
```

Put deployer-tunable defaults on the schema. Avoid secondary `?? default` logic scattered through execution code unless it represents a runtime fallback that cannot belong in plugin config.

## Patch overlay

Example development patch:

```yaml
- insert:
    - id: my-plugin
      name: '/absolute/path/to/plugin.ts'
      config:
        timeoutMs: 5000
```

When overriding an existing row by `id`, the row's `config` is replaced as a whole rather than deep-merged. Restate every required config key.

## Bundle vs profile

A **bundle** is the package you author and distribute. It ships a configuration patch and declares `dsh.bundle`.

A **profile** is a runnable composition managed under the Harness home. It lists bundles and has user-specific patch layers. Do not hand-author profile manifests unless the task explicitly concerns low-level profile internals.

## Minimal bundle

```text
dsh-my-plugin/
├── package.json
├── cordis.patch.yml
└── index.js
```

`package.json`:

```json
{
  "name": "dsh-my-plugin",
  "version": "0.1.0",
  "type": "module",
  "main": "index.js",
  "files": ["index.js", "cordis.patch.yml"],
  "dsh": {
    "bundle": {
      "patch": "./cordis.patch.yml"
    }
  }
}
```

`cordis.patch.yml`:

```yaml
- insert:
    - id: my-plugin
      name: dsh-my-plugin
```

When shipping TypeScript, use real built entry points and package exports appropriate to the repository/package setup rather than blindly copying this JavaScript-only minimal manifest.

## Install and verify

```sh
dsh plugin --profile demo add ./dsh-my-plugin
dsh --profile demo --dump-config
dsh --profile demo
```

Remove:

```sh
dsh plugin --profile demo remove dsh-my-plugin
```

In a source checkout, prefix commands with `pnpm` when required by the repository launcher.

## Layer precedence

Effective configuration is composed from ordered layers. Conceptually:

1. profile bundle patches, in bundle order
2. profile's own patch
3. home-level patch
4. CLI `--patch` overlays, in argv order

Later layers win. Always inspect `--dump-config` when behavior suggests the wrong row or config is active.

## Git installation and build scripts

A Git dependency commonly installs source, not prebuilt output. If the package relies on generated `lib/` or `dist/`, make sure the Git install path builds it safely, commonly through a self-contained `prepare` step.

Modern pnpm may require explicit approval before running dependency build scripts. Treat that approval as permission to execute package code on the host. Prefer trusted source, pinned commits, or prebuilt npm/tarball artifacts where appropriate.
