---
name: deepseek-harness-plugin-dev
description: Create, modify, debug, review, scaffold, test, and package DeepSeek Harness (dsh) plugins built on Cordis. Use when working with DeepSeek Harness plugins, Cordis plugins, cordis.yml or cordis.patch.yml, model-callable tools, services/providers, events, capability layering, plugin bundles, profiles, HMR, or dsh plugin installation.
compatibility: Requires a DeepSeek Harness checkout or installed dsh environment. TypeScript/Node.js and pnpm are commonly used; exact package APIs should be verified against the current Harness checkout when available.
metadata:
  author: openai
  version: "1.1.0"
  docs-reviewed: "2026-09-04"
  primary-framework: deepseek-harness-cordis
---

# DeepSeek Harness plugin development

Use this skill to implement real DeepSeek Harness plugins, not generic Node plugins. DeepSeek Harness is composed from Cordis plugins mounted into shared contexts; tools, model adapters, services, storage, policy, and agent behavior are extension points in that plugin tree.

## Cordis mental model

Reason in these concepts before designing a non-trivial plugin:

- **Plugin** — a lifecycle-owned unit mounted by Cordis. Usually a function with `apply(ctx)`; a `Service` subclass is also a plugin.
- **Context (`ctx`)** — the scoped repository of services and the entry point for Cordis registrations, events, effects, and child plugins.
- **Service** — a named capability exposed as `ctx.<key>`. Consumers depend on the capability name, not a concrete provider import.
- **`inject`** — declarative required service dependencies. It controls readiness and reloading; YAML row order is not dependency management.
- **Fiber/lifecycle** — every mounted plugin instance owns a Fiber that can be pending, load, become active, unload, and dispose.
- **Effect** — lifecycle-owned registration/resource. Cordis APIs already create effects; unmanaged resources belong in `ctx.effect()` with a disposer.
- **Event** — decoupled runtime communication. Use a service for direct capability calls; use events for announcements, observers, policy/interception, or pipelines.
- **Composition** — `cordis.yml` and patches describe a plugin tree; `ctx.plugin()` creates a child Fiber with independent lifecycle under its parent.

TypeScript declaration merging only adds compile-time knowledge of a service or event. It does **not** register anything at runtime.

For anything beyond one obvious registration, read `references/cordis-concepts.md` before choosing architecture. Then load only the task-specific references below.

## First: classify the requested plugin

Choose the smallest fitting shape before writing code:

| Need | Shape | Read next |
| --- | --- | --- |
| Cordis architecture is not already obvious | Mental-model pass | `references/cordis-concepts.md` |
| Startup behavior or simple registration | Function plugin | `references/plugin-basics.md` |
| Timers, sockets, watchers, child fibers, teardown, HMR safety | Lifecycle/effects | `references/lifecycle-effects.md` |
| Model-callable capability | Tool plugin | `references/tools.md` |
| Shared capability other plugins consume | Service definition/provider | `references/services.md` |
| Observe, announce, intercept, or pipeline behavior | Event listener/event contract | `references/events.md` |
| Nested plugin tree, groups, isolation, HMR composition | Composition | `references/composition-hmr.md` |
| User/deployment-tunable settings | Configurable plugin | `references/config-packaging.md` |
| Installable/distributable plugin | Bundle | `references/config-packaging.md` |
| Replaceable provider architecture | Three-role capability | `references/capability-design.md` |
| Plugin does not load, HMR behaves oddly, wrong config wins | Diagnostics | `references/diagnostics.md` |

Do not read every reference by default. Load only the references needed for the requested plugin. This is deliberate progressive disclosure.

## Core workflow

1. **Inspect the environment first.** If a DeepSeek Harness checkout is available, inspect its current package types, generated Cordis surfaces, nearby implementations, and effective configuration before relying on remembered APIs. Prefer current local source over copied examples.
2. **Model the plugin in Cordis terms.** Identify the plugin boundary, required services, lifecycle-owned resources, direct capabilities, event hooks, and whether child composition is needed.
3. **Identify the smallest seam.** Decide whether this is a function plugin, tool, service/provider, event listener/interceptor, adapter, configuration layer, or bundle. Do not split a simple tool into multiple packages without a real replacement/evolution boundary.
4. **Declare dependencies explicitly.** Use `inject` for required Cordis services. Never rely on row order in `cordis.yml` as a startup dependency mechanism.
5. **Keep lifecycle ownership inside Cordis.** Register listeners, tools, child plugins, and resources through `ctx`. Put manual cleanup for unmanaged resources in `ctx.effect()` and return a disposer.
6. **Choose service vs event intentionally.** Use services for stable callable capabilities and events for loose coupling, observation, decisions, and pipelines. Do not simulate one with the other without a reason.
7. **Make tunables configuration.** If two deployments may reasonably choose different values, expose them through an exported `Config` schema rather than hardcoding them.
8. **Implement the smallest coherent plugin.** Prefer a function plugin unless the plugin itself provides a stable service capability.
9. **Verify in a disposable setup.** For source development, load through a patch overlay and confirm the composed config. Exercise the actual registration/execution path and at least one unload/reload path when lifecycle behavior matters.
10. **Package only when required.** A distributable Harness plugin is normally an npm bundle with a `dsh.bundle` manifest pointing at its patch layer.
11. **Report exactly what changed.** Include files created/modified, how to run it, how to verify it, and any assumptions tied to the current Harness version.

## Non-negotiable implementation rules

- A basic Cordis plugin should expose `apply(ctx)`; `name` is useful metadata.
- Required services belong in `inject`; a dependent plugin should wait for services instead of polling or depending on YAML order.
- If a required service disappears, expect dependent plugins to unload and later reload. Do not retain required service instances outside the owning lifecycle.
- Registrations made through Cordis are lifecycle-owned. Do not add redundant manual unregistration for Cordis-owned registrations.
- Use `ctx.effect()` for unmanaged resources such as sockets, timers, subprocess handles, file watchers, or external clients that need explicit cleanup.
- When cleanup order matters, keep ordered steps in one disposer; do not assume several async disposers finish serially.
- `ctx.plugin(child)` creates a child Fiber; use it for lifecycle-aware composition rather than manually invoking another plugin's `apply()`.
- Declaration merging for `Context` or `Events` is type-only. Runtime service registration/emission/listening must still be implemented.
- For configuration, export both the TypeScript `Config` type/interface and a same-named Schemastery schema. Put defaults on schema fields.
- For tools, register with `ctx.tools.register(defineTool(...))`, declare `inject = ['tools']`, return a canonical JSON-compatible value matching `output.schema`, and keep model-facing prose in `output.render`.
- Tool executors must honor `exec.signal` for foreground cancellation when the underlying API supports cancellation.
- Do not make UI presentation functions perform I/O or depend on time/random/session state; replay must remain deterministic.
- Namespace custom events. Match the documented Cordis dispatch mode (`emit`, `parallel`, `serial`, `bail`, or `waterfall`) to the contract.
- A waterfall observer/middleware that intends downstream behavior to continue must call `next()`; omitting it is an intentional short-circuit.
- Use class/service form when the plugin provides a stable `ctx.<service>` capability; otherwise prefer function form.
- For source-checkout Web testing with `--patch`, remember that a patch does not relocate module resolution to the patch file's directory. Use a resolvable package name or an appropriate absolute source path.
- For standalone Cordis tutorial launchers executed from their scratch directory, relative module paths in that local `cordis.yml` are valid because the loader resolves from that composition context.
- Give composition entries stable `id`s when they should survive config edits as the same logical plugin instance.
- A bundle and a profile are different things. Author the bundle; let `dsh plugin` manage profile dependencies/manifests.
- Patch layers replace a targeted row's whole `config` value rather than deep-merging it. When overriding a row, restate all required config keys.
- Treat third-party plugins and install/build scripts as trusted host code. Review source and dependencies before granting build permissions.

## Default development path

For a new plugin in a Harness source checkout:

1. Create a small plugin source file.
2. Create a patch overlay that inserts it with a stable `id`.
3. Start the relevant surface, commonly:

```sh
pnpm dsh web --patch ./path/to/cordis.yml
```

4. If behavior depends on composition, inspect:

```sh
pnpm dsh --profile web --dump-config
```

or the installed-CLI equivalent:

```sh
dsh --profile web --dump-config
```

5. Exercise the plugin through the real Harness path.
6. Trigger one reload/unload cycle when the plugin owns resources, listeners, tools, services, or child plugins.
7. Add focused tests next to the owning package when the change is intended to ship.

For a simple starting point, use the templates in `assets/`. The optional scaffold helper supports the main plugin shapes:

```sh
node scripts/scaffold.mjs --name my-plugin --type basic|tool|service|configurable|bundle --out ./my-plugin
```

Treat generated code as a starting point and verify imports/types against the current Harness checkout. For an installable package, read `references/config-packaging.md` before generating manifests.

## Before finalizing code

Check these failure-prone points:

- Is the intended Cordis shape correct: function plugin, service, event extension, child composition, or tool?
- Does every required `ctx.<service>` have a matching `inject`?
- Is declaration merging being mistaken for runtime registration?
- Does the plugin load and unload safely under HMR?
- Are explicit external resources disposed?
- Are child plugins mounted with lifecycle ownership rather than manually called?
- Are config defaults and validation in the schema rather than scattered in runtime code?
- Does a tool return the value promised by `output.schema`?
- Does the tool separate canonical data from rendered prose?
- Does foreground work honor cancellation?
- Does every waterfall handler either deliberately short-circuit or call `next()`?
- Does a patch override the intended row `id`, and if so, does it restate the complete config?
- If packaged, does `package.json` declare `dsh.bundle.patch` and include the shipped patch/code files?
- If installed from Git, are built artifacts available or is a safe `prepare` path documented?

## Currentness rule

DeepSeek Harness and its vendored Cordis surface evolve quickly. When exact signatures, service names, event modes/signatures, config fields, Fiber APIs, or package entry points matter, inspect the current repository or current official docs instead of extrapolating from this skill. Use `references/sources.md` as the starting source map.
