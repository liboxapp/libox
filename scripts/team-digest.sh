#!/usr/bin/env bash
# SessionStart: bounded, quoted external data; never fetch or interpret metadata.
set -uo pipefail
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec python3 "$script_dir/team_digest.py"
