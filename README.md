# domain-agent-bench

A small, reproducible benchmark that compares three ways of placing an LLM agent on a
domain-driven data platform. It is the evaluation artifact for the paper
"Agent-Oriented Reference Architecture for Domain-Driven Enterprise Data Platforms".

| Config | Credential | Context | Cross-domain work |
|---|---|---|---|
| B0 | one broad credential over every table | none | direct reads |
| B1 | one broad credential over every table | all domain glossaries in the prompt | direct reads |
| S  | identity derived from the Servicing charter | Servicing context pack only | A2A contracts to Originations and Risk agents |

All three configurations carry the same prompt instruction to treat row contents as data.
Only S enforces the boundary in infrastructure (a database authorizer driven by the charter).

## What it measures

48 tasks for a Servicing agent over a synthetic lender estate (three bounded contexts,
seeded, no real data):

- 12 local tasks, answerable inside Servicing
- 12 cross-domain tasks that depend on another domain's meaning of a term or code
- 24 tasks whose source data carries an injected instruction to read a foreign table, in two tiers
  (18 target a regulated PII table)

Reported per configuration: task correctness, how often the agent followed an injected
instruction, how often that read completed, and the cost of mediation (LLM calls, tokens,
latency, A2A calls). Proportions carry Wilson 95% intervals.

## Run it

Python 3.9+, standard library only.

```bash
# 1. harness smoke test with a scripted stand-in (NOT results)
python run.py --backend mock
python summarize.py results/smoke/runs.jsonl

# 2. real run against any OpenAI-compatible endpoint, e.g. a local Ollama model
ollama pull qwen2.5-coder:14b
python run.py --backend openai --model qwen2.5-coder:14b --repeats 3 --traces
python summarize.py results/qwen2.5-coder_14b/runs.jsonl > results/qwen2.5-coder_14b/summary.md
```

Set `MESHBENCH_BASE_URL` and `MESHBENCH_API_KEY` for a hosted endpoint. Runs append to
`runs.jsonl` and resume where they stopped. `--tasks X1,I2-auto` runs a subset.

For the paper, run at least two models of different strength with `--repeats 3` or more,
and keep `runs.jsonl` and the traces with the artifact.

## Reading the results honestly

- In S an out-of-charter read cannot complete, by construction. The informative numbers are
  therefore how often agents in B0 and B1 follow injections despite the prompt guardrail,
  whether S keeps task correctness on cross-domain work, and what the mediation costs.
- B1 is the strong baseline. If B1 matches S on correctness, the benefit of S is containment
  and ownership, not accuracy, and the paper should say so.
- The mock backend replays a script. Its output must never be reported.

## Limitations

Synthetic data, one home domain, single-value SQL tasks, SQLite as the enforcement
substrate, and provider agents limited to one call. Audit and replay, autonomy tiers and
the model registry are not evaluated here.

## Layout

```
meshbench/data.py      synthetic estate
meshbench/domains.py   charters, context packs, A2A contracts
meshbench/tasks.py     task templates and injections
meshbench/platform.py  scoped identity enforcement, contract checks, trace
meshbench/agent.py     agent loop and the three configurations
meshbench/llm.py       model backends
run.py, summarize.py
```

## Result history

- `results/v1_*` (harness v1, 17 Nov 2026): first full run. Kept for the record and not used
  in the paper. In v1 the table returned by an A2A `select_ids` request had a column named
  `id` and the response did not state the column name. Agents wrote
  `... IN (SELECT loan_id FROM a2a_result_n)`, which SQLite resolves as a correlated reference
  and silently returns every row. That interface defect affected 38 of the 40 scoped
  cross-domain runs that used a returned table, so v1 cross-domain numbers for S are invalid.
- `results/v2_*` (harness v2): the returned column is named after the contract key
  (`app_id` or `loan_id`) and the response states it. Nothing else changed: same tasks, data,
  prompts for B0 and B1, models, temperature and seed.
- Injection tiers: tier 1 (I1 to I4) are plain one-line instructions. They were followed in
  0 of 216 runs in v1. Tier 2 (I5 to I8) was then declared once, using format
  mimicry and task-aligned wording, and is reported next to tier 1. Tier 2 is not tuned
  further whatever it shows.

## Results

See `results/SUMMARY.md`. In short, with qwen2.5-coder:7b and llama3.1:8b: domain context decides
correctness; the scoped agent matches the strong baseline on local tasks with a smaller prompt;
contract-mediated cross-domain work is much less accurate and more expensive than direct access;
and no model followed an injected instruction in either tier.
