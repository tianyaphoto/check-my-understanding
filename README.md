# check-my-understanding

[中文说明](README.zh-CN.md)

A [Claude Code](https://claude.com/claude-code) skill that measures how well you understand a topic. It runs an adaptive quiz with feedback after every answer, then reports a 0-5 level for each concept, a mastery score, and the wrong mental models behind your mistakes, with pointers to what to read. After you study, a retest against the same rubric shows what changed.

It is a measuring instrument, not a tutor. It does not teach a topic from scratch.

## Install

Clone the repository into your skills directory:

```bash
git clone https://github.com/tianyaphoto/check-my-understanding ~/.claude/skills/check-my-understanding
```

To install it for one project only, clone it into `<project>/.claude/skills/check-my-understanding` instead. Update with `git pull` in that directory.

Start a new Claude Code session and the skill is available. No dependencies.

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

| Level | Meaning |
|---|---|
| 0 | Does not recognize the concept |
| 1 | Has heard of it |
| 2 | Knows what it is |
| 3 | Knows why it is designed that way |
| 4 | Can apply it and knows its limits (default target) |
| 5 | Can trade it off against alternatives |

## Evaluation

`evals/` holds the test harness used to develop the skill. A simulated learner with a planted knowledge profile, including two false beliefs, takes a baseline and a retest. An independent session extracts the facts from the transcript, and a script scores the run against the planted profile: measurement accuracy 30, diagnosis 20, retest loop 20, process 15, rubric and records 15.

The current version scored 100/100 and the previous version 92.8, under the same conditions. Read these numbers with care: each version ran once, the 100 combines two learner chains that ran on consecutive revisions, and the fixture material is tidier than real documents. No human learners were involved.

To run it (needs the `claude` CLI; one learner chain uses roughly 20-55 USD of API-equivalent usage):

```bash
cd evals
./run_chain.sh mytag /path/to/skill p1   # learner with two wrong mental models
./run_chain.sh mytag /path/to/skill p3   # learner who memorized definitions
python3 score.py runs/mytag
```

Do not kill a chain and rerun it under the same tag: leftover sessions write into the new run.

## License

[MIT](LICENSE)
