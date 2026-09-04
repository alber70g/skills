# Diagnostics and verification

Read this when a plugin does not load, loads twice, gets the wrong config, leaks resources, or behaves differently across profiles.

## Plugin never loads

Check, in order:

1. Is the patch layer actually applied?
2. Does `--dump-config` show the row?
3. Is the module specifier/path resolvable from the composition context?
4. Does the plugin have required `inject` dependencies that never appear?
5. Did `apply()` throw?
6. Is a later patch overriding/removing/replacing the row?
7. If installed as a bundle, does the package declare `dsh.bundle.patch`?
8. If installed from Git, do referenced build outputs actually exist?

## Plugin stays pending

Likely cause: a required service in `inject` is absent, isolated into another group, or provided by a row that is itself failing/pending.

Inspect the composed tree and current service definitions. Do not fix this with arbitrary delays.

## Duplicate tools/listeners after edits

A normal Cordis-owned registration should disappear when its plugin unloads. Duplicates suggest one of these:

- registration happened outside the owning plugin lifecycle
- a global singleton retained state across reloads
- a custom resource was not wrapped in `ctx.effect()`
- code spawned unmanaged work that re-registers later
- the plugin is actually inserted more than once in composed config

## Wrong configuration

Remember that later patch layers win and a row config replacement is not a deep merge. Inspect effective config rather than reasoning only from the patch file you just edited.

## Wrong startup order

Do not reorder YAML rows as the primary fix. Declare the service dependency with `inject`.

## HMR crash or leak

Exercise at least one reload cycle. Verify:

- external clients close
- timers stop
- child processes/jobs follow the intended ownership model
- listeners/tools disappear
- service consumers tolerate provider replacement through normal Cordis lifecycle

## Tool-specific failures

Check:

- parameter schema matches actual model arguments
- semantic validation is performed where the schema cannot express it
- canonical output matches `output.schema`
- renderer handles every valid canonical value
- exceptions represent actual execution failure
- foreground work handles `exec.signal`
- presentation code is pure and replay-safe

## Packaging failures

Check:

- package entry point exists after install
- `files` includes patch and built code
- package name in the patch resolves to the installed package
- `dsh.bundle.patch` points at the shipped patch
- Git builds are self-contained
- pnpm build-script approval has not blocked `prepare`
- profile bundle list contains the plugin after `dsh plugin add`

## Verification output to give the user

When finishing a plugin task, provide:

- created/changed files
- exact run command
- exact verification command or interaction
- expected observable result
- any version-sensitive API assumptions
- any security-sensitive host access or dependency/install behavior
