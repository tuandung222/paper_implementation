#!/usr/bin/env bash
set -euo pipefail

source .venv/bin/activate

plan-act-run run-episode --goal "Find the top contributor and follow them" --no-dynamic-replanning --no-use-cot
plan-act-run run-episode --goal "Find the top contributor and follow them" --dynamic-replanning --no-use-cot
plan-act-run run-episode --goal "Find the top contributor and follow them" --dynamic-replanning --use-cot
