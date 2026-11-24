# Large codebases: build the rubric from an Understand Anything graph

Use this only when the material is a **large codebase**: a repository or directory the user is reading or about to work in, too big to read the relevant code in full before the quiz. Rule of thumb: more than about 50 source files or 10k lines (`git ls-files | wc -l`, or a `wc -l` over the source files). Everything else keeps the normal Step 1:

- a single file, a snippet, or a small repo you can read in full: read it directly;
- books, papers, docs, notes, a topic name: the normal path, even if they are long. Understand Anything is not used for them.

[Understand Anything](https://github.com/Egonex-AI/Understand-Anything) is a Claude Code plugin that turns a codebase into a knowledge graph (files, functions, classes, their edges, architectural layers, a guided tour). For a big codebase it answers the question this skill cannot answer cheaply on its own: *which 4-8 concepts are worth testing, and where do they live in the code.* The graph is a map; **the code stays the answer key.**

## A. Find or build the graph

1. **Scope.** If the user named a part of the codebase ("the payment flow", "`src/scheduler`"), the topic is that part. For a monorepo, scope the graph to the subdirectory that contains it.
2. **Existing graph.** Look for `.ua/knowledge-graph.json`, or the legacy `.understand-anything/knowledge-graph.json`, at the repository root (for a git worktree, the main checkout's root). Also note `domain-graph.json` in the same directory if it exists.
   - Compare the graph's `project.gitCommitHash` with `git rev-parse HEAD`. Same: use it. Different: tell the user in one line and offer an incremental refresh (`/understand`, which only re-analyzes changed files). If they decline, use the stale graph and verify against current code as usual (section B).
3. **No graph, plugin available** (an `understand` or `understand-anything:understand` skill is listed): tell the user in one message that you will first build a map of the codebase with Understand Anything, that the first run on a large project uses a lot of tokens (later runs are incremental), and what scope you will pass. Run it when they agree, by invoking that skill with the scope path and `--language <code>` matching the user's language. Do not pass `--auto-update`; that installs a commit hook, which is the user's call.
4. **No graph, plugin missing:** say so in one message, give the install commands, and offer to continue without the graph:

   ```
   /plugin marketplace add Egonex-AI/Understand-Anything
   /plugin install understand-anything
   ```

   Without the graph, fall back to the normal Step 1 on a narrowed scope: read the README, the architecture docs, and the entry points and core modules of the part the user cares about. Say in `sources.md` and the report that the rubric was built without a codebase map.

## B. Read the graph, verify in code

Read the graph's `project`, `layers`, `tour`, and the nodes and edges inside the scope. If `domain-graph.json` exists, read its domains and flows too: business flows often make better nodes than modules.

The node `summary` fields and the tour text were written by a model and can be wrong. Before any fact goes into a level descriptor, a misconception, or a feedback, **open the code at the node's `filePath` and `lineRange` and confirm it.** If the code disagrees with the graph, the code wins; note the mismatch in `sources.md`.

`sources.md` for a codebase:

- **S1**: the graph, with its path, `project.gitCommitHash`, and the scope it covers.
- **S2...**: the repository's own docs (README, ARCHITECTURE, ADRs, design docs) that the rubric relies on.
- Code pointers are `path:line` (or `path:start-end`), cited as `S1 path:line` in the tree and the report.
- Record the commit the rubric was built at. A retest uses the same frozen tree; if the code has changed in a way that makes a descriptor false, that is the "factual error" exception in Step 6.

## C. Turn the graph into a rubric

The tree rules in [rubric-and-questions.md](rubric-and-questions.md) still apply (4-8 nodes, one capability per level, ceilings, misconceptions). What changes is where nodes and questions come from.

**Nodes are concepts someone working in this code must hold, not files.** Good candidates:

| Graph signal | Node it suggests |
|---|---|
| A `tour` step, or a domain `flow` | An end-to-end flow ("how a request becomes a charge") |
| A `layer` and the edges that cross it | A boundary and its contract ("what the API layer may and may not do") |
| A node with many incoming `calls` / `depends_on` edges | A core abstraction everything leans on |
| `reads_from` / `writes_to` / `defines_schema` edges | The data model and who owns which data |
| `publishes` / `subscribes` / `triggers` edges | Async behavior, ordering, retries |
| `configures` / `deploys` edges | How behavior changes per environment |

Core nodes are the ones on the main flow of the scope (the tour order is a good guide). Supporting nodes are the ones a newcomer would trip over.

**Levels in code terms:**

- **L2**: what the component or flow does and roughly where it lives.
- **L3**: why it is built that way: the constraint or the failure it prevents (verify in code, comments, docs, or commit messages; do not invent a rationale).
- **L4**: a change or failure scenario answered from the graph's edges and confirmed in code: "If X starts returning null / is called twice / runs before Y, what breaks and where?", "You need to add Z: which layer does it go in, and what else must change?"
- **L5**: a trade-off against an alternative design. Code rarely states one. Give the node `ceiling: 4` unless a design doc, ADR, comment, or commit message records an alternative that was considered.

**Misconceptions in code** usually come from surface reading. Look for places where it misleads, and confirm each one in code:

- a name that suggests a different behavior than the code has;
- a call that looks synchronous but is queued, retried, or fire-and-forget;
- a module that looks like it owns data it only reads, or a cache that looks like the source of truth;
- an edge the graph shows that a reader would not expect (a hidden dependency across layers), or one a reader would expect that does not exist;
- error paths: what actually happens on failure versus what the happy path suggests.

## D. During the quiz and in the report

- Questions describe situations in the code's own terms (real module and function names are fine; they are not answers). Never paste the graph's summary of the node being asked about.
- Feedback pointers are `S1 path:line`, so the user can jump to the code.
- In the report's **Fix** lines, besides the code to read, you may point to the plugin's study aids when installed: `/understand-explain <path>` for a deep dive on one file or function, `/understand-dashboard` to explore the map, `/understand-chat <question>` to ask about the codebase. These are for studying between sessions, not during the quiz.
