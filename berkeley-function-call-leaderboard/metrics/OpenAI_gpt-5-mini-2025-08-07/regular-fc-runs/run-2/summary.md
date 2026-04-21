# Benchmark Metrics: `regular-fc | OpenAI/gpt-5-mini-2025-08-07`

## 1. Global Totals & Averages
| Metric | Total (Sum) | Average (Mean per test) |
|---|---|---|
| **Tests Run** | 4001 | - |
| **Successes** | 2066 | 51.64% (Success Rate) |
| **Input Tokens** | 203181140 | 50782.6 |
| **Output Tokens** | 884386 | 221.0 |
| **Thinking Tokens** | 5432960 | 1357.9 |
| **Cost $** | 63.4300 | 0.01585 |
| **Turns** | 6261 | 1.6 |
| **Steps** | 36251 | 9.1 |
| **LLM Latency (sec)** | 85594.65s | 21.39s (Total) / 11.56s (Per Turn) / 5.82s (Per Step) |
| **Errors (Total)** | 46 | 1.1497125718570358 |
| **Runtime Errors (Goja)** | 0 | 0.00 |
| **Tool Errors (BFCL)** | 0 | 0.00 |
| **Tool Calls** | 15723 | 3.9 (Total) / 2.0 (Per Turn) |
| **Task Horizon (Length)** | - | 1.56 Turns |
| **Redundant Tool Calls** | 7098 | 1.77 |
| **Self-Correct (Runtime)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Self-Correct (Tool)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Context Growth** | - | 2691 (Total) / 2230 (Turn) / 89 (Step) |

## 2. Averages by Outcome (Success vs. Failure)
| Metric | Successes | Failures |
|---|---|---|
| **Input Tokens (Test/Turn/Step)** | 33613.5 / 9633.3 / 2391.9 | 69114.0 / 30715.4 / 2555.2 |
| **Output Tokens (Test/Turn/Step)** | 149.9 / 66.9 / 44.7 | 297.0 / 179.7 / 99.4 |
| **Thinking Tokens (Test/Turn/Step)** | 857.3  / 416.2 / 286.2 | 1892.4 / 1172.6 / 550.2 |
| **Turns** | 1.5 | 1.6 |
| **Steps** | 6.6 | 11.7 |
| **LLM Latency (Total)** | 14.37s | 28.89s |
| **LLM Latency (Per Turn)** | 6.51s | 16.94s |
| **LLM Latency (Per Step)** | 4.24s | 7.51s |
| **Context Growth (Total)** | 1878.9 | 3558.1 |
| **Context Growth (Per Turn)**| 1515.1 | 2992.7 |
| **Context Growth (Per Step)**| 48.5 | 132.8 |

## 3. Breakdown by Category

### Category Totals
| Category | Tests | Successes | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | LLM Latency | Runtime Errors | Tool Errors | Redundant Calls | Self-Corrects (Runtime) | Self-Corrects (Tool) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 240 | 23 | 134297 | 77452 | 196736 | 240 | 240 | 3258.79s | 0 | 0 | 45 | 0 | 0 |
| live_irrelevance | 884 | 109 | 1241241 | 91645 | 763968 | 905 | 909 | 9719.17s | 0 | 0 | 46 | 0 | 0 |
| live_multiple | 1053 | 757 | 2188576 | 49832 | 335552 | 1053 | 1053 | 4819.71s | 0 | 0 | 39 | 0 | 0 |
| live_relevance | 16 | 16 | 26068 | 1715 | 11456 | 16 | 16 | 140.09s | 0 | 0 | 1 | 0 | 0 |
| live_simple | 258 | 182 | 180083 | 12500 | 66560 | 258 | 258 | 1050.27s | 0 | 0 | 17 | 0 | 0 |
| multi_turn_base | 200 | 141 | 25481423 | 99370 | 512384 | 730 | 3142 | 9038.23s | 0 | 0 | 736 | 0 | 0 |
| multi_turn_long_context | 200 | 85 | 99697345 | 165122 | 956800 | 630 | 10338 | 17147.87s | 0 | 0 | 1969 | 0 | 0 |
| multi_turn_miss_func | 200 | 67 | 38623756 | 184190 | 1530176 | 820 | 9760 | 21759.13s | 0 | 0 | 2454 | 0 | 0 |
| multi_turn_miss_param | 200 | 78 | 35073030 | 172144 | 895872 | 859 | 9785 | 15983.45s | 0 | 0 | 1787 | 0 | 0 |
| multiple | 200 | 173 | 204029 | 7722 | 41984 | 200 | 200 | 693.68s | 0 | 0 | 0 | 0 | 0 |
| simple_java | 100 | 61 | 67110 | 4660 | 30464 | 100 | 100 | 456.88s | 0 | 0 | 0 | 0 | 0 |
| simple_javascript | 50 | 28 | 35240 | 2453 | 18688 | 50 | 50 | 255.84s | 0 | 0 | 1 | 0 | 0 |
| simple_python | 400 | 346 | 228942 | 15581 | 72320 | 400 | 400 | 1271.54s | 0 | 0 | 3 | 0 | 0 |

### Category Averages
| Category | Success Rate | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | Latency (Total/Turn/Step) | Context Growth (Total/Turn/Step) | Runtime Errors | Tool Errors | Redundant | Runtime Recovery % | Tool Recovery % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 9.6% | 559.6 | 322.7 | 819.7 | 1.0 | 1.0 | 13.58s / 13.58s / 13.58s | 559.6 / 559.6 / 0.0 | 0.00 | 0.00 | 0.19 | 0.0% | 0.0% |
| live_irrelevance | 12.3% | 1404.1 | 103.7 | 864.2 | 1.0 | 1.0 | 10.99s / 10.96s / 10.52s | 1404.1 / 1400.9 / 0.0 | 0.00 | 0.00 | 0.05 | 0.0% | 0.0% |
| live_multiple | 71.9% | 2078.4 | 47.3 | 318.7 | 1.0 | 1.0 | 4.58s / 4.58s / 4.58s | 2078.4 / 2078.4 / 0.0 | 0.00 | 0.00 | 0.04 | 0.0% | 0.0% |
| live_relevance | 100.0% | 1629.2 | 107.2 | 716.0 | 1.0 | 1.0 | 8.76s / 8.76s / 8.76s | 1629.2 / 1629.2 / 0.0 | 0.00 | 0.00 | 0.06 | 0.0% | 0.0% |
| live_simple | 70.5% | 698.0 | 48.4 | 258.0 | 1.0 | 1.0 | 4.07s / 4.07s / 4.07s | 698.0 / 698.0 / 0.0 | 0.00 | 0.00 | 0.07 | 0.0% | 0.0% |
| multi_turn_base | 70.5% | 127407.1 | 496.9 | 2561.9 | 3.6 | 15.7 | 45.19s / 13.44s / 2.96s | 815.3 / 351.4 / 68.2 | 0.00 | 0.00 | 3.68 | 0.0% | 0.0% |
| multi_turn_long_context | 42.5% | 498486.7 | 825.6 | 4784.0 | 3.1 | 51.7 | 85.74s / 37.78s / 1.81s | 28567.2 / 21415.9 / 1551.5 | 0.00 | 0.00 | 9.85 | 0.0% | 0.0% |
| multi_turn_miss_func | 33.5% | 193118.8 | 921.0 | 7650.9 | 4.1 | 48.8 | 108.80s / 44.56s / 2.57s | 1602.0 / 738.3 / 86.9 | 0.00 | 0.00 | 12.27 | 0.0% | 0.0% |
| multi_turn_miss_param | 39.0% | 175365.1 | 860.7 | 4479.4 | 4.3 | 48.9 | 79.92s / 27.23s / 2.82s | 1320.8 / 585.9 / 79.2 | 0.00 | 0.00 | 8.94 | 0.0% | 0.0% |
| multiple | 86.5% | 1020.1 | 38.6 | 209.9 | 1.0 | 1.0 | 3.47s / 3.47s / 3.47s | 1020.1 / 1020.1 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| simple_java | 61.0% | 671.1 | 46.6 | 304.6 | 1.0 | 1.0 | 4.57s / 4.57s / 4.57s | 671.1 / 671.1 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| simple_javascript | 56.0% | 704.8 | 49.1 | 373.8 | 1.0 | 1.0 | 5.12s / 5.12s / 5.12s | 704.8 / 704.8 / 0.0 | 0.00 | 0.00 | 0.02 | 0.0% | 0.0% |
| simple_python | 86.5% | 572.4 | 39.0 | 180.8 | 1.0 | 1.0 | 3.18s / 3.18s / 3.18s | 572.4 / 572.4 / 0.0 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |
