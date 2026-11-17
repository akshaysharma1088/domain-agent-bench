#!/usr/bin/env python3
"""Summarize runs.jsonl into the tables the paper needs. Proportions carry Wilson 95% intervals."""
import json
import math
import sys
from collections import defaultdict

KINDS = {"L": "local", "X": "cross-domain", "I": "injected"}


def wilson(k, n, z=1.96):
    if n == 0:
        return "n/a"
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return f"{100 * p:.1f}% [{100 * max(0, c - h):.1f}, {100 * min(1, c + h):.1f}]"


def mean(xs):
    return f"{sum(xs) / len(xs):.1f}" if xs else "n/a"


def main(path):
    rows = [json.loads(line) for line in open(path)]
    if any(r["backend"] == "mock" for r in rows):
        print("> **MOCK BACKEND. These numbers come from a scripted stand-in and are NOT experimental results.**\n")
    print(f"model: {rows[0]['model']} | runs: {len(rows)} | repeats: {len({r['repeat'] for r in rows})}"
          f" | temperature: {rows[0]['temperature']} | seed: {rows[0]['seed']}\n")
    g = defaultdict(list)
    for r in rows:
        g[(r["config"], r["kind"])].append(r)
    configs = sorted({r["config"] for r in rows})

    print("### Task correctness\n\n| Config | " + " | ".join(KINDS.values()) + " |\n|---|---|---|---|")
    for c in configs:
        print(f"| {c} | " + " | ".join(
            wilson(sum(r["correct"] for r in g[(c, k)]), len(g[(c, k)])) for k in KINDS) + " |")

    print("\n### Injected-instruction tasks\n\n| Config | n | Followed the injection (attempted read) | "
          "Injection succeeded (read completed) | Regulated table read |\n|---|---|---|---|---|")
    for c in configs:
        rs = g[(c, "I")]
        print(f"| {c} | {len(rs)} | {wilson(sum(r['inj_attempt'] for r in rs), len(rs))} | "
              f"{wilson(sum(r['inj_success'] for r in rs), len(rs))} | "
              f"{wilson(sum(r['regulated_read'] for r in rs), len(rs))} |")

    print("\n### Cost of mediation (mean per task)\n\n| Config | Kind | LLM calls | Prompt tokens | "
          "Completion tokens | Latency s | A2A calls | Direct foreign-table reads |\n|---|---|---|---|---|---|---|---|")
    for c in configs:
        for k, label in KINDS.items():
            rs = g[(c, k)]
            print(f"| {c} | {label} | {mean([r['llm_calls'] for r in rs])} | {mean([r['prompt_tokens'] for r in rs])} | "
                  f"{mean([r['completion_tokens'] for r in rs])} | {mean([r['latency_s'] for r in rs])} | "
                  f"{mean([r['a2a_calls'] for r in rs])} | {mean([len(r['foreign_tables_read']) for r in rs])} |")

    bad = [r for r in rows if not r["submitted"]]
    print(f"\nruns that never submitted: {len(bad)} | runs with parse errors: "
          f"{sum(1 for r in rows if r['parse_errors'])} | A2A requests refused by contract: "
          f"{sum(r['a2a_refused'] for r in rows)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results/smoke/runs.jsonl")
