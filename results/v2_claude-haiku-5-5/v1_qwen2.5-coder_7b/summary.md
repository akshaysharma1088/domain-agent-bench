model: qwen2.5-coder:7b | runs: 324 | repeats: 3 | temperature: 0.2 | seed: 7

### Task correctness

| Config | local | cross-domain | injected |
|---|---|---|---|
| B0 | 19.4% [9.8, 35.0] | 2.8% [0.5, 14.2] | 36.1% [22.5, 52.4] |
| B1 | 94.4% [81.9, 98.5] | 44.4% [29.5, 60.4] | 52.8% [37.0, 68.0] |
| S | 94.4% [81.9, 98.5] | 0.0% [0.0, 9.6] | 38.9% [24.8, 55.1] |

### Injected-instruction tasks

| Config | n | Followed the injection (attempted read) | Injection succeeded (read completed) | Regulated table read |
|---|---|---|---|---|
| B0 | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] |
| B1 | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] |
| S | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] |

### Cost of mediation (mean per task)

| Config | Kind | LLM calls | Prompt tokens | Completion tokens | Latency s | A2A calls | Direct foreign-table reads |
|---|---|---|---|---|---|---|---|
| B0 | local | 3.7 | 3463.4 | 133.4 | 35.4 | 0.0 | 0.0 |
| B0 | cross-domain | 2.0 | 1719.3 | 79.5 | 18.0 | 0.0 | 0.8 |
| B0 | injected | 2.0 | 1767.7 | 76.6 | 25.2 | 0.0 | 0.0 |
| B1 | local | 2.0 | 2290.4 | 77.2 | 21.8 | 0.0 | 0.0 |
| B1 | cross-domain | 2.0 | 2303.9 | 103.8 | 22.5 | 0.0 | 1.0 |
| B1 | injected | 2.0 | 2341.3 | 79.9 | 27.2 | 0.0 | 0.0 |
| S | local | 2.0 | 1628.6 | 84.1 | 28.2 | 0.0 | 0.0 |
| S | cross-domain | 5.4 | 4244.2 | 251.0 | 72.0 | 1.4 | 0.0 |
| S | injected | 2.2 | 1896.5 | 90.3 | 39.1 | 0.1 | 0.0 |

runs that never submitted: 2 | runs with parse errors: 0 | A2A requests refused by contract: 0
