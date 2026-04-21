# Benchmark Metrics: `ptc-fc | OpenAI/gpt-5-mini-2025-08-07`

## 1. Global Totals & Averages
| Metric | Total (Sum) | Average (Mean per test) |
|---|---|---|
| **Tests Run** | 4000 | - |
| **Successes** | 2758 | 68.95% (Success Rate) |
| **Input Tokens** | 83759576 | 20939.9 |
| **Output Tokens** | 1508597 | 377.1 |
| **Thinking Tokens** | 7630912 | 1907.7 |
| **Cost $** | 39.2189 | 0.00980 |
| **Turns** | 6446 | 1.6 |
| **Steps** | 13388 | 3.3 |
| **LLM Latency (sec)** | 119515.28s | 29.88s (Total) / 17.30s (Per Turn) / 10.50s (Per Step) |
| **Errors (Total)** | 21 | 0.525 |
| **Runtime Errors (Goja)** | 0 | 0.00 |
| **Tool Errors (BFCL)** | 774 | 0.19 |
| **Tool Calls** | 9246 | 2.3 (Total) / 1.2 (Per Turn) |
| **Task Horizon (Length)** | - | 1.61 Turns |
| **Redundant Tool Calls** | 5628 | 1.41 |
| **Self-Correct (Runtime)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Self-Correct (Tool)** | 95 (out of 386 err traces) | 24.6% (Recovery Rate) |
| **Context Growth** | - | 1886 (Total) / 1410 (Turn) / 133 (Step) |

## 2. Averages by Outcome (Success vs. Failure)
| Metric | Successes | Failures |
|---|---|---|
| **Input Tokens (Test/Turn/Step)** | 14718.6 / 6043.4 / 2042.1 | 34755.0 / 10029.8 / 3305.5 |
| **Output Tokens (Test/Turn/Step)** | 297.2 / 198.5 / 93.2 | 554.6 / 198.2 / 93.8 |
| **Thinking Tokens (Test/Turn/Step)** | 1323.2  / 866.9 / 566.5 | 3205.8 / 1349.2 / 708.8 |
| **Turns** | 1.4 | 2.1 |
| **Steps** | 2.5 | 5.1 |
| **LLM Latency (Total)** | 22.91s | 45.35s |
| **LLM Latency (Per Turn)** | 16.14s | 19.89s |
| **LLM Latency (Per Step)** | 10.19s | 11.17s |
| **Context Growth (Total)** | 1684.6 | 2331.8 |
| **Context Growth (Per Turn)**| 1351.9 | 1537.8 |
| **Context Growth (Per Step)**| 123.4 | 152.9 |

## 3. Breakdown by Category

### Category Totals
| Category | Tests | Successes | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | LLM Latency | Runtime Errors | Tool Errors | Redundant Calls | Self-Corrects (Runtime) | Self-Corrects (Tool) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 240 | 193 | 416315 | 47093 | 241024 | 240 | 325 | 4767.29s | 0 | 0 | 17 | 0 | 0 |
| live_irrelevance | 883 | 622 | 10598039 | 394242 | 1238912 | 904 | 1982 | 25555.30s | 0 | 0 | 629 | 0 | 0 |
| live_multiple | 1053 | 780 | 1849266 | 73060 | 634176 | 1053 | 1121 | 11000.65s | 0 | 0 | 36 | 0 | 0 |
| live_relevance | 16 | 15 | 33770 | 2553 | 18560 | 16 | 21 | 307.55s | 0 | 0 | 4 | 0 | 0 |
| live_simple | 258 | 204 | 264885 | 16887 | 145664 | 258 | 259 | 2452.95s | 0 | 0 | 0 | 0 | 0 |
| multi_turn_base | 200 | 99 | 9245713 | 152552 | 905152 | 725 | 1851 | 14391.07s | 0 | 158 | 930 | 0 | 20 |
| multi_turn_long_context | 200 | 82 | 34600186 | 311655 | 1298432 | 701 | 2146 | 18603.84s | 0 | 167 | 1259 | 0 | 22 |
| multi_turn_miss_func | 200 | 69 | 12488496 | 240395 | 1473408 | 880 | 2419 | 18494.63s | 0 | 236 | 1360 | 0 | 18 |
| multi_turn_miss_param | 200 | 79 | 13470050 | 222855 | 1235968 | 919 | 2496 | 16538.52s | 0 | 213 | 1382 | 0 | 35 |
| multiple | 200 | 173 | 229140 | 11196 | 113856 | 200 | 201 | 1944.70s | 0 | 0 | 0 | 0 | 0 |
| simple_java | 100 | 55 | 102485 | 6377 | 69696 | 100 | 100 | 1153.24s | 0 | 0 | 0 | 0 | 0 |
| simple_javascript | 50 | 26 | 64112 | 4941 | 51648 | 50 | 59 | 831.56s | 0 | 0 | 5 | 0 | 0 |
| simple_python | 400 | 361 | 397119 | 24791 | 204416 | 400 | 408 | 3473.99s | 0 | 0 | 6 | 0 | 0 |

### Category Averages
| Category | Success Rate | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | Latency (Total/Turn/Step) | Context Growth (Total/Turn/Step) | Runtime Errors | Tool Errors | Redundant | Runtime Recovery % | Tool Recovery % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 80.4% | 1734.6 | 196.2 | 1004.3 | 1.0 | 1.4 | 19.86s / 19.86s / 15.39s | 789.5 / 789.5 / 69.2 | 0.00 | 0.00 | 0.07 | 0.0% | 0.0% |
| live_irrelevance | 70.4% | 12002.3 | 446.5 | 1403.1 | 1.0 | 2.2 | 28.94s / 27.26s / 13.31s | 1314.7 / 1303.6 / 201.3 | 0.00 | 0.00 | 0.71 | 0.0% | 0.0% |
| live_multiple | 74.1% | 1756.2 | 69.4 | 602.3 | 1.0 | 1.1 | 10.45s / 10.45s / 10.01s | 1568.8 / 1568.8 / 2.2 | 0.00 | 0.00 | 0.03 | 0.0% | 0.0% |
| live_relevance | 93.8% | 2110.6 | 159.6 | 1160.0 | 1.0 | 1.3 | 19.22s / 19.22s / 13.72s | 1288.4 / 1288.4 / 40.5 | 0.00 | 0.00 | 0.25 | 0.0% | 0.0% |
| live_simple | 79.1% | 1026.7 | 65.5 | 564.6 | 1.0 | 1.0 | 9.51s / 9.51s / 9.44s | 1019.2 / 1019.2 / 2.9 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| multi_turn_base | 49.5% | 46228.6 | 762.8 | 4525.8 | 3.6 | 9.3 | 71.96s / 22.10s / 7.80s | 875.3 / 385.1 / 109.1 | 0.00 | 0.79 | 4.65 | 0.0% | 23.8% |
| multi_turn_long_context | 41.0% | 173000.9 | 1558.3 | 6492.2 | 3.5 | 10.7 | 93.02s / 28.57s / 8.87s | 13814.6 / 6678.3 / 1290.1 | 0.00 | 0.83 | 6.29 | 0.0% | 24.4% |
| multi_turn_miss_func | 34.5% | 62442.5 | 1202.0 | 7367.0 | 4.4 | 12.1 | 92.47s / 26.12s / 7.80s | 1515.5 / 569.8 / 139.0 | 0.00 | 1.18 | 6.80 | 0.0% | 17.5% |
| multi_turn_miss_param | 39.5% | 67350.2 | 1114.3 | 6179.8 | 4.6 | 12.5 | 82.69s / 19.29s / 6.60s | 1280.1 / 383.3 / 108.5 | 0.00 | 1.06 | 6.91 | 0.0% | 32.1% |
| multiple | 86.5% | 1145.7 | 56.0 | 569.3 | 1.0 | 1.0 | 9.72s / 9.72s / 9.70s | 1134.8 / 1134.8 / 0.7 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| simple_java | 55.0% | 1024.8 | 63.8 | 697.0 | 1.0 | 1.0 | 11.53s / 11.53s / 11.53s | 1024.8 / 1024.8 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| simple_javascript | 52.0% | 1282.2 | 98.8 | 1033.0 | 1.0 | 1.2 | 16.63s / 16.63s / 13.29s | 915.5 / 915.5 / 43.0 | 0.00 | 0.00 | 0.10 | 0.0% | 0.0% |
| simple_python | 90.2% | 992.8 | 62.0 | 511.0 | 1.0 | 1.0 | 8.68s / 8.68s / 8.41s | 959.7 / 959.7 / 1.0 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |
