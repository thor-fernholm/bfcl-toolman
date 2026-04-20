# Benchmark Metrics: `ptc-fc | OpenAI/gpt-5-mini-2025-08-07`

## 1. Global Totals & Averages
| Metric | Total (Sum) | Average (Mean per test) |
|---|---|---|
| **Tests Run** | 4254 | - |
| **Successes** | 2721 | 63.96% (Success Rate) |
| **Input Tokens** | 78847753 | 18535.0 |
| **Output Tokens** | 1341473 | 315.3 |
| **Thinking Tokens** | 8150592 | 1916.0 |
| **Turns** | 7336 | 1.7 |
| **Steps** | 15977 | 3.8 |
| **LLM Latency (sec)** | 141883.64s | 33.35s (Total) / 16.82s (Per Turn) / 9.91s (Per Step) |
| **Runtime Errors (Goja)** | 0 | 0.00 |
| **Tool Errors (BFCL)** | 937 | 0.22 |
| **Tool Calls** | 9140 | 2.1 (Total) / 1.1 (Per Turn) |
| **Task Horizon (Length)** | - | 1.72 Turns |
| **Redundant Tool Calls** | 5416 | 1.27 |
| **Self-Correct (Runtime)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Self-Correct (Tool)** | 101 (out of 442 err traces) | 22.9% (Recovery Rate) |
| **Context Growth** | - | 1734 (Total) / 1291 (Turn) / 137 (Step) |

## 2. Averages by Outcome (Success vs. Failure)
| Metric | Successes | Failures |
|---|---|---|
| **Input Tokens (Test/Turn/Step)** | 10518.7 / 4196.0 / 1942.0 | 32763.5 / 9832.8 / 3146.7 |
| **Output Tokens (Test/Turn/Step)** | 237.2 / 160.0 / 90.4 | 454.1 / 168.4 / 78.7 |
| **Thinking Tokens (Test/Turn/Step)** | 1227.3  / 808.6 / 556.1 | 3138.3 / 1263.6 / 622.4 |
| **Turns** | 1.4 | 2.4 |
| **Steps** | 2.4 | 6.2 |
| **LLM Latency (Total)** | 22.10s | 53.33s |
| **LLM Latency (Per Turn)** | 14.50s | 20.93s |
| **LLM Latency (Per Step)** | 9.72s | 10.26s |
| **Context Growth (Total)** | 1469.5 | 2204.7 |
| **Context Growth (Per Turn)**| 1224.7 | 1408.7 |
| **Context Growth (Per Step)**| 120.2 | 165.6 |

## 3. Breakdown by Category

### Category Totals
| Category | Tests | Successes | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | LLM Latency | Runtime Errors | Tool Errors | Redundant Calls | Self-Corrects (Runtime) | Self-Corrects (Tool) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 240 | 191 | 357733 | 48108 | 241088 | 240 | 338 | 4378.76s | 0 | 0 | 12 | 0 | 0 |
| live_irrelevance | 876 | 612 | 3305645 | 251948 | 986944 | 877 | 1587 | 17943.40s | 0 | 0 | 263 | 0 | 0 |
| live_multiple | 1053 | 775 | 1761367 | 71991 | 639552 | 1053 | 1116 | 10569.54s | 0 | 0 | 30 | 0 | 0 |
| live_relevance | 16 | 13 | 26933 | 2599 | 13504 | 16 | 18 | 227.53s | 0 | 0 | 0 | 0 | 0 |
| live_simple | 258 | 197 | 266342 | 16735 | 144832 | 258 | 260 | 2427.61s | 0 | 0 | 1 | 0 | 0 |
| multi_turn_base | 461 | 95 | 14888762 | 205854 | 1664640 | 1621 | 4788 | 28513.18s | 0 | 269 | 1139 | 0 | 25 |
| multi_turn_long_context | 200 | 86 | 31623412 | 277707 | 1291776 | 705 | 2136 | 23360.19s | 0 | 170 | 1235 | 0 | 27 |
| multi_turn_miss_func | 200 | 75 | 13046432 | 220011 | 1460800 | 900 | 2466 | 25043.69s | 0 | 270 | 1376 | 0 | 26 |
| multi_turn_miss_param | 200 | 72 | 12661171 | 192256 | 1250048 | 916 | 2458 | 21778.29s | 0 | 228 | 1310 | 0 | 23 |
| multiple | 200 | 175 | 229140 | 11455 | 110784 | 200 | 201 | 1839.41s | 0 | 0 | 0 | 0 | 0 |
| simple_java | 100 | 56 | 109794 | 6889 | 67072 | 100 | 105 | 1093.70s | 0 | 0 | 5 | 0 | 0 |
| simple_javascript | 50 | 24 | 176975 | 12121 | 78208 | 50 | 97 | 1239.31s | 0 | 0 | 40 | 0 | 0 |
| simple_python | 400 | 350 | 394047 | 23799 | 201344 | 400 | 407 | 3469.04s | 0 | 0 | 5 | 0 | 0 |

### Category Averages
| Category | Success Rate | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | Latency (Total/Turn/Step) | Context Growth (Total/Turn/Step) | Runtime Errors | Tool Errors | Redundant | Runtime Recovery % | Tool Recovery % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 79.6% | 1490.6 | 200.4 | 1004.5 | 1.0 | 1.4 | 18.24s / 18.24s / 13.64s | 737.0 / 737.0 / 122.2 | 0.00 | 0.00 | 0.05 | 0.0% | 0.0% |
| live_irrelevance | 69.9% | 3773.6 | 287.6 | 1126.6 | 1.0 | 1.8 | 20.48s / 20.47s / 11.67s | 947.9 / 947.9 / 187.8 | 0.00 | 0.00 | 0.30 | 0.0% | 0.0% |
| live_multiple | 73.6% | 1672.7 | 68.4 | 607.4 | 1.0 | 1.1 | 10.04s / 10.04s / 9.64s | 1566.6 / 1566.6 / 2.6 | 0.00 | 0.00 | 0.03 | 0.0% | 0.0% |
| live_relevance | 81.2% | 1683.3 | 162.4 | 844.0 | 1.0 | 1.1 | 14.22s / 14.22s / 12.91s | 1264.1 / 1264.1 / 53.3 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| live_simple | 76.4% | 1032.3 | 64.9 | 561.4 | 1.0 | 1.0 | 9.41s / 9.41s / 9.29s | 1014.2 / 1014.2 / 3.3 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| multi_turn_base | 20.6% | 32296.7 | 446.5 | 3610.9 | 3.5 | 10.4 | 61.85s / 20.07s / 6.63s | 786.2 / 369.5 / 169.2 | 0.00 | 0.58 | 2.47 | 0.0% | 18.8% |
| multi_turn_long_context | 43.0% | 158117.1 | 1388.5 | 6458.9 | 3.5 | 10.7 | 116.80s / 36.68s / 10.95s | 13682.5 / 7164.2 / 1257.2 | 0.00 | 0.85 | 6.17 | 0.0% | 29.3% |
| multi_turn_miss_func | 37.5% | 65232.2 | 1100.1 | 7304.0 | 4.5 | 12.3 | 125.22s / 31.14s / 10.26s | 1642.8 / 527.2 / 141.2 | 0.00 | 1.35 | 6.88 | 0.0% | 23.6% |
| multi_turn_miss_param | 36.0% | 63305.9 | 961.3 | 6250.2 | 4.6 | 12.3 | 108.89s / 27.75s / 8.88s | 1219.6 / 382.7 / 108.2 | 0.00 | 1.14 | 6.55 | 0.0% | 21.5% |
| multiple | 87.5% | 1145.7 | 57.3 | 553.9 | 1.0 | 1.0 | 9.20s / 9.20s / 9.15s | 1134.8 / 1134.8 / 0.7 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| simple_java | 56.0% | 1097.9 | 68.9 | 670.7 | 1.0 | 1.1 | 10.94s / 10.94s / 10.37s | 1015.9 / 1015.9 / 4.1 | 0.00 | 0.00 | 0.05 | 0.0% | 0.0% |
| simple_javascript | 48.0% | 3539.5 | 242.4 | 1564.2 | 1.0 | 1.9 | 24.79s / 24.79s / 12.09s | 1124.4 / 1124.4 / 47.9 | 0.00 | 0.00 | 0.80 | 0.0% | 0.0% |
| simple_python | 87.5% | 985.1 | 59.5 | 503.4 | 1.0 | 1.0 | 8.67s / 8.67s / 8.41s | 958.3 / 958.3 / 0.8 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |
