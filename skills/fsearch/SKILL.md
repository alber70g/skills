---
name: fsearch
description: Search local macOS files with the installed FSearch CLI by fuzzy name, path, indexed contents, symbol definition, size, type, or modification age. Use for locating files across the disk, finding large or recent files, and searching text inside files.
---

# FSearch

Use the installed `fsearch` CLI to locate files and folders on macOS. Searches start the daemon automatically and share its index. Ordinary searches need no build, installation, or login-item setup.

## Choose the query type

Plain words search **names**, not contents. Choose the keyword by what the user wants to match:

| Intent | Query | Meaning |
|---|---|---|
| Find a file by name | `readme` | Fuzzy matching; words of 5+ letters tolerate one typo |
| Literal name fragment | `'readme` | Case-insensitive substring without fuzzy matching; not whole-name equality |
| Name starts/ends with | `^readme` / `.rs$` | Prefix / suffix matching |
| Exclude a name fragment | `!backup` | Negated literal name token |
| Regex on filename | `re:^main\.rs$` | Case-insensitive filename regex; anchor for whole-name equality |
| Regex on full path | `path:/src/.*\.rs$` | Case-insensitive path regex |
| Literal text inside files | `grep:apply_dir` | Content search; regex metacharacters are literal |
| Regex inside files | `regex:fn\s+\w+_dir` | Content regex; distinct from `re:` and `path:` |
| Symbol definition | `sym:apply_dir` | Declaration-pattern matching; use `grep:` for references/calls |

`sym:` is a declaration heuristic, not language-server resolution, and is case-sensitive. Literal and regex content searches use smart-case: all-lowercase patterns ignore case; an uppercase character makes matching case-sensitive.

Use one of `grep:`, `regex:`, or `sym:` per query. Repeating these replaces the previous content pattern rather than combining patterns. Plain words in a content query still narrow names/paths; they do not become additional content patterns.

## Narrow the results

Combine the search mode with metadata filters. A filter-only query is valid, especially for large or recent files.

| Keyword | Values and examples |
|---|---|
| `in:` | Folder subtree, e.g. `in:~/projects`; `~` expands inside the query. Prefer an absolute path or `~` path for explicit scope. |
| `ext:` | Extensions, optionally with a dot; comma-separated alternatives, e.g. `ext:rs,py`. |
| `type:` | Extension groups: `image`, `video`, `audio`, `doc`, `code`, `archive`, `font`; `app` selects `.app` directories. These are not MIME/content detection. |
| `kind:` | `file`, `dir` (or `folder`), `link` (or `symlink`). |
| `size:` | `>5mb`, `<1gb`, `10mb..100mb`, or an exact size. Units: bytes (`b` or none), `kb`, `mb`, `gb`, `tb`; decimal multiples. |
| `mtime:` | Modification **age**: `<7d` means within seven days; `>30d` means older than thirty days; `7d..30d` means that age range. Units: `s`, `m`/`min`, `h`, `d` (default), `w`, `mo`, `y`. |
| `limit:` | Maximum returned results/files, e.g. `limit:20`; default 50. Not a size sort or a total count. |

Use one range expression per `size:` or `mtime:`; repeating these replaces the previous range. In the inspected implementation, `>`/`>=` share an inclusive lower bound and `<`/`<=` share an inclusive upper bound. Verify boundary values when strict inequalities matter.

Use the requested folder as `in:` when known; omit it for whole-disk discovery. Results are ranked by relevance, not largest-first. For largest files, retrieve enough candidates with `kind:file size:...`, sort their JSON `size` fields descending, and qualify the ranking if `limit:` may have truncated candidates. Directory sizes are not recursive disk usage; use a disk-usage tool for largest folders.

## Quote and run

Pass the whole query as one shell argument so `>`, `<`, `!`, `$`, and backslashes reach FSearch intact. Inside that argument, FSearch double quotes group values containing spaces. Shell quoting and FSearch quoting are separate layers; the leading apostrophe in `'exact` is a query operator.

```bash
fsearch 'readme in:~/projects limit:20' --json
fsearch "'readme in:~/projects limit:20" --json
fsearch 're:^main\.rs$ in:~/projects' --json
fsearch 'type:image size:>5mb mtime:<7d limit:20' --json
fsearch 'kind:file size:>1gb limit:100' --json
fsearch 'ext:rs grep:apply_dir in:~/projects' --json
fsearch 'ext:rs regex:fn\s+\w+_dir in:~/projects' --json
fsearch 'sym:apply_dir in:~/projects' --json
fsearch 'grep:"connection refused" in:"~/projects/My Project"' --json
```

Prefer `--json` for interpreting results programmatically. Name responses contain `ok` and `hits` with `path`, `kind`, `size` (bytes), `mtime` (Unix seconds), and `score`. Content responses contain `files` with `path` and `matches` (`line`, `text`), plus `complete`, `indexing`, and `source` (`index` or `scan`). Check `ok`; errors are not empty results. Preserve returned paths exactly, including spaces.

For awkward quoting or structured batches, use `fsearch stdio`: send one JSON object per line and close stdin after a finite batch. Serialize arbitrary strings instead of hand-escaping them.

```json
{"q":"readme","in":"~/projects/My Project","limit":20}
{"op":"grep","pattern":"connection refused","mode":"literal","in":"~/projects/My Project","limit":20}
{"op":"grep","pattern":"fn\\s+\\w+_dir","mode":"regex","in":"~/projects","limit":20}
```

## Coverage and follow-up

Name and metadata search reach more files than content search. The inspected build indexes eligible text files under the home directory up to **1 MiB (1,048,576 bytes)**, with a smaller cap for extensionless files. It excludes some formats, generated files, and trees such as `build/` and `vendor/`. Explicit `in:` outside the content-index scope can use a scan, but that scan also caps candidate sizes at 1 MiB. A `size:` filter does not bypass content-size limits.

For contents of large files, locate paths with FSearch first, then stream-search relevant text files with `rg -n -F -- 'literal' /absolute/file` or `rg -n -- 'regex' /absolute/file`. Use the same targeted fallback when content coverage omits a relevant file. Read useful matching lines and surrounding context instead of loading a whole large file. Finding a PDF, archive, or image by type does not imply FSearch can extract its contents.

For empty or incomplete results, check the query mode and scope before broadening. `complete:false`, pending `indexing`, and result limits can explain partial results; even `complete:true` does not prove all disk files were covered. Name and content updates can have different indexing delays.

Use `fsearch status` when coverage or readiness is in doubt. Without Full Disk Access, protected macOS folders are skipped. If those folders matter, explain the gap: terminal-launched indexing needs a terminal with Full Disk Access; a login item needs a grant for `~/.local/bin/fsearch`, renewed after rebuilds. Do not reconfigure installation or permissions as part of an ordinary search.

Return relevant paths, content line numbers/snippets, or file sizes, and state material scope or coverage limits. Inspect relevant files before drawing conclusions about their contents.
