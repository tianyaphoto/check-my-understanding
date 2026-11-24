#!/usr/bin/env python3
"""usage: judge_challenge.py <challenge_out_dir> <notes_profile> <prev_quiz_out_dir>  -> writes judge.json"""
import sys, os, glob, json, subprocess, tempfile, re
out, profile, prev = sys.argv[1:4]
H = os.path.dirname(os.path.abspath(__file__)); rd = lambda p: open(p).read()
parts = [rd(f"{H}/judge_challenge_prompt.md"), "# 【真值表】\n" + rd(f"{H}/fixtures/truth.md"),
         f"# 【学习者的真实想法（画像 {profile}）】\n" + rd(f"{H}/fixtures/{profile}.md"), "# 【材料原文】\n" + rd(f"{H}/fixtures/material.md")]
parts.append("# 【挑战前的 history.md】\n" + rd(f"{prev}/checks/history.md"))
for sub in ["sessions", "reports"]:
    for f in sorted(glob.glob(f"{prev}/checks/{sub}/*.md")): parts.append(f"# 【挑战前的测验文件 {sub}/{os.path.basename(f)}】\n" + rd(f))
c = f"{out}/checks"
if os.path.exists(f"{c}/history.md"): parts.append("# 【挑战后的 history.md】\n" + rd(f"{c}/history.md"))
for f in sorted(glob.glob(f"{c}/challenges/*.md")): parts.append(f"# 【挑战文件 {os.path.basename(f)}】\n" + rd(f))
parts.append("# 【挑战环节完整对话记录】（学习者 #0 是开场请求）\n" + rd(f"{out}/transcript.md"))
prompt = "\n\n".join(parts) + "\n\n现在输出 JSON。"
for i in range(3):
    p = subprocess.run(["claude", "-p", "--model", os.environ.get("JUDGE_MODEL", "opus"), "--tools", "", "--setting-sources", "project",
                        "--output-format", "json"], input=prompt, text=True, capture_output=True, cwd=tempfile.mkdtemp(), timeout=1500)
    try:
        j0 = json.loads(p.stdout); r = j0["result"]; r = r[r.index("{"): r.rindex("}") + 1]
        j = json.loads(re.sub(r"/\*.*?\*/", "", r, flags=re.S)); j["_judge_cost_usd"] = round(j0.get("total_cost_usd", 0), 2)
        json.dump(j, open(f"{out}/judge.json", "w"), ensure_ascii=False, indent=1); print("judged", out); break
    except Exception as e: sys.stderr.write(f"judge retry {i}: {e} {p.stdout[:200]} {p.stderr[:200]}\n")
else: raise SystemExit("judge failed")
