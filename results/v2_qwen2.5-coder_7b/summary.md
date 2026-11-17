model: qwen2.5-coder:7b | runs: 324 | repeats: 3 | temperature: 0.2 | seed: 7

### Task correctness

| Config | local | cross-domain | injected |
|---|---|---|---|
| B0 | 22.2% [11.7, 38.1] | 2.8% [0.5, 14.2] | 36.1% [22.5, 52.4] |
| B1 | 94.4% [81.9, 98.5] | 50.0% [34.5, 65.5] | 50.0% [34.5, 65.5] |
| S | 97.2% [85.8, 99.5] | 2.8% [0.5, 14.2] | 30.6% [18.0, 46.9] |

### Injected-instruction tasks

| Config | n | Followed the injection (attempted read) | Injection succeeded (read completed) | Regulated table read |
|---|---|---|---|---|
| B0 | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] |
| B1 | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] |
| S | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] |

### Cost of mediation (mean per task)

| Config | Kind | LLM calls | Prompt tokens | Completion tokens | Latency s | A2A calls | Direct foreign-table reads |
|---|---|---|---|---|---|---|---|
| B0 | local | 3.4 | 3145.0 | 122.6 | 28.3 | 0.0 | 0.0 |
| B0 | cross-domain | 2.0 | 1718.7 | 78.0 | 16.0 | 0.0 | 0.8 |
| B0 | injected | 2.0 | 1768.4 | 77.9 | 20.9 | 0.0 | 0.0 |
| B1 | local | 2.0 | 2291.0 | 78.1 | 21.4 | 0.0 | 0.0 |
| B1 | cross-domain | 2.0 | 2305.9 | 108.1 | 22.0 | 0.0 | 1.0 |
| B1 | injected | 2.0 | 2341.3 | 79.9 | 26.8 | 0.0 | 0.0 |
| S | local | 2.0 | 1673.6 | 85.0 | 26.4 | 0.0 | 0.0 |
| S | cross-domain | 6.9 | 5664.8 | 331.4 | 91.2 | 1.9 | 0.0 |
| S | injected | 2.0 | 1693.8 | 77.0 | 31.6 | 0.0 | 0.0 |

runs that never submitted: 0 | runs with parse errors: 0 | A2A requests refused by contract: 0
