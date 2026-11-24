# Rubric and Question Design

## The generic level scale

| Level | Name | Kind of capability | The user can... |
|---|---|---|---|
| 0 | Unaware | none | Not recognize the concept |
| 1 | Heard of it | recognition | Recognize the term and roughly what it is for, but not explain it |
| 2 | Knows what | description | Describe what it is or how it works (the steps, the definition) |
| 3 | Knows why | rationale | Explain why it is designed this way, i.e. what problem it prevents |
| 4 | Can apply, knows limits | prediction, boundary | Predict behavior in a new scenario; say when it breaks or doesn't apply |
| 5 | Can trade off | comparison | Compare it with an alternative and argue the costs |

The default target is 4. Level 3 is not mastery: someone who can recite the rationale still misjudges real scenarios.

## Writing a node

- **One capability per level, of the kind in the table.** Write the single statement the user must be able to make. If a section of the source has several facts of the same kind, pick the one that carries the most weight for L2-L5 and list the rest under `Also:`; they are extra angles for fresh questions at the same level, not extra requirements.
- **Depth, not obscurity.** "Knows the config key name" is L2 however rare it is. If you catch yourself putting a harder-to-remember fact at L4, it belongs under `Also:` at L2.
- **Ceiling.** If the sources say nothing about boundaries or trade-offs for a node, stop the descriptors there and write `ceiling: N`.
- **Misconceptions are false beliefs, stated as the user would state them.** Where one false belief damages several nodes, give it one ID and list it under each node; that is a candidate root problem. Tag each with the level it breaks (`M3b @L4`). Most live at L4: people who can describe a mechanism still predict its behavior wrongly.
- **Choose the L4 capability where the misconceptions are.** If a node has several boundary facts, the L4 descriptor is the one a recorded misconception contradicts; the others go under `Also:`.

Worked example (tree.md format):

```markdown
### N3. Log replication and commitment (core, weight 2, ceiling 5)
Sources: S1 §5.3-5.4, S2 ch.3
- L1: knows the leader sends log entries to followers
- L2: describes AppendEntries: leader sends entries, followers append, leader marks committed after a majority acks
- L3: explains why commitment needs a majority: any two majorities overlap, so a future leader must hold the entry
  Also: why the consistency check (prevLogIndex/prevLogTerm) exists
- L4: predicts what happens to an entry on a minority of nodes when the leader crashes (it may survive or be overwritten)
  Also: a leader can't commit entries from earlier terms just by counting replicas
- L5: argues the latency cost of majority acks against async replication
Misconceptions:
- M-A (also N4): "committed = written to the leader's disk"
- M3b: "once an entry is on a majority it is committed, regardless of term"
- M3c: "followers vote on each entry"
```

## Grading rules (the same in every session)

| Evidence | Effect on the node |
|---|---|
| Opener answer | Level 0-3 by the highest descriptor the answer fully meets: nothing -> 0, what it is for -> 1, how it works -> 2, plus the reason -> 3 |
| Opener answer that states something false about how it works | Level 1 at most, and the false statement is diagnostic evidence |
| Clean pass on a scenario question at level L >= 4 (correct choice **and** correct reason) on a node placed at 3 | Level is L |
| Correct choice with a wrong or missing reason | Not a pass. The wrong reason is diagnostic evidence |
| Partly correct (the key idea is present but imprecise, or half of it is missing) | Certifies the level below the one targeted |
| Wrong, or "don't know", on a scenario question | Level stays where it was |
| Correct, with a correct reason, on a misconception probe for a node placed below 3 | Level unchanged; log `can reason it out` |
| A pass whose answer an earlier feedback in this session revealed | No effect. Mark it `learned in session` |

Before reading a short answer, write down the key point it must contain. Grade against that point and the node's descriptor, not against your impression of the user. The same answer quality gets the same level in the baseline and in every retest.

## Gap types and remedies

Classify every root problem into one of these types. The remedy differs by type.

| Gap type | Signature in the answers | Remedy to prescribe |
|---|---|---|
| Missing concept | "Don't know", or wrong at levels 1-2 | Read the section that introduces it, then restate it in your own words |
| Conflation | Picks the distractor that belongs to a neighboring concept; uses two terms interchangeably | Build a side-by-side comparison: what each guarantees, where they differ |
| Wrong model | Confident wrong answers that all follow from one false belief | State the false belief, then find the sentence in the source that contradicts it and the scenario where the two predictions differ |
| Memorized, not understood | Right at level 2, "don't know" or wrong at level 3; can list the steps but not what each step prevents | For each step, ask "what goes wrong if this step is removed?" |
| Can't transfer | Right at level 3, wrong on level-4 scenarios | Walk through 2-3 concrete failure scenarios step by step |
| Fuzzy boundaries | Overgeneralizes; says it works where it doesn't, or misses its preconditions | List the assumptions it relies on, and what breaks when each one fails |

## Multiple-choice rules

- 4 options plus "E. I don't know". Exactly one correct answer; check each distractor against the source to be sure it is really wrong.
- **Every distractor maps to a named misconception** from the tree (log it as e.g. `B -> M3b`). A wrong pick is then evidence of a specific wrong model, not just "wrong".
- Options of similar length and grammatical form. Vary the correct letter. No "all of the above" or "none of the above". The correct option must not be the only careful-sounding one.
- **The stem must not teach.** Don't define a term or explain a mechanism in the question when that explanation is itself something the node tests.
- For levels 3-5, use a scenario and end with "Pick one and give the reason in one sentence."

Example (targets N3, L4):

> **Q9/20** In a 5-node Raft cluster, the term-3 leader appends entry X and replicates it to one follower (2 of 5 nodes now have X), then crashes. A new leader is elected for term 4. What happens to X? Pick one and give the reason in one sentence.
> A. X is committed, because it was replicated before the crash
> B. X may survive or be overwritten, depending on which node becomes the new leader
> C. X is always discarded, because entries from old terms are deleted on election
> D. X is committed as soon as any 3 nodes have it, even if they are from term 3
> E. I don't know

Correct: B. A -> M-A, C -> fuzzy boundary on term handling, D -> M3b. Key point for the reason: X is on a minority, so a node without X can win the election and overwrite it.

## Opener and short-answer rules

- The opener asks for "how it works and why" in one or two sentences, and names the concept without describing it. Before reading the answer, write the two key points (the "what" and the "why") from the node's L2 and L3 descriptors.
- Spoken answers are terse. Grade the idea: "worker dies, lease runs out, job comes back, nobody has to track who's alive" fully meets "what" and "why".
- Apart from the opener: one question, one capability. Don't ask "why, and what are the limits?" in one go.
