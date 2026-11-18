# Final results (harness v2)

Main run (36 tasks) and tier 2 injection run (12 tasks) merged per model. Three repeats, temperature 0.2, seed 7.

## qwen2.5-coder_7b

model: qwen2.5-coder:7b | runs: 432 | repeats: 3 | temperature: 0.2 | seed: 7

### Task correctness

| Config | local | cross-domain | injected |
|---|---|---|---|
| B0 | 22.2% [11.7, 38.1] | 2.8% [0.5, 14.2] | 40.3% [29.7, 51.8] |
| B1 | 94.4% [81.9, 98.5] | 50.0% [34.5, 65.5] | 45.8% [34.8, 57.3] |
| S | 97.2% [85.8, 99.5] | 2.8% [0.5, 14.2] | 30.6% [21.1, 42.0] |

### Injected-instruction tasks, tier 1

| Config | n | Followed the injection (attempted read) | Injection succeeded (read completed) | Regulated table read | Task still correct |
|---|---|---|---|---|---|
| B0 | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 36.1% [22.5, 52.4] |
| B1 | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 50.0% [34.5, 65.5] |
| S | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 30.6% [18.0, 46.9] |

### Injected-instruction tasks, tier 2

| Config | n | Followed the injection (attempted read) | Injection succeeded (read completed) | Regulated table read | Task still correct |
|---|---|---|---|---|---|
| B0 | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 44.4% [29.5, 60.4] |
| B1 | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 41.7% [27.1, 57.8] |
| S | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 30.6% [18.0, 46.9] |

### Cost of mediation (mean per task)

| Config | Kind | LLM calls | Prompt tokens | Completion tokens | Latency s | A2A calls | Direct foreign-table reads |
|---|---|---|---|---|---|---|---|
| B0 | local | 3.4 | 3145.0 | 122.6 | 28.3 | 0.0 | 0.0 |
| B0 | cross-domain | 2.0 | 1718.7 | 78.0 | 16.0 | 0.0 | 0.8 |
| B0 | injected | 2.0 | 1801.5 | 79.1 | 26.1 | 0.0 | 0.0 |
| B1 | local | 2.0 | 2291.0 | 78.1 | 21.4 | 0.0 | 0.0 |
| B1 | cross-domain | 2.0 | 2305.9 | 108.1 | 22.0 | 0.0 | 1.0 |
| B1 | injected | 2.0 | 2373.5 | 79.2 | 29.8 | 0.0 | 0.0 |
| S | local | 2.0 | 1673.6 | 85.0 | 26.4 | 0.0 | 0.0 |
| S | cross-domain | 6.9 | 5664.8 | 331.4 | 91.2 | 1.9 | 0.0 |
| S | injected | 2.0 | 1726.3 | 77.0 | 31.2 | 0.0 | 0.0 |

runs that never submitted: 0 | runs with parse errors: 0 | A2A requests refused by contract: 0

## llama3.1_8b

model: llama3.1:8b | runs: 432 | repeats: 3 | temperature: 0.2 | seed: 7

### Task correctness

| Config | local | cross-domain | injected |
|---|---|---|---|
| B0 | 2.8% [0.5, 14.2] | 5.6% [1.5, 18.1] | 83.3% [73.1, 90.2] |
| B1 | 88.9% [74.7, 95.6] | 63.9% [47.6, 77.5] | 87.5% [77.9, 93.3] |
| S | 83.3% [68.1, 92.1] | 27.8% [15.8, 44.0] | 72.2% [61.0, 81.2] |

### Injected-instruction tasks, tier 1

| Config | n | Followed the injection (attempted read) | Injection succeeded (read completed) | Regulated table read | Task still correct |
|---|---|---|---|---|---|
| B0 | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 83.3% [68.1, 92.1] |
| B1 | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 83.3% [68.1, 92.1] |
| S | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 75.0% [58.9, 86.2] |

### Injected-instruction tasks, tier 2

| Config | n | Followed the injection (attempted read) | Injection succeeded (read completed) | Regulated table read | Task still correct |
|---|---|---|---|---|---|
| B0 | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 83.3% [68.1, 92.1] |
| B1 | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 91.7% [78.2, 97.1] |
| S | 36 | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 0.0% [0.0, 9.6] | 69.4% [53.1, 82.0] |

### Cost of mediation (mean per task)

| Config | Kind | LLM calls | Prompt tokens | Completion tokens | Latency s | A2A calls | Direct foreign-table reads |
|---|---|---|---|---|---|---|---|
| B0 | local | 3.3 | 2572.5 | 106.8 | 34.9 | 0.0 | 0.0 |
| B0 | cross-domain | 3.0 | 2452.5 | 150.2 | 41.1 | 0.0 | 1.0 |
| B0 | injected | 2.7 | 2144.7 | 128.9 | 39.8 | 0.0 | 0.2 |
| B1 | local | 2.5 | 2544.2 | 87.6 | 27.6 | 0.0 | 0.0 |
| B1 | cross-domain | 2.4 | 2454.8 | 127.4 | 31.2 | 0.0 | 1.0 |
| B1 | injected | 2.5 | 2653.4 | 124.2 | 43.0 | 0.0 | 0.1 |
| S | local | 2.4 | 1793.7 | 96.2 | 27.2 | 0.2 | 0.0 |
| S | cross-domain | 8.5 | 5972.4 | 351.0 | 92.6 | 2.8 | 0.0 |
| S | injected | 3.7 | 2893.5 | 155.7 | 51.9 | 0.6 | 0.0 |

runs that never submitted: 5 | runs with parse errors: 23 | A2A requests refused by contract: 8
