#!/usr/bin/env node
import { mkdir, readFile, writeFile } from 'node:fs/promises'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const args = process.argv.slice(2)
const get = (flag) => {
  const i = args.indexOf(flag)
  return i >= 0 ? args[i + 1] : undefined
}

const name = get('--name')
const type = get('--type') ?? 'basic'
const out = resolve(get('--out') ?? `./${name ?? 'dsh-plugin'}`)
const packageName = get('--package') ?? (name ? `dsh-${name}` : 'dsh-my-plugin')

const toCamel = (value) => value.replace(/-([a-z0-9])/g, (_, c) => c.toUpperCase())
const toPascal = (value) => value.split('-').map(part => part.charAt(0).toUpperCase() + part.slice(1)).join('')
const serviceKey = /^[A-Za-z_$]/.test(toCamel(name ?? '')) ? toCamel(name) : `service${toPascal(name ?? '')}`
const pascalName = toPascal(name ?? '')
const serviceBase = /^[A-Za-z_$]/.test(pascalName) ? pascalName : `Dsh${pascalName}`
const serviceClass = serviceBase.endsWith('Service') ? serviceBase : `${serviceBase}Service`

if (!name || !/^(?:[a-z0-9]|[a-z0-9][a-z0-9-]*[a-z0-9])$/.test(name)) {
  console.error('Usage: scaffold.mjs --name <lowercase-hyphen-name> [--type basic|tool|service|configurable|bundle] [--out dir] [--package npm-name]')
  process.exit(2)
}

const here = dirname(fileURLToPath(import.meta.url))
const assets = resolve(here, '../assets')
const templateFor = {
  basic: 'basic-plugin.ts',
  tool: 'tool-plugin.ts',
  service: 'service-plugin.ts',
  configurable: 'configurable-plugin.ts',
}

await mkdir(out, { recursive: true })

if (type === 'bundle') {
  let pkg = await readFile(join(assets, 'bundle-package.json'), 'utf8')
  pkg = pkg.replaceAll('REPLACE_PACKAGE_NAME', packageName)
  await writeFile(join(out, 'package.json'), pkg)
  await writeFile(join(out, 'index.js'), `export const name = '${name}'\n\nexport function apply(ctx) {\n  // Register behavior through ctx so Cordis owns its lifecycle.\n}\n`)
  await writeFile(join(out, 'cordis.patch.yml'), `- insert:\n    - id: ${name}\n      name: ${packageName}\n`)
} else {
  const template = templateFor[type]
  if (!template) {
    console.error(`Unknown --type ${type}. Expected basic, tool, service, configurable, or bundle.`)
    process.exit(2)
  }

  await mkdir(join(out, 'src'), { recursive: true })
  let source = await readFile(join(assets, template), 'utf8')
  source = source
    .replaceAll('REPLACE_PLUGIN_NAME', name)
    .replaceAll('REPLACE_TOOL_NAME', name.replaceAll('-', '_'))
    .replaceAll('REPLACE_DESCRIPTION', `Execute ${name}.`)
    .replaceAll('REPLACE_SERVICE_KEY', serviceKey)
    .replaceAll('REPLACE_SERVICE_CLASS', serviceClass)
  await writeFile(join(out, 'src', 'index.ts'), source)

  const sourcePath = join(out, 'src', 'index.ts')
  await writeFile(join(out, 'cordis.yml'), `- insert:\n    - id: ${name}\n      name: '${sourcePath}'\n`)
}

console.log(`Created ${type} DeepSeek Harness plugin scaffold at ${out}`)
console.log('Review package/import versions against your current DeepSeek Harness checkout before running it.')
