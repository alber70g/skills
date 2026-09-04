# Composition, groups, isolation, and HMR

Read this when designing a non-trivial `cordis.yml` tree, nested groups, isolated providers, or diagnosing reload/composition behavior.

## `cordis.yml` is a plugin tree

Composition determines which plugin instances exist and how they are configured. An entry can have a stable identity and lifecycle metadata, not merely a module name.

```yaml
- id: greeter
  name: './greeter.ts'
- id: consumer
  name: './consumer.ts'
  disabled: true
```

Use stable `id`s for logical entries that should be recognized as the same entry across configuration edits. Without a stable id, edits can cause an otherwise unchanged row to be treated as removal plus addition.

## Dependencies are not row order

If `consumer` requires `greeter`, express that through a service and `inject`. Reordering YAML rows is not the dependency model.

A plugin with an unsatisfied required dependency remains PENDING. That is a valid lifecycle state and can be silent.

## Groups and child composition

Configuration groups nest a subtree that can load/unload as a unit. Runtime `ctx.plugin(child)` similarly creates a child Fiber owned by its parent, but these are different composition surfaces:

- `cordis.yml`/patches compose the application tree declaratively.
- `ctx.plugin()` composes a child dynamically from plugin code.

Use the simplest surface that matches ownership and configurability.

## Service isolation

Groups can isolate a service name so separate subtrees see different providers/configurations.

Use isolation when you truly need scoped instances, for example:

```text
group A -> shell(timeout 5s)  -> plugin A
group B -> shell(timeout 60s) -> plugin B
```

Do not invent global mutable provider routing when Cordis isolation expresses the boundary directly.

Verify exact `group`/`isolate` config syntax against the current Harness docs/config catalog before emitting production config.

## HMR

When Cordis HMR is enabled, replacing plugin code follows the lifecycle model:

1. unload the old plugin
2. dispose its effects/children
3. load the new implementation
4. run `apply` again

This only stays safe when registrations and resources are owned by the correct Fiber. Read `lifecycle-effects.md` for cleanup rules.

## Diagnosing a plugin that never loads

A silent plugin may be PENDING rather than failed. Check:

1. Is the row present in effective config?
2. Is the module resolvable?
3. Are all `inject` services provided in the visible/isolation scope?
4. Is a provider itself PENDING or FAILED?
5. Did configuration validation or `apply()` throw?

In a standalone Cordis debugging context, the runtime registry/Fiber states can be inspected; use the current `FiberState`/registry API from the checked-out Cordis version rather than assuming an old exact signature.

## Patch composition

DSH profiles are built from ordered layers/bundles plus profile/home/CLI patch layers. Later layers can replace targeted entries. Inspect the effective composition instead of reasoning from one YAML file in isolation:

```sh
dsh --profile web --dump-config
```

For source checkout commands, use the repo's equivalent `pnpm dsh ...` invocation.

Read `config-packaging.md` for bundle/profile/patch packaging semantics.
