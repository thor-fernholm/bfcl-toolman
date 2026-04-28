# Benchmark Metrics: `ptc-fc | vLLM/google/gemma-4-E4B-it`

## 1. Global Totals & Averages
| Metric | Total (Sum) | Average (Mean per test) |
|---|---|---|
| **Tests Run** | 4001 | - |
| **Successes** | 2633 | 65.81% (Success Rate) |
| **Input Tokens** | 46681390 | 11667.4 |
| **Output Tokens** | 692698 | 173.1 |
| **Thinking Tokens** | 0 | 0.0 |
| **Cost $** | 0.0000 | 0.00000 |
| **Turns** | 6539 | 1.6 |
| **Steps** | 10225 | 2.6 |
| **LLM Latency (sec)** | 193451.75s | 48.35s (Total) / 13.67s (Per Turn) / 7.55s (Per Step) |
| **Errors (Total)** | 15 | 0.3749062734316421 |
| **Runtime Errors (Goja)** | 0 | 0.00 |
| **Tool Errors (BFCL)** | 703 | 0.18 |
| **Tool Calls** | 5919 | 1.5 (Total) / 0.8 (Per Turn) |
| **Task Horizon (Length)** | - | 1.63 Turns |
| **Redundant Tool Calls** | 2597 | 0.65 |
| **Self-Correct (Runtime)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Self-Correct (Tool)** | 18 (out of 415 err traces) | 4.3% (Recovery Rate) |
| **Context Growth** | - | 1467 (Total) / 1224 (Turn) / 74 (Step) |

## 2. Averages by Outcome (Success vs. Failure)
| Metric | Successes | Failures |
|---|---|---|
| **Input Tokens (Test/Turn/Step)** | 5053.6 / 2269.4 / 1703.0 | 24397.1 / 6603.0 / 3577.3 |
| **Output Tokens (Test/Turn/Step)** | 90.8 / 63.0 / 53.4 | 331.6 / 112.8 / 71.4 |
| **Thinking Tokens (Test/Turn/Step)** | 0.0  / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 |
| **Turns** | 1.2 | 2.5 |
| **Steps** | 1.5 | 4.6 |
| **LLM Latency (Total)** | 16.41s | 109.82s |
| **LLM Latency (Per Turn)** | 6.12s | 28.18s |
| **LLM Latency (Per Step)** | 3.89s | 14.60s |
| **Context Growth (Total)** | 1472.3 | 1456.8 |
| **Context Growth (Per Turn)**| 1328.4 | 1024.1 |
| **Context Growth (Per Step)**| 45.3 | 130.6 |

## 3. Breakdown by Meta-Category

### Meta-Category Totals (Unweighted Sums)
| Meta-Category | Tests | Successes | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | LLM Latency | Runtime Errors | Tool Errors | Redundant Calls | Self-Corrects (Runtime) | Self-Corrects (Tool) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| single_turn | 2061 | 1648 | 3022669 | 126370 | 0 | 2061 | 2152 | 5170.40s | 0 | 0 | 6 | 0 | 0 |
| multi_turn | 800 | 146 | 41959350 | 500693 | 0 | 3317 | 6728 | 184859.46s | 0 | 703 | 2588 | 0 | 18 |
| irrelevance | 1140 | 839 | 1699371 | 65635 | 0 | 1161 | 1345 | 3421.89s | 0 | 0 | 3 | 0 | 0 |

### Meta-Category Averages (Weighted)
| Meta-Category | Success Rate | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | Latency (Total/Turn/Step) | Context Growth (Total/Turn/Step) | Runtime Errors | Tool Errors | Redundant | Runtime Recovery % | Tool Recovery % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| single_turn | 78.64% | 1434.5 | 61.6 | 0.0 | 1.0 | 1.0 | 2.61s / 2.61s / 2.50s | 1333.9 / 1333.9 / 7.3 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| multi_turn | 18.25% | 52449.2 | 625.9 | 0.0 | 4.1 | 8.4 | 231.07s / 57.66s / 27.94s | 2101.8 / 890.8 / 321.0 | 0.00 | 0.88 | 3.24 | 0.0% | 4.1% |
| irrelevance | 72.46% | 1383.9 | 55.3 | 0.0 | 1.0 | 1.2 | 2.83s / 2.81s / 2.41s | 1080.2 / 1079.1 / 24.5 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |

**Category Accuracy (Weighted 3:2:1 for Multi:Single:Irrelevance):** 47.41%

## 4. Breakdown by Category

### Category Totals
| Category | Tests | Successes | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | LLM Latency | Runtime Errors | Tool Errors | Redundant Calls | Self-Corrects (Runtime) | Self-Corrects (Tool) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 240 | 169 | 285551 | 12169 | 0 | 240 | 275 | 605.39s | 0 | 0 | 1 | 0 | 0 |
| live_irrelevance | 884 | 658 | 1385962 | 51882 | 0 | 905 | 1052 | 2753.45s | 0 | 0 | 2 | 0 | 0 |
| live_multiple | 1053 | 793 | 1865532 | 65239 | 0 | 1053 | 1105 | 2522.36s | 0 | 0 | 1 | 0 | 0 |
| live_relevance | 16 | 12 | 27858 | 1584 | 0 | 16 | 18 | 63.05s | 0 | 0 | 0 | 0 | 0 |
| live_simple | 258 | 207 | 300068 | 16831 | 0 | 258 | 271 | 628.20s | 0 | 0 | 0 | 0 | 0 |
| multi_turn_base | 200 | 55 | 8614202 | 108016 | 0 | 731 | 1591 | 27533.58s | 0 | 173 | 657 | 0 | 2 |
| multi_turn_long_context | 200 | 45 | 13869504 | 147399 | 0 | 729 | 1537 | 73605.86s | 0 | 165 | 610 | 0 | 1 |
| multi_turn_miss_func | 200 | 2 | 9250877 | 121980 | 0 | 929 | 1726 | 49623.80s | 0 | 174 | 595 | 0 | 1 |
| multi_turn_miss_param | 200 | 44 | 10224767 | 123298 | 0 | 928 | 1874 | 34096.23s | 0 | 191 | 726 | 0 | 14 |
| multiple | 200 | 187 | 251633 | 11211 | 0 | 200 | 203 | 565.96s | 0 | 0 | 0 | 0 | 0 |
| simple_java | 100 | 55 | 122194 | 6753 | 0 | 100 | 110 | 278.25s | 0 | 0 | 2 | 0 | 0 |
| simple_javascript | 50 | 28 | 62744 | 3551 | 0 | 50 | 56 | 152.55s | 0 | 0 | 0 | 0 | 0 |
| simple_python | 400 | 378 | 420498 | 22785 | 0 | 400 | 407 | 1023.08s | 0 | 0 | 3 | 0 | 0 |

### Category Averages
| Category | Success Rate | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | Latency (Total/Turn/Step) | Context Growth (Total/Turn/Step) | Runtime Errors | Tool Errors | Redundant | Runtime Recovery % | Tool Recovery % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 70.42% | 1189.8 | 50.7 | 0.0 | 1.0 | 1.1 | 2.52s / 2.52s / 2.17s | 892.2 / 892.2 / 23.4 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| live_irrelevance | 74.43% | 1567.8 | 58.7 | 0.0 | 1.0 | 1.2 | 3.11s / 3.07s / 2.61s | 1258.5 / 1256.3 / 25.2 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| live_multiple | 75.31% | 1771.6 | 62.0 | 0.0 | 1.0 | 1.0 | 2.40s / 2.40s / 2.34s | 1678.2 / 1678.2 / 4.2 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| live_relevance | 75.00% | 1741.1 | 99.0 | 0.0 | 1.0 | 1.1 | 3.94s / 3.94s / 3.50s | 1419.6 / 1419.6 / 37.9 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| live_simple | 80.23% | 1163.1 | 65.2 | 0.0 | 1.0 | 1.1 | 2.43s / 2.43s / 2.21s | 1049.4 / 1049.4 / 14.1 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| multi_turn_base | 27.50% | 43071.0 | 540.1 | 0.0 | 3.7 | 8.0 | 137.67s / 37.61s / 16.76s | 768.0 / 345.5 / 110.0 | 0.00 | 0.86 | 3.29 | 0.0% | 2.0% |
| multi_turn_long_context | 22.50% | 69347.5 | 737.0 | 0.0 | 3.6 | 7.7 | 368.03s / 99.55s / 46.12s | 5735.8 / 2618.4 / 935.5 | 0.00 | 0.82 | 3.05 | 0.0% | 1.0% |
| multi_turn_miss_func | 1.00% | 46254.4 | 609.9 | 0.0 | 4.6 | 8.6 | 248.12s / 55.18s / 30.10s | 1024.5 / 322.4 / 136.2 | 0.00 | 0.87 | 2.98 | 0.0% | 1.0% |
| multi_turn_miss_param | 22.00% | 51123.8 | 616.5 | 0.0 | 4.6 | 9.4 | 170.48s / 38.29s / 18.77s | 879.1 / 277.0 / 102.5 | 0.00 | 0.95 | 3.63 | 0.0% | 12.4% |
| multiple | 93.50% | 1258.2 | 56.1 | 0.0 | 1.0 | 1.0 | 2.83s / 2.83s / 2.79s | 1222.7 / 1222.7 / 3.2 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| simple_java | 55.00% | 1221.9 | 67.5 | 0.0 | 1.0 | 1.1 | 2.78s / 2.78s / 2.53s | 1008.9 / 1008.9 / 15.9 | 0.00 | 0.00 | 0.02 | 0.0% | 0.0% |
| simple_javascript | 56.00% | 1254.9 | 71.0 | 0.0 | 1.0 | 1.1 | 3.05s / 3.05s / 2.69s | 988.8 / 988.8 / 21.6 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| simple_python | 94.50% | 1051.2 | 57.0 | 0.0 | 1.0 | 1.0 | 2.56s / 2.56s / 2.48s | 1014.4 / 1014.4 / 3.3 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |

