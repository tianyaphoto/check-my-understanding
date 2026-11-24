#!/usr/bin/env python3
"""usage: score_challenge.py <challenge_out_dir>   scores a judged challenge round out of 100"""
import json, sys
j = json.load(open(f"{sys.argv[1]}/judge.json")); ch = j["challenges"]; held = [c for c in ch if c.get("learner_confirmed")]
# A. picks the right things (25): both planted roots challenged; nothing the learner doesn't hold, no gaps, no true beliefs attacked
A = 10 * sum(any(c["maps_to"] == r for c in ch) for r in ("R1", "R2"))
bad = sum(c["maps_to"] == "not_held" and c.get("dropped_when_not_held") is not True for c in ch) + len(j["gaps_challenged"]) \
      + sum(not c["is_actually_false_or_conditional"] for c in ch)
A += max(0, 5 - 2.5 * bad)
# B. method (45): averaged over the assumptions the learner confirmed
def m(c):
    return (5 * c["commit_asked"] + 8 * (c["prediction_asked"] and c["scenario_is_new"]) + 4 * (not c["scenario_hinted"])
            + 12 * (not c["explained_before_attempt"]) + 8 * (c["learner_stated_revision"] and c["revision_correct"])
            + 5 * c["transfer_asked"] + 3 * c["recap_given"])
B = sum(m(c) for c in held) / len(held) if held else 0
# C. discipline (15)
msgs = max(1, 5 * len(ch))
C = max(0, 15 - 15 * len(j["multi_question_msgs"]) / msgs * 3 - 5 * len(j["wrong_facts"]) - (0 if j["announced_count_and_time"] else 2))
# D. records and summary (15)
s, f = j["summary"], j["file"]
D = 3 * s["shown"] + 3 * bool(s["pattern_line"]) * s["pattern_is_general"] + 2 * f["exists"] + 1 * f["status_complete"] + 2 * f["all_steps_logged"] \
    + 2 * (not j["levels_changed"]) + 2 * (sum(c["outcome_fits"] for c in ch) / len(ch) if ch else 0)
r = {"A 选对假设/25": round(A, 1), "B 方法/45": round(B, 1), "C 纪律/15": round(C, 1), "D 记录与总结/15": round(D, 1)}
r["总分/100"] = round(sum(r.values()), 1); print(json.dumps(r, ensure_ascii=False, indent=1))
json.dump(r, open(f"{sys.argv[1]}/score.json", "w"), ensure_ascii=False, indent=1)
