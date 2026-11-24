# check-my-understanding

[中文说明](README.zh-CN.md)

A [Claude Code](https://claude.com/claude-code) skill that measures how well you understand a topic. It runs an adaptive quiz with feedback after every answer, then reports a 0-5 level for each concept, a mastery score, and the wrong mental models behind your mistakes, with pointers to what to read. After you study, a retest against the same rubric shows what changed.

It is a measuring instrument, not a tutor. It does not teach a topic from scratch.

## Install

Clone the repository into your skills directory:

```bash
git clone https://github.com/tianyaphoto/check-my-understanding ~/.claude/skills/check-my-understanding
```

To install it for one project only, clone it into `<project>/.claude/skills/check-my-understanding` instead.

Start a new Claude Code session and the skill is available. No dependencies.

## Update

Pull the latest version in the directory you cloned into, then start a new Claude Code session. A session that is already open keeps the version it loaded.

```bash
git -C ~/.claude/skills/check-my-understanding pull
```

- **Your records are safe.** Test records live in your `records_dir`, outside the skill directory, and an update never touches them. Trees and logs written by an older version keep working: a retest or a challenge round uses them as they are.
- **Which version do I have?** `git -C ~/.claude/skills/check-my-understanding log -1 --format='%h %ad %s' --date=short`
- **You edited the skill locally and the pull is refused.** Keep your edits with `git stash`, pull, then `git stash pop`. To drop them instead, run `git checkout .` before pulling.
- **You copied the files instead of cloning.** Delete the directory and install again with the clone command above.

## Use

Say what you want tested, in any language:

- `check my understanding of Raft`
- `test me on this document: docs/design.md`
- `retest me on Raft` (after you have studied the gaps)

On the first run the skill asks where to keep its records and saves the answer to `~/.config/check-my-understanding/config.json`:

```json
{ "records_dir": "~/notes/understanding-checks", "default_questions": 20, "default_target_level": 4 }
```

A baseline is 20 questions and takes about 30 minutes. "I don't know" is a valid answer, and you can say "pause" at any point and resume later.

## How it works

1. **Sources.** Your material is the answer key. Given only a topic name, the skill picks 3-5 authoritative sources and reads them first.
2. **A frozen rubric.** It builds a knowledge tree of 4-8 concepts. Each concept has one checkable capability per level, and the tree is never edited afterwards, so every session is graded on the same scale.
3. **The quiz.** One open "explain it" question per concept places it at level 0-3 without leaking anything. Concepts at level 3 get a scenario question at the target level. The remaining questions test the common misconceptions recorded in the tree.
4. **The report.** Per-concept levels, a mastery score, and one to three root problems, each with the evidence, the consequence in real work, and what to read.
5. **Retest.** New questions in new situations. Each earlier root problem is checked again and reported as resolved, partly resolved, or persisting.
6. **Challenge round (optional).** After a report, say `challenge my assumptions`. See below.

| Level | Meaning |
|---|---|
| 0 | Does not recognize the concept |
| 1 | Has heard of it |
| 2 | Knows what it is |
| 3 | Knows why it is designed that way |
| 4 | Can apply it and knows its limits (default target) |
| 5 | Can trade it off against alternatives |

## Challenge round

The quiz tells you which of your beliefs are wrong. The challenge round makes you find that out yourself, which is what changes how you think. It takes up to three assumptions that your answers exposed, including unstated ones behind correct answers, and runs each through five steps:

1. **Commit.** It quotes what you said and asks whether you hold that belief.
2. **Predict.** It gives a new situation and asks what happens.
3. **Confront.** It tells you what actually happens, with the source, and nothing more.
4. **Rebuild.** You work out what was wrong in your model and state the new one.
5. **Transfer.** You name where the old belief would have misled you in your own work.

It never states the corrected model before you have tried, and it concedes if you defend the assumption with an argument the source supports. The round ends with a table of old and new beliefs and one line on the habit of thought they share. It does not change your levels; the next retest checks whether each change held.

## Evaluation

`evals/` holds the test harness used to develop the skill. A simulated learner with a planted knowledge profile, including two false beliefs, takes a baseline and a retest. An independent session extracts the facts from the transcript, and a script scores the run against the planted profile: measurement accuracy 30, diagnosis 20, retest loop 20, process 15, rubric and records 15.

The quiz and retest scored 100/100, against 92.8 for the version before the redesign, under the same conditions. The challenge round is scored separately (picks the right assumptions 25, method 45, one question per message 15, records and summary 15) and scored 85, 100 and 95 in three runs across two revisions. Read these numbers with care: each configuration ran once, the 100 combines learner chains from different revisions, the fixture material is tidier than real documents, and the last wording changes to the challenge round were not rerun. No human learners were involved.

To run it (needs the `claude` CLI; one learner chain uses roughly 20-55 USD of API-equivalent usage):

```bash
cd evals
./run_chain.sh mytag /path/to/skill p1   # learner with two wrong mental models
./run_chain.sh mytag /path/to/skill p3   # learner who memorized definitions
python3 score.py runs/mytag

./run_chain.sh mytag2 /path/to/skill p1 challenge   # baseline -> challenge round -> retest
```

Do not kill a chain and rerun it under the same tag: leftover sessions write into the new run.

## License

[MIT](LICENSE)
