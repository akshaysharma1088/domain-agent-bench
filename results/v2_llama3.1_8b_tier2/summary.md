model: llama3.1:8b | runs: 108 | repeats: 3 | temperature: 0.2 | seed: 7

### Task correctness

| Config | local | cross-domain | injected |
|---|---|---|---|
| B0 | n/a | n/a | 83.3% [68.1, 92.1] |
| B1 | n/a | n/a | 91.7% [78.2, 97.1] |
| S | n/a | n/a | 69.4% [53.1, 82.0] |

### Injected-instruction tasks, tier 2

| Config | n | Followed the injection (attempted read) | Injection succeeded (read completed) | Regulated table read | Task still correct |
|---|---|---|---|---|---|
| B0 | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 83.3% [68.1, 92.1] |
| B1 | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 91.7% [78.2, 97.1] |
| S | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 69.4% [53.1, 82.0] |

### Cost of mediation (mean per task)

| Config | Kind | LLM calls | Prompt tokens | Completion tokens | Latency s | A2A calls | Direct foreign-table reads |
|---|---|---|---|---|---|---|---|
| B0 | local | n/a | n/a | n/a | n/a | n/a | n/a |
| B0 | cross-domain | n/a | n/a | n/a | n/a | n/a | n/a |
| B0 | injected | 2.7 | 2165.8 | 126.2 | 36.3 | 0.0 | 0.1 |
| B1 | local | n/a | n/a | n/a | n/a | n/a | n/a |
| B1 | cross-domain | n/a | n/a | n/a | n/a | n/a | n/a |
| B1 | injected | 2.4 | 2635.1 | 116.2 | 41.2 | 0.0 | 0.1 |
| S | local | n/a | n/a | n/a | n/a | n/a | n/a |
| S | cross-domain | n/a | n/a | n/a | n/a | n/a | n/a |
| S | injected | 5.4 | 4192.3 | 205.6 | 71.2 | 1.3 | 0.0 |

runs that never submitted: 1 | runs with parse errors: 5 | A2A requests refused by contract: 8
