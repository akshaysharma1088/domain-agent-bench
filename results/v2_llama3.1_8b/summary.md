model: llama3.1:8b | runs: 324 | repeats: 3 | temperature: 0.2 | seed: 7

### Task correctness

| Config | local | cross-domain | injected |
|---|---|---|---|
| B0 | 2.8% [0.5, 14.2] | 5.6% [1.5, 18.1] | 83.3% [68.1, 92.1] |
| B1 | 88.9% [74.7, 95.6] | 63.9% [47.6, 77.5] | 83.3% [68.1, 92.1] |
| S | 83.3% [68.1, 92.1] | 27.8% [15.8, 44.0] | 75.0% [58.9, 86.2] |

### Injected-instruction tasks

| Config | n | Followed the injection (attempted read) | Injection succeeded (read completed) | Regulated table read |
|---|---|---|---|---|
| B0 | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] |
| B1 | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] |
| S | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] |

### Cost of mediation (mean per task)

| Config | Kind | LLM calls | Prompt tokens | Completion tokens | Latency s | A2A calls | Direct foreign-table reads |
|---|---|---|---|---|---|---|---|
| B0 | local | 3.3 | 2572.5 | 106.8 | 34.9 | 0.0 | 0.0 |
| B0 | cross-domain | 3.0 | 2452.5 | 150.2 | 41.1 | 0.0 | 1.0 |
| B0 | injected | 2.7 | 2123.6 | 131.7 | 43.3 | 0.0 | 0.2 |
| B1 | local | 2.5 | 2544.2 | 87.6 | 27.6 | 0.0 | 0.0 |
| B1 | cross-domain | 2.4 | 2454.8 | 127.4 | 31.2 | 0.0 | 1.0 |
| B1 | injected | 2.5 | 2671.6 | 132.2 | 44.8 | 0.0 | 0.1 |
| S | local | 2.4 | 1793.7 | 96.2 | 27.2 | 0.2 | 0.0 |
| S | cross-domain | 8.5 | 5972.4 | 351.0 | 92.6 | 2.8 | 0.0 |
| S | injected | 2.1 | 1594.7 | 105.7 | 32.5 | 0.0 | 0.0 |

runs that never submitted: 4 | runs with parse errors: 18 | A2A requests refused by contract: 0
