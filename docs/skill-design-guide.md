# Skill Design Guide

This is the authoring standard for `SKILL.md` files in this repository
(`samples/discovery`, `samples/enrichment/.../skills/*`, and any new agent
skill added under those trees). It exists so that skills stay easy to audit,
cheap to load, and hard to get wrong as they grow. Every section below ends
with how it applies to the skills that already exist here.

## 1. Trigger

Decide explicitly how a skill activates, and write that decision down instead
of leaving it implicit:

| Mode | Trade-off |
| --- | --- |
| Model-invoked | Convenient, but the `description` field is loaded into context on every turn, and activation is probabilistic. |
| User-invoked | Deterministic and context-cheap, but the operator has to know it exists. |
| Hybrid | Reserve for workflows that genuinely need both entry points. |

Read-only, information-retrieval skills are the safe default for
model-invoked. Anything that writes, publishes, or promotes data should not
activate just because a model judged it relevant.

**Applied here:**

| Skill | Invocation | Why |
| --- | --- | --- |
| `samples/discovery` (Knowledge Catalog search) | Model-invoked | Read-only; answering the user's question is the whole point. |
| `kb-search` (fileskb lookup) | Model-invoked | Read-only lookup against a local knowledge base. |
| Any future "publish enrichment to catalog" or "overwrite entry" skill | User-invoked, with explicit confirmation | Mutating the catalog should never happen because a model merely thought it was relevant. |

## 2. Structure

A skill has exactly two kinds of content:

- **Steps** — the procedure, needed on every invocation. This lives in
  `SKILL.md`.
- **References** — material only needed for a specific branch of the
  procedure (a lookup table, a set of worked examples, a per-source
  cookbook). This lives in a `references/` directory next to `SKILL.md` and
  is pulled in only when that branch is taken.

This is the same split already used for catalog content in this repo —
`okf/bundles/<name>/references/` holds per-entry detail (metrics, joins)
that the top-level catalog docs point to rather than inline. Skills should
follow the identical convention:

```
skill/
├── SKILL.md              # always-loaded procedure
└── references/
    ├── predicate-reference.md   # loaded only when extracting predicates
    └── examples.md              # loaded only when worked examples are needed
```

**Applied here:** `samples/discovery/SKILL.md` is the skill in this repo
most in need of this split — it used to inline the full predicate reference
table and worked examples directly in `SKILL.md`, mixing core procedure with
branch-specific lookup material. See the refactor in this same change: the
procedure stays in `SKILL.md`, the table moves to
`references/predicate-reference.md`, and the examples move to
`references/examples.md`.

This particular agent (`samples/discovery/agent.py`) has no file-reading
tool — it loads its instruction as one string — so the split here is for
maintainability and pruning, not a runtime context saving:
`load_instruction()` concatenates `SKILL.md` with everything under
`references/` before handing it to the model. A skill whose agent *does*
have a file-reading tool, like `kb-search` (via the `fileskb` MCP server's
`list_contents`/`read_file`), can instead keep reference material out of the
loaded instruction entirely and pull it in only when a step needs it — that
is the genuine on-demand version of this same split.

## 3. Steering

A "leading phrase" is a short, repeated form of words that compresses a
behavioral rule the model should keep returning to — not a one-time
instruction. It should show up wherever the behavior matters: the
`description` field, step headings, and any validation/error text — not
just asserted once at the top and then forgotten.

Judge success by the skill's actual output, not by whether the phrase was
echoed back in reasoning.

**Applied here** — the doctrine already implicit in `samples/discovery/SKILL.md`,
made explicit and repeated at the points that matter:

| Leading phrase | Behavior it compresses |
| --- | --- |
| Baseline search always | The literal user query is always one of the parallel searches, never replaced by generated variations. |
| Predicates from the table only | Never invent a predicate that isn't in the Predicate Reference Table. |
| Names, not explanations | Return entry names only; do not justify why an entry was selected. |
| Attempt first, clarify never | Never open with "I cannot answer that" or ask a clarifying question before searching. |

## 4. Phase isolation

For any workflow with sequential, gated stages (for example a pipeline like
propose → review → dedup, as in `ConversationLearner`), don't hand the
executor every stage's instructions up front. Expose only:

- the current stage's goal,
- what evidence it must produce,
- and a pointer to the next stage — without the next stage's content.

Advancing to the next stage happens only after the current stage's output is
accepted (a gate/judge check), not by the executor reading ahead. This
matters because early visibility into a later stage measurably changes
behavior in the current one (rushing discovery because the destination is
already known, designing around unverified state, etc.) — withholding the
future stage's *content*, not just instructing the model not to peek, is
what prevents it.

**Applied here:** none of the current skills in this repo are multi-stage
pipelines with a gating mechanism, so there is nothing to refactor today.
This section is the standard to apply when one is added — e.g. if an
enrichment or promotion skill grows a propose → validate → publish sequence,
each stage should be its own bounded unit rather than one `SKILL.md` that
narrates the whole pipeline.

## 5. Pruning

Every edit to a skill gets a deletion test before it's considered done:

1. Remove the instruction.
2. Re-run the skill against its existing examples/tests.
3. If behavior doesn't materially change, leave it removed.
4. If it only matters for one branch, move it into that branch's
   `references/` file instead of `SKILL.md`.
5. If it's genuinely durable knowledge, it belongs in the shared
   catalog/reference material, not restated inside every skill that needs
   it.
6. If it duplicates something already established elsewhere (platform
   behavior, another skill's instructions), delete it rather than
   re-stating it.

This repo doesn't yet have an automated eval harness for skills, so step 2
today means manually re-running the worked examples in
`references/examples.md` and confirming the extracted predicates and
returned entries are unchanged. If an eval harness is added later, this is
the hook it should run against.
