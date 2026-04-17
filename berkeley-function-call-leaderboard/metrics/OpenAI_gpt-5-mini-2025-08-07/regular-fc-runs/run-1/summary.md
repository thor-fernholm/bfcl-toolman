# Benchmark Metrics: `regular-fc | OpenAI/gpt-5-mini-2025-08-07`

## 1. Global Totals & Averages
| Metric | Total (Sum) | Average (Mean per test) |
|---|---|---|
| **Tests Run** | 4001 | - |
| **Successes** | 1831 | 45.76% (Success Rate) |
| **Input Tokens** | 82971653 | 20737.7 |
| **Output Tokens** | 531607 | 132.9 |
| **Thinking Tokens** | 3775872 | 943.7 |
| **Turns** | 5397 | 1.3 |
| **Steps** | 14603 | 3.6 |
| **LLM Latency (sec)** | 72787.76s | 18.19s (Total) / 12.59s (Per Turn) / 7.81s (Per Step) |
| **Runtime Errors (Goja)** | 0 | 0.00 |
| **Tool Errors (BFCL)** | 0 | 0.00 |
| **Tool Calls** | 10235 | 2.6 (Total) / 1.7 (Per Turn) |
| **Task Horizon (Length)** | - | 1.35 Turns |
| **Redundant Tool Calls** | 3163 | 0.79 |
| **Self-Correct (Runtime)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Self-Correct (Tool)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Context Growth** | - | 1629 (Total) / 1542 (Turn) / 94 (Step) |

## 2. Averages by Outcome (Success vs. Failure)
| Metric | Successes | Failures |
|---|---|---|
| **Input Tokens (Test/Turn/Step)** | 10526.3 / 3894.9 / 1928.7 | 29353.9 / 14700.9 / 2762.7 |
| **Output Tokens (Test/Turn/Step)** | 76.2 / 51.2 / 44.1 | 180.7 / 120.8 / 66.2 |
| **Thinking Tokens (Test/Turn/Step)** | 468.3  / 319.7 / 274.7 | 1344.9 / 964.2 / 520.2 |
| **Turns** | 1.2 | 1.5 |
| **Steps** | 2.1 | 5.0 |
| **LLM Latency (Total)** | 10.57s | 24.62s |
| **LLM Latency (Per Turn)** | 7.33s | 17.03s |
| **LLM Latency (Per Step)** | 6.04s | 9.31s |
| **Context Growth (Total)** | 1329.6 | 1881.1 |
| **Context Growth (Per Turn)**| 1285.5 | 1758.2 |
| **Context Growth (Per Step)**| 11.4 | 164.1 |

## 3. Breakdown by Category

### Category Totals
| Category | Tests | Successes | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | LLM Latency | Runtime Errors | Tool Errors | Redundant Calls | Self-Corrects (Runtime) | Self-Corrects (Tool) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 240 | 33 | 134297 | 15739 | 195520 | 240 | 245 | 4024.28s | 0 | 0 | 30 | 0 | 0 |
| live_irrelevance | 876 | 73 | 1225834 | 93210 | 743040 | 877 | 879 | 13085.38s | 0 | 0 | 60 | 0 | 0 |
| live_multiple | 1053 | 764 | 2188576 | 49699 | 320960 | 1053 | 1053 | 6743.62s | 0 | 0 | 40 | 0 | 0 |
| live_relevance | 16 | 16 | 26068 | 1485 | 9536 | 16 | 16 | 174.84s | 0 | 0 | 0 | 0 | 0 |
| live_simple | 258 | 182 | 180083 | 12364 | 64512 | 258 | 258 | 1400.47s | 0 | 0 | 16 | 0 | 0 |
| multi_turn_base | 208 | 97 | 21207259 | 73147 | 435776 | 676 | 2862 | 11044.46s | 0 | 0 | 535 | 0 | 0 |
| multi_turn_long_context | 200 | 9 | 18342469 | 68578 | 384384 | 387 | 2402 | 7919.73s | 0 | 0 | 450 | 0 | 0 |
| multi_turn_miss_func | 200 | 7 | 12564316 | 69928 | 651392 | 406 | 2526 | 10274.36s | 0 | 0 | 866 | 0 | 0 |
| multi_turn_miss_param | 200 | 44 | 26567430 | 116923 | 817152 | 734 | 3609 | 14578.80s | 0 | 0 | 1162 | 0 | 0 |
| multiple | 200 | 169 | 204029 | 7779 | 38080 | 200 | 200 | 895.81s | 0 | 0 | 0 | 0 | 0 |
| simple_java | 100 | 60 | 67110 | 4576 | 28800 | 100 | 102 | 598.20s | 0 | 0 | 0 | 0 | 0 |
| simple_javascript | 50 | 27 | 35240 | 2516 | 18240 | 50 | 50 | 347.70s | 0 | 0 | 1 | 0 | 0 |
| simple_python | 400 | 350 | 228942 | 15663 | 68480 | 400 | 401 | 1700.11s | 0 | 0 | 3 | 0 | 0 |

### Category Averages
| Category | Success Rate | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | Latency (Total/Turn/Step) | Context Growth (Total/Turn/Step) | Runtime Errors | Tool Errors | Redundant | Runtime Recovery % | Tool Recovery % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 13.8% | 559.6 | 65.6 | 814.7 | 1.0 | 1.0 | 16.77s / 16.77s / 15.06s | 559.6 / 559.6 / 0.0 | 0.00 | 0.00 | 0.12 | 0.0% | 0.0% |
| live_irrelevance | 8.3% | 1399.4 | 106.4 | 848.2 | 1.0 | 1.0 | 14.94s / 14.94s / 14.75s | 1399.4 / 1399.4 / 0.0 | 0.00 | 0.00 | 0.07 | 0.0% | 0.0% |
| live_multiple | 72.6% | 2078.4 | 47.2 | 304.8 | 1.0 | 1.0 | 6.40s / 6.40s / 6.40s | 2078.4 / 2078.4 / 0.0 | 0.00 | 0.00 | 0.04 | 0.0% | 0.0% |
| live_relevance | 100.0% | 1629.2 | 92.8 | 596.0 | 1.0 | 1.0 | 10.93s / 10.93s / 10.93s | 1629.2 / 1629.2 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| live_simple | 70.5% | 698.0 | 47.9 | 250.0 | 1.0 | 1.0 | 5.43s / 5.43s / 5.43s | 698.0 / 698.0 / 0.0 | 0.00 | 0.00 | 0.06 | 0.0% | 0.0% |
| multi_turn_base | 46.6% | 101958.0 | 351.7 | 2095.1 | 3.2 | 13.8 | 53.10s / 20.77s / 3.89s | 640.2 / 336.7 / 68.3 | 0.00 | 0.00 | 2.57 | 0.0% | 0.0% |
| multi_turn_long_context | 4.5% | 91712.3 | 342.9 | 1921.9 | 1.9 | 12.0 | 39.60s / 24.73s / 3.18s | 8567.7 / 7828.5 / 1656.7 | 0.00 | 0.00 | 2.25 | 0.0% | 0.0% |
| multi_turn_miss_func | 3.5% | 62821.6 | 349.6 | 3257.0 | 2.0 | 12.6 | 51.37s / 31.89s / 3.46s | 825.2 / 665.2 / 84.5 | 0.00 | 0.00 | 4.33 | 0.0% | 0.0% |
| multi_turn_miss_param | 22.0% | 132837.1 | 584.6 | 4085.8 | 3.7 | 18.0 | 72.89s / 28.83s / 3.73s | 1072.9 / 549.7 / 73.2 | 0.00 | 0.00 | 5.81 | 0.0% | 0.0% |
| multiple | 84.5% | 1020.1 | 38.9 | 190.4 | 1.0 | 1.0 | 4.48s / 4.48s / 4.48s | 1020.1 / 1020.1 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| simple_java | 60.0% | 671.1 | 45.8 | 288.0 | 1.0 | 1.0 | 5.98s / 5.98s / 5.77s | 671.1 / 671.1 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| simple_javascript | 54.0% | 704.8 | 50.3 | 364.8 | 1.0 | 1.0 | 6.95s / 6.95s / 6.95s | 704.8 / 704.8 / 0.0 | 0.00 | 0.00 | 0.02 | 0.0% | 0.0% |
| simple_python | 87.5% | 572.4 | 39.2 | 171.2 | 1.0 | 1.0 | 4.25s / 4.25s / 4.25s | 572.4 / 572.4 / 0.0 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |
