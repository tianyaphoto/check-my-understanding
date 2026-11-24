---
name: check-my-understanding
description: "Measure how well the user understands a topic or a piece of material with an adaptive quiz and immediate feedback, then report a 0-5 level per concept, a mastery score, and a diagnosis of the root misconceptions with reading pointers. Supports a baseline -> study -> retest loop against a frozen rubric until every core concept reaches the target level. Use when the user wants to check, test, assess, or find the gaps in their understanding: 'check my understanding of X', 'test me on X', 'find my blind spots', 'retest me', '测测我', '摸底', '复测', '看看我对 X 理解到什么程度'. Not for teaching a topic from scratch or one-off factual questions."
---

# Check My Understanding

This skill is a **measuring instrument with immediate feedback, not a lecture**. Its job is to find exactly where the user's understanding breaks, correct each answer on the spot, say bluntly what the pattern of mistakes means, and drive a loop:

**baseline test -> user studies the gaps -> retest -> ... -> mastered**

Two properties decide whether the instrument is any good, and every rule below serves one of them:

1. **The levels are true.** A reported level matches what the user can actually do, and means the same thing in every session.
2. **The diagnosis is actionable.** It names the wrong mental model behind the mistakes, so the user knows what to fix.

## Hard rules during a quiz

1. **Feedback on the previous answer, then exactly one new question, then stop.** One question per message. Show progress like `Q7/20`. Never give hints before an answer.
2. **"I don't know" is a valid answer and is encouraged.** Say so once at the start. Every multiple-choice question ends with an "I don't know" option. Guesses pollute the measurement.
3. **Grade meaning, not wording.** The user may answer by voice and the transcription may be wrong. If an answer is garbled and the verdict depends on it, restate what you understood and ask them to confirm. That does not count as a question.
4. **Never ask what you have already given away.** Before writing each question, check it against the `Revealed` lines in this session's log and against every question in earlier session logs. A question whose answer a feedback already stated, or that repeats an earlier question, measures memory of this conversation, not understanding.
5. **Persist after every answer, before you reply** (see [references/storage.md](references/storage.md)), so the quiz can pause and resume at any point. Write the log first; the message with the feedback and the next question is the last thing in the turn, in one piece. Never split feedback and question around a file write.
6. **Use the user's language** for all questions, reports, and files. Technical terms may keep their original form.

## Configuration

Resolve the records directory in this order:

1. A location the user names in the current conversation.
2. `records_dir` in `~/.config/check-my-understanding/config.json`.
3. Neither: ask once ("Where should I keep test records? Default: `./understanding-checks/`"), then write the answer to the config file so you never ask again.

Optional keys in the same file, with defaults: `"default_questions": 20`, `"default_target_level": 4`.

Records for a topic live in `<records_dir>/<topic-slug>/checks/`. The `checks/` subfolder keeps them from colliding with other tools that use the same topic folder. File formats are in [references/storage.md](references/storage.md).

## Workflow

### Step 0: Locate the topic and decide the mode

- Derive a short kebab-case slug for the topic. List `<records_dir>` and fuzzy-match existing topic folders (e.g. `raft` vs `raft-consensus`). On a close match, ask whether it is the same topic.
- An unfinished session exists (`status: in-progress` or `paused`): offer to resume it.
- A finished session exists: this is a **retest** (go to Step 6).
- Nothing exists: this is a **baseline** (Steps 1-5).

### Step 1: Gather the sources (baseline only)

- **User gave material** (file, link, notes, a chapter): read all of it. It defines the scope and is the answer key. You may add an outside source only to fill an obvious hole, and must label it as outside.
- **User gave only a topic name**: search the web and choose **3-5 authoritative sources**. Prefer primary sources (official docs, the original paper, the spec, a widely used textbook, a recognized expert's long-form explanation) over SEO summaries. Read them before building anything. These sources become the user's reading list.
- **No web access available**: build from your own knowledge and say plainly in `sources.md` and in the report that there is no external ground truth.

Write `sources.md`: each source with its link or path and what it covers, numbered so the tree and the report can point to "S2 §3".

### Step 2: Build the frozen rubric (the knowledge tree)

This is the ruler. Every later session is graded against it, so build it carefully once. Read [references/rubric-and-questions.md](references/rubric-and-questions.md) before writing it; the rules that matter most:

- **4-8 nodes in total** (core, weight 2; supporting, weight 1). More than 8 cannot be measured in 20 questions: propose splitting the topic into sub-topics, each tested in its own session, and let the user pick one.
- **Each level of a node is one checkable capability of the kind the scale names**: L2 what it is, L3 why it is designed that way, L4 what happens in a new scenario or where it stops working, L5 how it trades off against an alternative. A rarer fact is not a higher level. One question must be able to settle a level, so a level never bundles several independent facts.
- **A node has a ceiling** when the sources contain nothing of a higher kind (a list of shortcuts has no L5). Record `ceiling: 3`. The node's target is `min(target, ceiling)`.
- For each node also record the **common misconceptions** (they become distractors and diagnosis categories) and source pointers (`S1 §2`).

Save as `tree.md`. Do not show the level descriptors or misconceptions to the user; that would leak the answers.

Done when: every node has one capability per level up to its ceiling, every L4 is a scenario or a boundary, every L5 is a trade-off, and every false belief a reader could plausibly hold is recorded as a misconception under each node it damages.

### Step 3: Confirm the setup (one message)

Show: the node names only (so the user can check the scope), the question count (default 20, about 30 minutes; the user may ask for more), and the target level (default 4; suggest 3 for "just want to follow conversations about it", 5 for "need to make design decisions or survive a deep interview"). Tell them each answer gets immediate feedback and the final report pulls the patterns together. Remind them that "I don't know" is welcome and that they can say "pause" at any time. Start when they agree.

### Step 4: Run the quiz

**Question formats** (design rules and examples are in the rubric reference):

- **Opener (places a node at 0-3 in one question): an open "explain it" question.** "In a sentence or two: how does X work, and why is it built that way? Say whatever you know, or 'don't know'." No options, and the stem names the concept without describing it, so nothing leaks. Grade it against the node's L1-L3 descriptors: nothing -> 0; knows roughly what it is for -> 1; describes how it works -> 2; also gives the reason -> 3.
- **Levels 4-5 and misconception probes: "choose and say why"** — a scenario multiple-choice question that ends with "Pick one and give the reason in one sentence". The user answers once ("B, because ..."). This counts as one question.
- If the user gives only a letter, reply with the verdict alone ("Correct. Before I explain: why that one?") and wait. That follow-up does not count toward the budget.
- If an opener answer is too thin to grade (the user clearly knows more than they said), ask once "Go on: what does it do, step by step?" before grading. That does not count either.

**Order for a baseline (default 20).** Levels are cumulative: a clean pass at level L certifies every level below it.

1. **Breadth scan**: one opener on every node, core nodes first. Every node is now placed at 0-3, and no node is `untested`.
2. **Climb**: each node placed at 3 gets one question at its target level (L4 by default). If the node has a recorded misconception at that level, the question is the scenario where that false belief picks a specific wrong option. Pass with a correct reason: the node is at target and **pinned**. Fail: pinned at 3.
3. **Misconception probes**: nodes placed at 0-2 are pinned for scoring, but a low level does not tell you *what the user believes instead*. With the remaining budget, ask one scenario question for each recorded misconception that has not been tested yet, shared misconceptions (those listed under several nodes) and core nodes first. Each probe is a concrete situation where the false belief predicts one specific distractor.
   - Confident wrong pick or wrong reason: evidence of that wrong model, for the diagnosis.
   - "Don't know": a gap, not a wrong model.
   - Correct with a correct reason on a node placed below 3: don't raise the level on this alone (the opener said otherwise). Note it as `can reason it out`; the retest will settle it.
4. **Leftover budget**: probe target+1 on pinned core nodes that reached the target.

Stop when the budget is used up. Stop earlier only when every node is pinned **and** every recorded misconception of a core node has been probed; say in the report that the quiz ended early and why.

A pass that only repeats what a feedback revealed does not count (hard rule 4). Because feedback after an opener explains that node's "what" and "why", never ask another L1-L3 question on that node in the same session.

**Socratic probes** for levels 3-5: counterexample ("What if the network splits right after..."), boundary ("When does this stop working?"), alternative ("Why not just use X?"), removal ("What breaks if you drop this step?"), prediction ("Given this setup, what happens next?").

**Immediate feedback** (top of the next message, before the next question):

- **Verdict**: correct / partly correct / wrong / "don't know".
- **The right answer** and the reason in 1-3 sentences. After an opener, give what the user was missing among "what" and "why" and nothing about boundaries or trade-offs: those are still to be tested.
- **If wrong or partial: what the answer reveals.** Name the misconception the chosen option or the wording points to ("Picking C means you think detaching *pauses* the agents"). This is the sharp part. Don't soften it.
- **Source pointer** (`S1 §5`) on every feedback, correct answers included, so the user knows where this lives.
- Keep it under about 6 lines, and explain only the question just asked. Feedback that wanders into neighbouring points gives away later questions.

**After each answer, append to the session log** (format in the storage reference): the question, the targeted node and level, the user's verbatim answer, the verdict, the misconception it reveals if any, a `Revealed:` line listing the facts your feedback just told the user, and the node's current level with its pinned state.

**The user pushes back on feedback or a grade:** re-check against the source and the node's descriptors right away. If they're right, say so plainly, fix the verdict and the level, recompute, and log the correction. If not, show exactly where the source says otherwise, in one or two sentences. A dispute doesn't count as a question.

**User asks for a hint:** decline in one line and remind them that "I don't know" is fine. **User says "pause":** save state, tell them how to resume, stop.

### Step 5: Score and diagnose

**Node levels** follow from the log by the grading rules in the rubric reference (the ladder above plus the partial-credit and conflict rules). Apply the rules; do not adjust a level by impression. A node that somehow got no question is reported as `untested` and counts as level 0 in the score; say so in the report.

**Mastery score** = sum(weight x min(level, node target)) / sum(weight x node target) x 100, where node target = min(target, ceiling). 100% means every node is at its target. The score tracks the trend; the per-node levels and the diagnosis are what matter.

**The diagnosis is the main deliverable.** Find the **1-3 root problems** behind the wrong answers, ranked by impact. One wrong mental model usually explains several wrong answers across nodes; name that model instead of listing low-scoring nodes.

- A **wrong mental model** is something the user believes that is false. It shows as confident wrong answers: a chosen distractor, a wrong reason, a wrong prediction.
- A **gap** is something the user doesn't know. It shows as "don't know". Report a pattern of gaps as a gap ("you know what each mechanism does but not why") and never dress it up as a false belief the user did not express.
- Every root problem must rest on at least two answers. A false belief seen in only one answer goes into the report as "suspected, to be checked in the retest", not as a root problem.
- **Group wrong answers by the premise that predicts them.** For each confident wrong answer, write the belief that would make it look right. Answers whose beliefs are the same premise form one root problem, even across nodes ("you treat an expired lease as harmless: you think it isn't counted and doesn't block anything"). Do this grouping before setting any single-answer belief aside as "suspected": two single answers on different nodes often share a premise.
- **Keep different premises apart.** Put a wrong answer under a root problem only if that root's premise, taken literally, predicts the option the user chose. Don't fold a second false belief into the biggest root because it is nearby; it becomes its own root problem or a suspected one.

For each root problem, give:

- **Verdict**: one blunt sentence that names the wrong mental model or the gap, e.g. "You treat Raft as 'elect a boss, then obey the boss'. You haven't grasped that its real invariant is 'a committed entry is never lost', and every log-related question went wrong because of it."
- **Evidence**: which questions, what the user said, and why that answer exposes the problem.
- **Consequence**: the concrete wrong decision this would cause in real work.
- **Gap type** and the matching remedy (see the table in the rubric reference).
- **Fix**: what to read (`S2 §3`) and the question to hold in mind while reading it.

Be specific and direct. No hedging, no praise sandwich. Strengths get one line.

Then write and show the report using [references/report-formats.md](references/report-formats.md), save it, add the row to `history.md`, and set the session `status: complete`. Revealing the answers is safe because a retest never reuses questions. Offer to explain any point live, but don't lecture unprompted.

Done when: the report is shown and saved, `history.md` has the new row, and every level in the report equals the level in the session log.

### Step 6: Retest

- Load `tree.md`, the previous reports, and every earlier session log. **Do not edit the rubric.** A tree written by an earlier version of this skill (no ceilings, several facts in one level) is used as it is; for a level with several facts, test the one a logged misconception contradicts. The only exception is fixing a factual error; log it in the tree's changelog and note in the report that the node's comparison isn't like-for-like.
- **Budget**: 2 questions for each node below its target, plus 1 spot-check for each node at its target, plus 1 for each previous root problem. Use the configured default if that is larger; never exceed 1.5x the default. Tell the user the number before starting, and that it ends early if everything is settled sooner. A retest must be able to bring every node to its target in one session.
- **Previous root problems and misconceptions come first.** For every node that a previous root problem or a logged misconception touched, the target-level question is a fresh scenario where that false belief picks a specific wrong option. A root problem that touched two nodes is checked on both, and counts as resolved only if both come out right.
- **Below-target nodes**: the user has studied, so open each one **at its target level** with a "choose and say why" scenario. Pass with a correct reason: the node is at target, pinned, one question spent. Fail: ask one open "why is it built that way?" question (L3). Pass: pinned at 3. Fail: the level stays where the previous session left it, unless the answers show it is lower.
- **Spot-checks**: one question at the target level on each node that was already at target, to catch earlier lucky guesses and forgetting. A fail here drops the node to 3 and gets the same L3 follow-up.
- **All questions are new, and new means a different situation.** The baseline's feedback already walked through its scenarios, so the same setup with other numbers measures memory of that feedback. For each retest question, pick a situation no earlier log used (another actor, another failure, another business case), and prefer an angle from the node's `Also:` points when the main one has been asked. Check every question against the earlier session logs before asking it.
- The hard rules, feedback, and logging stay the same.
- The report adds a **before -> after table** (up / same / down per node) and revisits each previous root problem explicitly: resolved / partly resolved / persists, with the question that shows it. Judge each one by its own premise as the previous report stated it: a different false belief that is still there is a separate, persisting problem, not a reason to call this one "partly resolved". A drop gets a flag: an earlier lucky guess, or forgetting?
- **Mastered:** when every core node is at or above its target, open the report with a plain "Mastered." and offer a stretch target (target+1) or a spaced check-up in a few weeks. Otherwise give the next reading plan and suggest a retest after it.
