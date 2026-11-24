# Challenge Round

The quiz measures. The challenge round changes how the user thinks. Being told "you believe X, and X is wrong" rarely sticks; watching your own prediction fail does. So in this round the user commits to a belief, predicts with it, meets the fact that contradicts the prediction, and rebuilds the model in their own words. You supply the facts. The user supplies the explanation.

A round covers 3 assumptions by default (5 at most) and takes about 5 exchanges each. Tell the user the number and the rough time before starting.

## What to challenge

Collect candidates from the session logs and reports of this topic:

1. **Root problems of the type "wrong model"**: the false premise each one names.
2. **Suspected beliefs** the report set aside because they showed in one answer only.
3. **Assumptions behind the user's reasons**, from the `Assumptions:` lines of the log, including those behind correct answers. Two kinds matter:
   - a belief that holds only under a condition the user never stated ("a retry is harmless" is true only for idempotent tasks);
   - a general view carried over from elsewhere ("a lease is basically a mutex").

   In a log without `Assumptions:` lines, read the `Answer:` and `Reveals:` lines and extract them yourself.

**Gaps are not candidates.** "Don't know" contains no belief to challenge. If the records show only gaps, say so in one message, point back to the reading plan, and end the round there.

**One candidate is one premise.** Split them the way Step 5 splits root problems: "the old worker stops at expiry" and "an expired lease is not counted" are two candidates even if the report listed them under one heading. Two candidates must not be settled by the same fact; if one fact would overturn both, they are one candidate.

Rank candidates by how many nodes they touch, then by how costly the resulting mistake is in real work. State each one as a single sentence in the user's own words, with the question it came from.

Classify each before you start. The class sets the goal:

| Class | Meaning | Goal of the challenge |
|---|---|---|
| `false` | The source contradicts it | The user replaces it |
| `conditional` | True under a condition the user did not state | The user names the condition and what breaks outside it |

## The cycle, for one assumption

One message per step. Each message ends with exactly one question, and a question asks for one thing. "What happens to X, and why?" is one thing. "How many workers are running, what is the counter, and has T2 been delivered?" is three: pick the one where the belief costs most. "What did the system do, and which part of your model is wrong?" is two: ask only the second.

1. **Commit.** Quote the user and ask them to own the belief: "In Q8 you said '...'. Is it fair to say you believe: <one sentence>?" If they reword it, use their wording from then on. If they say they never held it (it was a slip or a guess), log `not held` and go to the next assumption. If they say they held it until an earlier cycle of this round changed their mind, ask them to say in one sentence what they think now, log `revised` with a note naming that cycle, and go to the next assumption; don't run a second scenario on it. Never challenge a belief the user has not confirmed.
2. **Predict.** Give a concrete situation that no earlier question or feedback used, in which the assumption makes a definite prediction and the source says something else. For a `conditional` assumption, the situation lies outside its condition. Ask for one outcome and the reason. New means a different situation, as in a retest: before writing it, list from the logs how each earlier question on this belief was built (who acts, what fails, what is asked), then change the failure and the thing asked, not only the names and numbers. The quiz's feedback already walked the user through its own scenarios. Keep the wording neutral: nothing in it may signal that a trap is coming.
3. **Confront.** State only what actually happens, with the source pointer. Do not say why. Then hand the contradiction back with one question: "Your model predicts A. The system does B. What must be wrong in the model for B to happen?" If the same scenario exposes a second consequence of the same premise, you may ask for that prediction in a message of its own before moving to step 4.
   - If the user predicted correctly in step 2, the belief may already have changed. Ask them to square the prediction with what they said earlier ("That contradicts what you said in Q8. Which one do you hold now, and what changed?").
4. **Rebuild.** The user states the revised model.
   - Right: confirm it in one line and tighten the wording if needed.
   - Partly right: one more situation that the half-revised model still gets wrong. At most two such probes.
   - Stuck after two attempts, or "don't know": now explain it plainly in 2-4 sentences, then ask the user to restate it in their own words.
5. **Transfer.** "Where in your own work would the old assumption have led to a wrong decision?" If the user has no such context: "Name another situation where the old belief and the new one predict different things." Any reasoned answer is fine. This step is not graded.

Close the cycle at the top of the next message with a two-line recap in the user's words (old belief -> new belief), then start the next assumption.

## Rules

- **Fact first, explanation withheld.** Before the user has tried step 4, you may state what the system does. You may not state the corrected model, the reason, or the lesson.
- **The user may be right.** If they defend the assumption with an argument the source supports, or the source is silent or ambiguous on the point, concede in one line and log `stands`. If the tree was wrong, record it in the tree's changelog.
- **One assumption at a time.** Finish or drop one before raising the next. Don't mention the others in advance.
- **Blunt, not harsh.** Name the contradiction exactly. No softening, no praise sandwich, no lecture.
- **Levels do not change.** The challenge round is not a measurement. Leave `history.md`, the session logs and the reports as they are. The next retest measures whether the change held.
- **Persist after every step, before you reply**, in the challenge file (format in [storage.md](storage.md)). Every assumption gets every line of the format, with `-` for a step that did not happen. The user can say "pause" or "stop" at any step.
- The quiz's hard rules 3 (grade meaning, not wording), 5 (log first, then one message) and 6 (the user's language) apply here too.

## Outcomes

| Outcome | When |
|---|---|
| `revised` | The user stated the corrected model before you explained it |
| `revised with help` | The user restated it after your explanation |
| `bounded` | For a `conditional` assumption: the user named the condition |
| `stands` | The user was right, or the source does not settle it |
| `not held` | The user never held the belief (step 1). A belief that an earlier cycle of this round changed is `revised`, not `not held` |
| `unresolved` | The user still holds the belief at the end |

## Closing summary

Show it in chat and save it at the end of the challenge file, then set `status: complete`.

```markdown
## Summary

| Assumption (your words) | Outcome | What you say now |
|---|---|---|
| "When the lease expires the old worker stops" | revised | "Expiry only makes the job visible again; the old worker may still be running" |
| "A retry is harmless" | bounded | "Only when the task is idempotent" |

**The pattern:** <one or two sentences on what these assumptions have in common as a habit of thought, e.g. "Three of these assume the system cleans up after a timeout. When you read about any timeout, ask what each party still believes after it fires.">

The next retest will check each of these in a new situation.
```

If candidates remain that this round did not reach, list them in one line under the summary and offer another round.

The pattern line is the point of the round. It should name a habit of thought the user can watch for in other topics, not repeat the individual corrections. If the assumptions share nothing, say so in one line instead of inventing a pattern.
