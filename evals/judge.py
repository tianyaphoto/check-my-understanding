#!/usr/bin/env python3
"""usage: judge.py <quiz_out_dir> <profile> <baseline|retest> [prev_quiz_out_dir]  -> writes judge.json"""
import sys, os, glob, json, subprocess, tempfile, re
out, profile, kind = sys.argv[1:4]; prev = sys.argv[4] if len(sys.argv) > 4 else None
H = os.path.dirname(os.path.abspath(__file__)); rd = lambda p: open(p).read()
parts = [rd(f"{H}/judge_prompt.md").replace("{profile}", profile).replace("{kind}", kind)]
parts += ["# 【真值表】\n" + rd(f"{H}/fixtures/truth.md"), "# 【材料原文】\n" + rd(f"{H}/fixtures/material.md")]
c = f"{out}/checks"
for f in ["sources.md", "tree.md", "history.md"]:
    if os.path.exists(f"{c}/{f}"): parts.append(f"# 【考官文件 {f}】\n" + rd(f"{c}/{f}"))
for sub in ["sessions", "reports"]:
    for f in sorted(glob.glob(f"{c}/{sub}/*.md")): parts.append(f"# 【考官文件 {sub}/{os.path.basename(f)}】\n" + rd(f))
if prev and os.path.exists(f"{prev}/checks/tree.md"):
    parts.append("# 【上一场结束时的 tree.md（用于判断量尺是否被改动）】\n" + rd(f"{prev}/checks/tree.md"))
parts.append(f"# 【本场完整对话记录】（学习者 #0 是开场请求；复测时，考官文件里文件名靠后的 session / report 才是本场）\n" + rd(f"{out}/transcript.md"))
prompt = "\n\n".join(parts) + "\n\n现在输出 JSON。"
for i in range(3):
    p = subprocess.run(["claude", "-p", "--model", os.environ.get("JUDGE_MODEL", "opus"), "--tools", "", "--setting-sources", "project",
                        "--output-format", "json"], input=prompt, text=True, capture_output=True, cwd=tempfile.mkdtemp(), timeout=1500)
    try:
        r = json.loads(p.stdout)["result"]; r = r[r.index("{"): r.rindex("}") + 1]
        r = re.sub(r"/\*.*?\*/", "", r, flags=re.S)
        j = json.loads(r); json.dump(j, open(f"{out}/judge.json", "w"), ensure_ascii=False, indent=1); print("judged", out); break
    except Exception as e: sys.stderr.write(f"judge retry {i}: {e} {p.stdout[:200]} {p.stderr[:200]}\n")
else: raise SystemExit("judge failed")
