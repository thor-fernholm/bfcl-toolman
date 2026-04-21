# Benchmark Metrics: `ptc-fc | OpenAI/gpt-5-mini-2025-08-07`

## 1. Global Totals & Averages
| Metric | Total (Sum) | Average (Mean per test) |
|---|---|---|
| **Tests Run** | 4000 | - |
| **Successes** | 2758 | 68.95% (Success Rate) |
| **Input Tokens** | 85208088 | 21302.0 |
| **Output Tokens** | 1508841 | 377.2 |
| **Thinking Tokens** | 7628352 | 1907.1 |
| **Cost $** | 39.5764 | 0.00989 |
| **Turns** | 6440 | 1.6 |
| **Steps** | 13320 | 3.3 |
| **LLM Latency (sec)** | 118960.72s | 29.74s (Total) / 17.56s (Per Turn) / 10.55s (Per Step) |
| **Errors (Total)** | 20 | 0.5 |
| **Runtime Errors (Goja)** | 0 | 0.00 |
| **Tool Errors (BFCL)** | 819 | 0.20 |
| **Tool Calls** | 9178 | 2.3 (Total) / 1.2 (Per Turn) |
| **Task Horizon (Length)** | - | 1.61 Turns |
| **Redundant Tool Calls** | 5563 | 1.39 |
| **Self-Correct (Runtime)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Self-Correct (Tool)** | 92 (out of 391 err traces) | 23.5% (Recovery Rate) |
| **Context Growth** | - | 1681 (Total) / 1327 (Turn) / 116 (Step) |

## 2. Averages by Outcome (Success vs. Failure)
| Metric | Successes | Failures |
|---|---|---|
| **Input Tokens (Test/Turn/Step)** | 17533.4 / 7893.8 / 1970.7 | 29670.7 / 9040.3 / 3165.5 |
| **Output Tokens (Test/Turn/Step)** | 312.0 / 203.5 / 92.3 | 522.0 / 198.5 / 90.2 |
| **Thinking Tokens (Test/Turn/Step)** | 1311.2  / 867.8 / 560.1 | 3230.3 / 1355.0 / 698.6 |
| **Turns** | 1.4 | 2.2 |
| **Steps** | 2.5 | 5.1 |
| **LLM Latency (Total)** | 23.18s | 44.32s |
| **LLM Latency (Per Turn)** | 16.53s | 19.84s |
| **LLM Latency (Per Step)** | 10.27s | 11.18s |
| **Context Growth (Total)** | 1559.2 | 1951.0 |
| **Context Growth (Per Turn)**| 1325.5 | 1329.7 |
| **Context Growth (Per Step)**| 111.8 | 124.7 |

## 3. Breakdown by Category

### Category Totals
| Category | Tests | Successes | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | LLM Latency | Runtime Errors | Tool Errors | Redundant Calls | Self-Corrects (Runtime) | Self-Corrects (Tool) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 240 | 193 | 326260 | 46243 | 222336 | 240 | 317 | 4858.57s | 0 | 0 | 6 | 0 | 0 |
| live_irrelevance | 883 | 629 | 23562212 | 433951 | 1287680 | 893 | 2095 | 27561.08s | 0 | 0 | 748 | 0 | 0 |
| live_multiple | 1053 | 790 | 1724026 | 70119 | 615744 | 1053 | 1099 | 10943.85s | 0 | 0 | 14 | 0 | 0 |
| live_relevance | 16 | 13 | 24570 | 2591 | 15296 | 16 | 17 | 275.07s | 0 | 0 | 0 | 0 | 0 |
| live_simple | 258 | 201 | 263162 | 16798 | 147264 | 258 | 258 | 2546.02s | 0 | 0 | 0 | 0 | 0 |
| multi_turn_base | 200 | 94 | 8867221 | 152560 | 905088 | 721 | 1784 | 13915.56s | 0 | 174 | 870 | 0 | 19 |
| multi_turn_long_context | 200 | 85 | 23829404 | 247747 | 1273280 | 711 | 2069 | 16802.23s | 0 | 193 | 1174 | 0 | 25 |
| multi_turn_miss_func | 200 | 71 | 13053358 | 251869 | 1489664 | 889 | 2457 | 18386.63s | 0 | 243 | 1384 | 0 | 24 |
| multi_turn_miss_param | 200 | 71 | 12661846 | 230392 | 1222848 | 909 | 2425 | 15780.05s | 0 | 209 | 1327 | 0 | 24 |
| multiple | 200 | 170 | 230532 | 13336 | 111232 | 200 | 202 | 1933.05s | 0 | 0 | 1 | 0 | 0 |
| simple_java | 100 | 59 | 103673 | 6649 | 71104 | 100 | 101 | 1237.98s | 0 | 0 | 1 | 0 | 0 |
| simple_javascript | 50 | 25 | 175506 | 13210 | 70400 | 50 | 94 | 1211.18s | 0 | 0 | 38 | 0 | 0 |
| simple_python | 400 | 357 | 386318 | 23376 | 196416 | 400 | 402 | 3509.43s | 0 | 0 | 0 | 0 | 0 |

### Category Averages
| Category | Success Rate | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | Latency (Total/Turn/Step) | Context Growth (Total/Turn/Step) | Runtime Errors | Tool Errors | Redundant | Runtime Recovery % | Tool Recovery % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 80.4% | 1359.4 | 192.7 | 926.4 | 1.0 | 1.3 | 20.24s / 20.24s / 15.93s | 760.2 / 760.2 / 90.1 | 0.00 | 0.00 | 0.03 | 0.0% | 0.0% |
| live_irrelevance | 71.2% | 26684.3 | 491.5 | 1458.3 | 1.0 | 2.4 | 31.21s / 28.42s / 13.15s | 1378.3 / 1377.4 / 185.4 | 0.00 | 0.00 | 0.85 | 0.0% | 0.0% |
| live_multiple | 75.0% | 1637.3 | 66.6 | 584.8 | 1.0 | 1.0 | 10.39s / 10.39s / 10.18s | 1569.2 / 1569.2 / 2.8 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |
| live_relevance | 81.2% | 1535.6 | 161.9 | 956.0 | 1.0 | 1.1 | 17.19s / 17.19s / 16.19s | 1350.2 / 1350.2 / 22.6 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| live_simple | 77.9% | 1020.0 | 65.1 | 570.8 | 1.0 | 1.0 | 9.87s / 9.87s / 9.87s | 1020.0 / 1020.0 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| multi_turn_base | 47.0% | 44336.1 | 762.8 | 4525.4 | 3.6 | 8.9 | 69.58s / 21.94s / 7.91s | 844.7 / 375.7 / 110.0 | 0.00 | 0.87 | 4.35 | 0.0% | 20.9% |
| multi_turn_long_context | 42.5% | 119147.0 | 1238.7 | 6366.4 | 3.6 | 10.3 | 84.01s / 25.37s / 8.11s | 9373.3 / 4623.1 / 987.2 | 0.00 | 0.96 | 5.87 | 0.0% | 25.3% |
| multi_turn_miss_func | 35.5% | 65266.8 | 1259.3 | 7448.3 | 4.4 | 12.3 | 91.93s / 25.45s / 7.71s | 1653.0 / 618.0 / 144.6 | 0.00 | 1.22 | 6.92 | 0.0% | 24.7% |
| multi_turn_miss_param | 35.5% | 63309.2 | 1152.0 | 6114.2 | 4.5 | 12.1 | 78.90s / 20.31s / 6.39s | 1233.3 / 411.5 / 108.4 | 0.00 | 1.04 | 6.63 | 0.0% | 23.1% |
| multiple | 85.0% | 1152.7 | 66.7 | 556.2 | 1.0 | 1.0 | 9.67s / 9.67s / 9.51s | 1130.9 / 1130.9 / 2.2 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |
| simple_java | 59.0% | 1036.7 | 66.5 | 711.0 | 1.0 | 1.0 | 12.38s / 12.38s / 12.21s | 1016.2 / 1016.2 / 1.6 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |
| simple_javascript | 50.0% | 3510.1 | 264.2 | 1408.0 | 1.0 | 1.9 | 24.22s / 24.22s / 12.31s | 1114.6 / 1114.6 / 72.4 | 0.00 | 0.00 | 0.76 | 0.0% | 0.0% |
| simple_python | 89.2% | 965.8 | 58.4 | 491.0 | 1.0 | 1.0 | 8.77s / 8.77s / 8.70s | 956.0 / 956.0 / 0.8 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
