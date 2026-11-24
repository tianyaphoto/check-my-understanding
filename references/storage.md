# Storage Layout

```
<records_dir>/<topic-slug>/checks/
├── sources.md          numbered sources (S1, S2, ...) with link/path and coverage
├── tree.md             the frozen rubric: nodes, weights, ceilings, level descriptors, misconceptions, changelog
├── history.md          one row per finished session: date, kind, mastery %, level per node
├── sessions/
│   └── 2026-11-23-1-baseline.md    question log + state (one file per session)
├── reports/
│   └── 2026-11-23-1-baseline.md    the report shown to the user
└── challenges/
    └── 2026-11-24-1.md             one file per challenge round (only if the user took one)
```

Session kinds: `baseline`, `retest`. The number after the date distinguishes several sessions on the same day.

## Session file

A YAML header holds the resumable state. Update it after every answer.

```markdown
---
topic: raft-consensus
kind: baseline
status: in-progress        # in-progress | paused | complete
budget: 20
asked: 7
target_level: 4
levels: { N1: 3, N2: 2, N3: open, N4: 1, N5: open }   # open = no pass or fail pins it yet
pinned: [N4]
---

## Q1 · N1 · opener
<question text>
Key points: what = <one line>; why = <one line>   (written before reading the answer)
Answer: "it keeps the terminals alive in a background server, so closing the window doesn't kill anything"
Verdict: what yes, why yes
Reveals: -
Assumptions: "closing the window is the only thing that could kill them" (unstated: the server itself never restarts)
Revealed: nothing new
Level: N1 = 3, open (next: L4)

## Q9 · N2 · L4 · choose and say why · probes M2b
<question text with options>
Correct: B (A -> M2b, C -> M2c, D -> conflation with N1). Key point for the reason: <one line>
Answer: "A, idle means nothing is waiting"
Verdict: wrong
Reveals: M2b (idle = safe)
Assumptions: "idle means nothing is waiting"
Revealed: status is inferred by reading the screen, so idle can hide an unknown dialog
Level: N2 = 2, pinned
```

Every entry has all eight lines. `Reveals` is what the answer says about the user (a misconception ID or a gap, `-` if nothing). `Assumptions` records any belief the user's reasoning relied on, in their words, for right answers too (`-` if the answer shows none); the challenge round draws on these lines. `Revealed` is what your feedback told the user; hard rule 4 checks new questions against these lines. `Level` ends with `pinned` once the ladder has settled the node.

To resume: read the header, re-read the logged questions and `Revealed` lines (so nothing repeats or leaks), and continue from `asked + 1`.

## history.md

```markdown
| Date | Kind | Mastery | N1 | N2 | N3 | N4 | N5 |
|---|---|---|---|---|---|---|---|
| 2026-11-23 | baseline | 46% | 4 | 2 | 2 | 1 | – |
| 2026-11-30 | retest | 78% | 3 | 4 | 4 | 3 | 3 |
```

## tree.md changelog

At the bottom of `tree.md`. Append only, and only for factual corrections:

```markdown
## Changelog
- 2026-11-30: N4 L3 descriptor corrected (was wrong about joint consensus). N4 is not like-for-like with the baseline.
```

## Challenge file

`challenges/<date>-<n>.md`. Update it after every step.

```markdown
---
topic: raft-consensus
status: in-progress        # in-progress | paused | complete
based_on: [sessions/2026-11-23-1-baseline.md]
assumptions: 3
current: A2
step: confront
---

## A1 · false · from Q4, Q9 · touches N3, N4
Belief (user's words): "once the leader has written it, it's committed"
Commit: confirmed
Scenario: <the situation you gave>
Prediction: "the entry survives, the leader had it"
Fact given: the new leader overwrites it (S1 §5.4)
Rebuild: "so committed means a majority has it, not the leader" (attempt 1)
Transfer: "our failover runbook assumes the old primary's last writes are safe"
Outcome: revised
Now says: "an entry is safe only once a majority holds it"

## Summary
<the closing table and the pattern line>
```

