# Plugin basics

Read this when creating a simple DeepSeek Harness/Cordis plugin. For architecture vocabulary, start with `cordis-concepts.md`. For resources/unload behavior, read `lifecycle-effects.md`.

## Minimal function plugin

```ts
import type { Context } from '@deepseek-ai/cordis'

export const name = 'my-plugin'

export function apply(ctx: Context) {
  // Register capabilities here through ctx.
}
```

Function form is the default for behavior and registrations. Use a `Service` subclass when the plugin itself provides a stable reusable `ctx.<service>` capability.

## Required dependencies

```ts
export const inject = ['tools', 'llm']

export function apply(ctx: Context) {
  // ctx.tools and ctx.llm are ready here.
}
```

A plugin remains PENDING until required services exist. If a required service disappears, Cordis unloads the dependent plugin and can load it again when the service returns. Dependency topology belongs in `inject`, not YAML row position.

## Child composition

Do not call another plugin's `apply()` manually. If this plugin owns a child plugin, mount it:

```ts
export function apply(ctx: Context) {
  ctx.plugin(childPlugin)
}
```

The child receives its own Fiber/lifecycle scope and is disposed with its parent. Read `lifecycle-effects.md` and `composition-hmr.md` for non-trivial trees.

## Development overlay

For a plugin loaded into the Web surface from a source checkout, a patch can insert a row:

```yaml
- insert:
    - id: my-plugin
      name: '/absolute/path/to/deepseek-harness/scratch-plugin/src/my-plugin.ts'
```

Then run:

```sh
pnpm dsh web --patch ./scratch-plugin/cordis.yml
```

A patch layer contributes configuration; it does not make module paths resolve relative to the patch file itself. Prefer a package specifier or a correct absolute path when testing a local source file this way.

## Standalone Cordis tutorial mode

The tutorial launcher is different: when you run the Cordis loader from the tutorial scratch directory, that local `cordis.yml` may load `./hello.ts` directly because that composition is rooted in the scratch directory.

## Minimal review checklist

- Is function form enough?
- Are all required services in `inject`?
- Is every registration created from the owning plugin lifecycle?
- Should this be a service rather than behavior-only plugin?
- If it owns resources or children, did you also read `lifecycle-effects.md`?
