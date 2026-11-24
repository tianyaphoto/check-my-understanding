#!/usr/bin/env python3
"""Drive one quiz: an examiner session (real skill) talks to a learner session (planted knowledge).
usage: run_quiz.py <work_dir> <notes_file> <baseline|retest|challenge> <out_dir>"""
import json, subprocess, sys, uuid, glob, os, time, tempfile, shutil
work, notes, kind, out = sys.argv[1:5]
FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
os.makedirs(work, exist_ok=True); os.makedirs(out, exist_ok=True)
if not os.path.exists(f"{work}/material.md"): shutil.copy(f"{FIX}/material.md", work)
learner_sys = open(f"{FIX}/" + ("learner_challenge.md" if kind == "challenge" else "learner_common.md")).read() + open(notes).read()
learner_cwd = tempfile.mkdtemp(prefix="cmu-learner-")
ex_id, le_id = str(uuid.uuid4()), str(uuid.uuid4())
EX_MODEL = os.environ.get("EX_MODEL")
SKILL_DIR = os.environ.get("SKILL_DIR")   # set -> isolated mode: project-level skill copy, no user settings
if SKILL_DIR and not os.path.exists(f"{work}/.claude/skills"):
    shutil.copytree(SKILL_DIR, f"{work}/.claude/skills/check-my-understanding")
    if os.environ.get("EVAL_CLAUDE_MD"): shutil.copy(os.environ["EVAL_CLAUDE_MD"], f"{work}/CLAUDE.md")  # optional: examiner's user instructions

def call(args, prompt, cwd, tries=6):
    for i in range(tries):
        p = subprocess.run(["claude", "-p", "--output-format", "json"] + args, input=prompt, text=True,
                           capture_output=True, cwd=cwd, timeout=1200)
        try:
            j = json.loads(p.stdout)
            if not j.get("is_error") and j.get("result"): return j["result"], j.get("total_cost_usd", 0)
        except Exception: pass
        sys.stderr.write(f"[retry {i}] rc={p.returncode} out={p.stdout[:300]} err={p.stderr[:300]}\n"); time.sleep(30 * (i + 1))
    raise SystemExit("call failed")

def examiner(msg, first):
    a = ["--permission-mode", "bypassPermissions"] + (["--session-id", ex_id] if first else ["--resume", ex_id])
    if EX_MODEL: a += ["--model", EX_MODEL]
    if SKILL_DIR: a += ["--setting-sources", "project"]
    return call(a, msg, work)

def learner(msg, first):
    a = ["--model", "sonnet", "--tools", "", "--setting-sources", "project", "--system-prompt", learner_sys]
    a += ["--session-id", le_id] if first else ["--resume", le_id]
    return call(a, msg, learner_cwd)

def reports():
    if kind == "challenge":   # done when a challenge file is marked complete
        return {x for x in glob.glob(f"{work}/records/**/challenges/*.md", recursive=True) if "status: complete" in open(x).read()}
    return set(glob.glob(f"{work}/records/**/reports/*.md", recursive=True))

first_msg = {"baseline": "测测我对这份材料的理解：material.md（就在当前目录）。测试记录放在当前目录的 records/ 下面。",
             "challenge": "挑战一下我在潮汐锁测验里暴露出来的假设。测试记录在当前目录的 records/ 下面，材料是当前目录的 material.md。",
             "retest": "材料我重新学过了，复测一下潮汐锁。测试记录在当前目录的 records/ 下面，材料还是当前目录的 material.md。"}[kind]
before = reports(); cost = 0.0; t0 = time.time()
tr = open(f"{out}/transcript.md", "w")
def log(who, n, text): tr.write(f"\n\n### {who} #{n}\n\n{text}"); tr.flush()
msg = first_msg; log("学习者", 0, msg); done = False
for n in range(1, 61):
    reply, c = examiner(msg, n == 1); cost += c; log("考官", n, reply)
    if reports() - before: done = True; break
    msg, c = learner(reply, n == 1); cost += c; log("学习者", n, msg)
tr.close()
rec = [os.path.dirname(os.path.dirname(x)) for x in reports()][:1]
if rec:
    dst = f"{out}/checks"; shutil.rmtree(dst, ignore_errors=True); shutil.copytree(rec[0], dst)
json.dump({"done": done, "examiner_turns": n, "cost_usd": round(cost, 2), "minutes": round((time.time()-t0)/60, 1),
           "examiner_session": ex_id, "new_reports": sorted(os.path.basename(x) for x in reports() - before)},
          open(f"{out}/meta.json", "w"), ensure_ascii=False, indent=1)
print(open(f"{out}/meta.json").read())
