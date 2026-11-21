#!/bin/sh
set -eu
cd "$(dirname "$0")"
pandoc --from=html --to=gfm --wrap=none control.html -o variant.md
