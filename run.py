#!/usr/bin/env python3
"""Run the benchmark. Results append to <out>/runs.jsonl and the run can be resumed.

  python run.py --backend mock                       # harness smoke test, NOT results
  python run.py --backend openai --model qwen2.5-coder:14b --repeats 3
"""
import argparse
import json
import os

from meshbench import data
from meshbench.agent import CONFIGS, run_task
from meshbench.llm import Mock, OpenAICompat
from meshbench.tasks import all_tasks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=["mock", "openai"], required=True)
    ap.add_argument("--model", default="mock-scripted")
    ap.add_argument("--base-url", default=None)
    ap.add_argument("--configs", default=",".join(CONFIGS))
    ap.add_argument("--repeats", type=int, default=1)
    ap.add_argument("--repeat-id", type=int, default=None, help="run only this repeat index (for parallel jobs)")
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--tasks", default="", help="comma-separated task ids or template codes, e.g. X1,I2-auto")
    ap.add_argument("--out", default=None)
    ap.add_argument("--traces", action="store_true", help="also write one trace file per run")
    args = ap.parse_args()

    llm = Mock() if args.backend == "mock" else OpenAICompat(args.model, args.base_url)
    out = args.out or os.path.join("results", "smoke" if args.backend == "mock" else llm.model.replace("/", "_").replace(":", "_"))
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "runs.jsonl")
    done = set()
    if os.path.exists(path):
        with open(path) as f:
            done = {(r["task"], r["config"], r["repeat"]) for r in map(json.loads, f)}

    tasks = all_tasks()
    if args.tasks:
        want = set(args.tasks.split(","))
        tasks = [t for t in tasks if t["id"] in want or t["t"] in want]
    base = data.build(seed=args.seed)
    configs = args.configs.split(",")
    reps = [args.repeat_id] if args.repeat_id is not None else list(range(args.repeats))
    total = len(tasks) * len(configs) * len(reps)
    i = 0
    with open(path, "a") as f:
        for rep in reps:
            for task in tasks:
                for cfg in configs:
                    i += 1
                    if (task["id"], cfg, rep) in done:
                        continue
                    r = run_task(task, cfg, llm, lambda: data.clone(base), args.temperature)
                    r.update(repeat=rep, seed=args.seed, temperature=args.temperature)
                    trace = r.pop("trace")
                    if args.traces:
                        os.makedirs(os.path.join(out, "traces"), exist_ok=True)
                        with open(os.path.join(out, "traces", f"{task['id']}_{cfg}_{rep}.json"), "w") as tf:
                            json.dump(trace, tf, indent=1, default=str)
                    f.write(json.dumps(r, default=str) + "\n")
                    f.flush()
                    print(f"[{i}/{total}] {task['id']:14s} {cfg:2s} correct={r['correct']} "
                          f"calls={r['llm_calls']} denied={r['denied_tables']}")
    print(f"\nwrote {path}\nnext: python summarize.py {path}")


if __name__ == "__main__":
    main()
