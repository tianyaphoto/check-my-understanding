#!/usr/bin/env python3
"""usage: score.py <run_tag_dir>   (expects p1/baseline p1/retest p3/baseline p3/retest each with judge.json)"""
import json, sys, os
R = sys.argv[1]; TARGET = 4
J = {k: json.load(open(f"{R}/{k}/judge.json")) for k in ["p1/baseline", "p1/retest", "p3/baseline", "p3/retest"]}
clip = lambda x: max(0.0, min(1.0, x)); rate = lambda a, b: (len(a) if isinstance(a, list) else a) / max(1, b)
detail = {}
def acc(j):
    tw = te = 0
    for n in j["nodes"]:
        w = 2 if n["weight"] == "core" else 1; m, t = n["measured"], n["truth"]
        e = 2 if not isinstance(m, int) else (0 if (m >= TARGET and t >= TARGET) else abs(m - t))
        tw += w; te += w * e
    mae = te / max(1, tw); return clip(1 - mae / 2), round(mae, 2)
A = 0
for k, j in J.items(): s, mae = acc(j); A += 30 / 4 * s; detail[f"A {k} MAE"] = mae
b1, b3 = J["p1/baseline"], J["p3/baseline"]
pts = {"root": 7, "mentioned": 3, "missed": 0}; found = {r["id"]: r["found"] for r in b1["roots"]}
B = pts[found.get("R1", "missed")] + pts[found.get("R2", "missed")] - 3 * len(b1["false_roots"])
B = max(0, B) + (3 if b3["gap_summary_ok"] else 0) + max(0, 3 - 3 * len(b3["false_roots"]))
detail["B roots"] = found; detail["B false_roots"] = [len(b1["false_roots"]), len(b3["false_roots"])]
r1, r3 = J["p1/retest"]["retest"], J["p3/retest"]["retest"]
ch = r1["changes"]; C = 6 * rate([c for c in ch if c["reported_direction"] == c["truth_direction"]], len(ch))
st = {r["id"]: r["reported"] for r in r1["roots_status"]}
C += {"resolved": 3, "partly": 1.5}.get(st.get("R1"), 0) + {"persists": 3, "partly": 1.5}.get(st.get("R2"), 0)
C += 0 if r1["mastered_declared"] else 2
C += 6 if r3["mastered_declared"] else 6 * 0.7 * r3["core_nodes_at_target"] / max(1, r3["core_nodes_total"])
detail["C"] = {"dir": f'{sum(c["reported_direction"]==c["truth_direction"] for c in ch)}/{len(ch)}', "roots": st,
               "p1 mastered": r1["mastered_declared"], "p3 mastered": r3["mastered_declared"],
               "p3 at target": f'{r3["core_nodes_at_target"]}/{r3["core_nodes_total"]}'}
D = E = 0
for k, j in J.items():
    p, g = j["process"], j["integrity"]; q = max(1, p["question_msgs"])
    pen = rate(p["multi_question_msgs"], q) + rate(p["feedback_missing"], p["feedback_expected"]) + 0.5 * rate(p["feedback_without_source"], p["feedback_expected"]) \
        + rate(p["mcq_without_idk"], p["mcq_total"]) + rate(p["hints_before_answer"], q) + 0.5 * rate(p["no_progress_marker"], q)
    if p["budget"] and (p["questions_asked"] - p["budget"]) / p["budget"] > 0.15: pen += 0.3
    D += 15 / 4 * clip(1 - pen); detail[f"D {k} penalty"] = round(pen, 2)
    asked = max(1, p["questions_asked"])
    pen = 2 * rate(g["wrong_keys"], asked) + 2 * rate(g["leaks_counted"], asked) + rate(g["mislabeled_levels"], asked) + 0.1 * len(g["log_fields_missing"])
    if abs(g["mastery_reported"] - g["mastery_recomputed"]) > 2: pen += 0.2
    pen += 0.2 * (not g["untested_rule_stated"]) + 0.2 * (not g["history_row_written"]) + 0.2 * (not g["report_saved"])
    if j["retest"]: pen += 2 * rate(j["retest"]["reused_questions"], asked) + 0.5 * bool(j["retest"]["rubric_edited"])
    E += 15 / 4 * clip(1 - pen); detail[f"E {k} penalty"] = round(pen, 2)
res = {"A 测量准确/30": round(A, 1), "B 诊断/20": round(B, 1), "C 复测闭环/20": round(C, 1), "D 流程/15": round(D, 1), "E 量尺与记录/15": round(E, 1)}
res["总分/100"] = round(A + B + C + D + E, 1)
print(json.dumps(res, ensure_ascii=False, indent=1)); print(json.dumps(detail, ensure_ascii=False, indent=1))
json.dump({"score": res, "detail": detail}, open(f"{R}/score.json", "w"), ensure_ascii=False, indent=1)
