#!/bin/bash
# usage: run_challenge.sh <tag> <skill_dir> <prev_quiz_out_dir> <notes_profile>
# Runs a challenge round in a fresh session on top of the records of a finished quiz, then judges and scores it.
set -u; H="$(cd "$(dirname "$0")" && pwd)"; TAG="$1"; export SKILL_DIR="$2" EX_MODEL="${EX_MODEL:-opus}"; PREV="$3"; N="$4"
R="$H/runs/$TAG/challenge"; W="${TMPDIR:-/tmp}/cmu-eval-work/$TAG-ch-$$"; rm -rf "$R"; mkdir -p "$R" "$W"
slug=$(grep -m1 '^topic:' "$PREV"/checks/sessions/*.md | head -1 | sed 's/.*topic: *//')
mkdir -p "$W/records/$slug"; cp -R "$PREV/checks" "$W/records/$slug/checks"
python3 "$H/run_quiz.py" "$W" "$H/fixtures/$N.md" challenge "$R" > "$R.log" 2>&1 || { echo "CHALLENGE_FAIL $TAG"; exit 1; }
python3 "$H/judge_challenge.py" "$R" "$N" "$PREV" >> "$R.log" 2>&1 && python3 "$H/score_challenge.py" "$R"
echo "CHALLENGE_DONE $TAG"
