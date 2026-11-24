#!/bin/bash
# usage: run_chain.sh <tag> <skill_dir> <p1|p3> [challenge]
# One learner chain in isolated mode, with judging: baseline -> (challenge round) -> retest
set -u; H="$(cd "$(dirname "$0")" && pwd)"; TAG="$1"; export SKILL_DIR="$2" EX_MODEL="${EX_MODEL:-opus}"; p="$3"; CH="${4:-}"
R="$H/runs/$TAG"; W="${TMPDIR:-/tmp}/cmu-eval-work/$TAG-$p-$$"; rm -rf "$R/$p"; mkdir -p "$R/$p"
[ -d "$R/skill-snapshot" ] || cp -R "$SKILL_DIR" "$R/skill-snapshot"
case $p in p1) a=notes_p1a; b=notes_p1b;; p3) a=notes_p3a; b=notes_p3b;; esac
python3 "$H/run_quiz.py" "$W" "$H/fixtures/$a.md" baseline "$R/$p/baseline" > "$R/$p-baseline.log" 2>&1 || { echo "CHAIN_FAIL $TAG $p"; exit 1; }
python3 "$H/judge.py" "$R/$p/baseline" "$a" baseline >> "$R/$p-baseline.log" 2>&1 &
if [ "$CH" = challenge ]; then
  python3 "$H/run_quiz.py" "$W" "$H/fixtures/$a.md" challenge "$R/$p/challenge" > "$R/$p-challenge.log" 2>&1 || { echo "CHAIN_FAIL $TAG $p challenge"; exit 1; }
  { python3 "$H/judge_challenge.py" "$R/$p/challenge" "$a" "$R/$p/baseline" && python3 "$H/score_challenge.py" "$R/$p/challenge"; } >> "$R/$p-challenge.log" 2>&1 &
fi
python3 "$H/run_quiz.py" "$W" "$H/fixtures/$b.md" retest "$R/$p/retest" > "$R/$p-retest.log" 2>&1 &&
python3 "$H/judge.py" "$R/$p/retest" "$b" retest "$R/$p/baseline" >> "$R/$p-retest.log" 2>&1
wait; echo "CHAIN_DONE $TAG $p"
