#!/bin/sh
set -eu

# Initialize the default idea brief directory for this workspace.

ideas_dir=${1:-docs/ideas}

mkdir -p "$ideas_dir"

printf '{"status":"ready","directory":"%s"}\n' "$ideas_dir"
