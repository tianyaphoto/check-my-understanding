# Report Formats

Write reports in the user's language. Show the report in chat and save it to `checks/reports/`.

## Baseline report

```markdown
# <Topic>: baseline (<date>)

**Verdict:** <one sentence: where you stand and the single biggest problem>
**Mastery:** 46% of target (target level 4) · 20 questions · 5 "don't know"

## Diagnosis

### 1. <Blunt one-line verdict naming the wrong mental model>
- **Evidence:** Q4 you chose A ("committed = on the leader's disk"); Q9 you said X is safe because it was replicated; Q14 ...
- **Consequence:** <the concrete wrong decision this causes in real work>
- **Gap type:** Memorized, not understood
- **Fix:** Read S1 §5.3-5.4. While reading, keep asking: "If the leader dies right now, which entries are guaranteed to survive, and why?"

### 2. ...
(at most 3, ranked by impact)

## Concept levels

| Concept | Level | Target | |
|---|---|---|---|
| N1 Leader election | ████░ 4 | 4 | ✓ |
| N3 Log replication | ██░░░ 2 | 4 | ← root problem 1 |
| N6 Client shortcuts (supporting) | ██░░░ 2 | 3 (ceiling) | |

Every level in this table equals the level in the session log. If a node got no question, show it as `untested`, count it as 0 in the mastery score, and say so under the table.

**Strengths:** <one line>

## Missed questions
(only wrong, partial, and "don't know"; one line each, since each was already explained as feedback)

- **Q4** (A, correct C): <the key point in one line> -> root problem 1

## Reading plan
1. S1 §5.3-5.4: fixes root problem 1 (about 20 min)
2. ...
Retest when you're done; it will focus on N3 and N5.
```

## Retest report

Same structure, with these additions placed after the verdict:

```markdown
**Mastery:** 46% -> 78% (target level 4)

## What changed

| Concept | Before | Now | |
|---|---|---|---|
| N3 Log replication | 2 | 4 | ↑ reached target |
| N1 Leader election | 4 | 3 | ↓ check: earlier guess, or forgotten? |

## Previous root problems
1. "Raft as elect-a-boss": **resolved**. Q3 put you in a scenario where the old model predicts "the entry is safe"; you predicted the overwrite and gave the reason.
2. "...": **persists**. Q11: you still chose the answer the old model predicts ...

Judge each previous root problem by the question that targeted it in this retest, not by whether the node's level went up.
```

Then give the diagnosis of the remaining gaps (new or persisting), the node table, the missed questions, and the reading plan. If every core node is at target, open with a plain "Mastered." and offer a stretch target or a spaced check-up instead of a reading plan.
