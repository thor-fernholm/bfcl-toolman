# Benchmark Metrics: `ptc-fc | OpenAI/gpt-5-mini-2025-08-07`

## 1. Global Totals & Averages
| Metric | Total (Sum) | Average (Mean per test) |
|---|---|---|
| **Tests Run** | 4001 | - |
| **Successes** | 2736 | 68.38% (Success Rate) |
| **Input Tokens** | 74714117 | 18673.9 |
| **Output Tokens** | 1345104 | 336.2 |
| **Thinking Tokens** | 7316544 | 1828.7 |
| **Cost $** | 36.0018 | 0.008998 |
| **Turns** | 6465 | 1.6 |
| **Steps** | 13086 | 3.3 |
| **LLM Latency (sec)** | 177023.40s | 44.24s (Total) / 25.01s (Per Turn) / 15.56s (Per Step) |
| **Errors (Total)** | 19 | 0.47488127968008 |
| **Runtime Errors (Goja)** | 0 | 0.00 |
| **Tool Errors (BFCL)** | 826 | 0.21 |
| **Tool Calls** | 8933 | 2.2 (Total) / 1.2 (Per Turn) |
| **Task Horizon (Length)** | - | 1.62 Turns |
| **Redundant Tool Calls** | 5266 | 1.32 |
| **Self-Correct (Runtime)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Self-Correct (Tool)** | 106 (out of 394 err traces) | 26.9% (Recovery Rate) |
| **Context Growth** | - | 1724 (Total) / 1322 (Turn) / 140 (Step) |

## 2. Averages by Outcome (Success vs. Failure)
| Metric | Successes | Failures |
|---|---|---|
| **Input Tokens (Test/Turn/Step)** | 12941.6 / 4951.2 / 1962.9 | 31071.8 / 9218.2 / 3240.1 |
| **Output Tokens (Test/Turn/Step)** | 264.6 / 167.5 / 91.1 | 491.1 / 178.2 / 86.6 |
| **Thinking Tokens (Test/Turn/Step)** | 1281.4  / 840.0 / 562.8 | 3012.5 / 1267.0 / 690.2 |
| **Turns** | 1.4 | 2.2 |
| **Steps** | 2.5 | 5.0 |
| **LLM Latency (Total)** | 33.42s | 67.66s |
| **LLM Latency (Per Turn)** | 22.69s | 30.03s |
| **LLM Latency (Per Step)** | 14.75s | 17.30s |
| **Context Growth (Total)** | 1477.6 | 2258.1 |
| **Context Growth (Per Turn)**| 1226.9 | 1527.3 |
| **Context Growth (Per Step)**| 136.9 | 146.0 |

## 3. Breakdown by Category

### Category Totals
| Category | Tests | Successes | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | LLM Latency | Runtime Errors | Tool Errors | Redundant Calls | Self-Corrects (Runtime) | Self-Corrects (Tool) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 240 | 193 | 357656 | 45595 | 243904 | 240 | 340 | 5428.11s | 0 | 0 | 10 | 0 | 0 |
| live_irrelevance | 884 | 611 | 6875408 | 297401 | 1121664 | 905 | 1779 | 35863.55s | 0 | 0 | 410 | 0 | 0 |
| live_multiple | 1053 | 783 | 1728049 | 72977 | 637760 | 1053 | 1106 | 14817.18s | 0 | 0 | 20 | 0 | 0 |
| live_relevance | 16 | 14 | 60375 | 3593 | 16960 | 16 | 28 | 420.22s | 0 | 0 | 11 | 0 | 0 |
| live_simple | 258 | 203 | 265476 | 16342 | 145536 | 258 | 260 | 3482.09s | 0 | 0 | 2 | 0 | 0 |
| multi_turn_base | 200 | 101 | 8914028 | 132845 | 830080 | 731 | 1792 | 23838.69s | 0 | 171 | 863 | 0 | 32 |
| multi_turn_long_context | 200 | 81 | 29975005 | 264825 | 1275584 | 692 | 2106 | 29312.85s | 0 | 192 | 1238 | 0 | 26 |
| multi_turn_miss_func | 200 | 69 | 13539255 | 260884 | 1461120 | 899 | 2519 | 29120.14s | 0 | 270 | 1432 | 0 | 23 |
| multi_turn_miss_param | 200 | 74 | 11915658 | 193719 | 1111232 | 921 | 2322 | 21646.60s | 0 | 193 | 1206 | 0 | 25 |
| multiple | 200 | 171 | 229720 | 11682 | 106560 | 200 | 202 | 2453.10s | 0 | 0 | 1 | 0 | 0 |
| simple_java | 100 | 58 | 103643 | 6541 | 67200 | 100 | 101 | 1607.78s | 0 | 0 | 1 | 0 | 0 |
| simple_javascript | 50 | 21 | 357441 | 14790 | 97088 | 50 | 125 | 2430.66s | 0 | 0 | 69 | 0 | 0 |
| simple_python | 400 | 357 | 392403 | 23910 | 201856 | 400 | 406 | 6602.44s | 0 | 0 | 3 | 0 | 0 |

### Category Averages
| Category | Success Rate | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | Latency (Total/Turn/Step) | Context Growth (Total/Turn/Step) | Runtime Errors | Tool Errors | Redundant | Runtime Recovery % | Tool Recovery % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 80.4% | 1490.2 | 190.0 | 1016.3 | 1.0 | 1.4 | 22.62s / 22.62s / 16.75s | 715.3 / 715.3 / 114.3 | 0.00 | 0.00 | 0.04 | 0.0% | 0.0% |
| live_irrelevance | 69.1% | 7777.6 | 336.4 | 1268.9 | 1.0 | 2.0 | 40.57s / 38.29s / 21.56s | 1141.6 / 1125.6 / 262.9 | 0.00 | 0.00 | 0.46 | 0.0% | 0.0% |
| live_multiple | 74.4% | 1641.1 | 69.3 | 605.7 | 1.0 | 1.1 | 14.07s / 14.07s / 13.62s | 1564.2 / 1564.2 / 3.0 | 0.00 | 0.00 | 0.02 | 0.0% | 0.0% |
| live_relevance | 87.5% | 3773.4 | 224.6 | 1060.0 | 1.0 | 1.8 | 26.26s / 26.26s / 16.92s | 1253.5 / 1253.5 / 55.7 | 0.00 | 0.00 | 0.69 | 0.0% | 0.0% |
| live_simple | 78.7% | 1029.0 | 63.3 | 564.1 | 1.0 | 1.0 | 13.50s / 13.50s / 13.46s | 1017.3 / 1017.3 / 0.5 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |
| multi_turn_base | 50.5% | 44570.1 | 664.2 | 4150.4 | 3.7 | 9.0 | 119.19s / 34.77s / 13.67s | 823.1 / 342.5 / 107.0 | 0.00 | 0.85 | 4.32 | 0.0% | 34.8% |
| multi_turn_long_context | 40.5% | 149875.0 | 1324.1 | 6377.9 | 3.5 | 10.5 | 146.56s / 47.87s / 13.87s | 11397.5 / 5833.6 / 1096.1 | 0.00 | 0.96 | 6.19 | 0.0% | 27.1% |
| multi_turn_miss_func | 34.5% | 67696.3 | 1304.4 | 7305.6 | 4.5 | 12.6 | 145.60s / 36.87s / 11.61s | 1714.5 / 573.4 / 143.8 | 0.00 | 1.35 | 7.16 | 0.0% | 21.7% |
| multi_turn_miss_param | 37.0% | 59578.3 | 968.6 | 5556.2 | 4.6 | 11.6 | 108.23s / 25.30s / 9.52s | 1135.6 / 340.2 / 107.7 | 0.00 | 0.96 | 6.03 | 0.0% | 25.0% |
| multiple | 85.5% | 1148.6 | 58.4 | 532.8 | 1.0 | 1.0 | 12.27s / 12.27s / 12.11s | 1137.0 / 1137.0 / 3.2 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |
| simple_java | 58.0% | 1036.4 | 65.4 | 672.0 | 1.0 | 1.0 | 16.08s / 16.08s / 15.95s | 1016.3 / 1016.3 / 1.5 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |
| simple_javascript | 42.0% | 7148.8 | 295.8 | 1941.8 | 1.0 | 2.5 | 48.61s / 48.61s / 18.01s | 1258.8 / 1258.8 / 52.3 | 0.00 | 0.00 | 1.38 | 0.0% | 0.0% |
| simple_python | 89.2% | 981.0 | 59.8 | 504.6 | 1.0 | 1.0 | 16.51s / 16.51s / 16.07s | 956.8 / 956.8 / 1.7 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |
