#!/bin/sh
# Zero-dependency macOS fallback; accepts plain text, without flags.
set -eu
[ "$#" -gt 0 ] && [ -n "$*" ] || { echo 'usage: notify-user "message"' >&2; exit 1; }
exec /usr/bin/say -- "$*"
