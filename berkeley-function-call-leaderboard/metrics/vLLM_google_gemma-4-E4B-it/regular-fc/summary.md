# Benchmark Metrics: `regular-fc | vLLM/google/gemma-4-E4B-it`

## 1. Global Totals & Averages
| Metric | Total (Sum) | Average (Mean per test) |
|---|---|---|
| **Tests Run** | 3999 | - |
| **Successes** | 2396 | 59.91% (Success Rate) |
| **Input Tokens** | 105227579 | 26313.5 |
| **Output Tokens** | 478560 | 119.7 |
| **Thinking Tokens** | 0 | 0.0 |
| **Cost $** | 0.0000 | 0.00000 |
| **Turns** | 6553 | 1.6 |
| **Steps** | 10962 | 2.7 |
| **LLM Latency (sec)** | 233906.73s | 58.49s (Total) / 17.39s (Per Turn) / 9.26s (Per Step) |
| **Errors (Total)** | 23 | 0.5751437859464866 |
| **Runtime Errors (Goja)** | 0 | 0.00 |
| **Tool Errors (BFCL)** | 0 | 0.00 |
| **Tool Calls** | 6749 | 1.7 (Total) / 0.8 (Per Turn) |
| **Task Horizon (Length)** | - | 1.64 Turns |
| **Redundant Tool Calls** | 624 | 0.16 |
| **Self-Correct (Runtime)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Self-Correct (Tool)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Context Growth** | - | 1829 (Total) / 1516 (Turn) / 75 (Step) |

## 2. Averages by Outcome (Success vs. Failure)
| Metric | Successes | Failures |
|---|---|---|
| **Input Tokens (Test/Turn/Step)** | 11198.1 / 4083.3 / 2476.0 | 48906.4 / 12889.4 / 5901.2 |
| **Output Tokens (Test/Turn/Step)** | 70.8 / 47.4 / 41.9 | 192.7 / 70.3 / 48.0 |
| **Thinking Tokens (Test/Turn/Step)** | 0.0  / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 |
| **Turns** | 1.2 | 2.3 |
| **Steps** | 1.7 | 4.4 |
| **LLM Latency (Total)** | 30.67s | 100.07s |
| **LLM Latency (Per Turn)** | 10.93s | 27.04s |
| **LLM Latency (Per Step)** | 6.75s | 13.02s |
| **Context Growth (Total)** | 1810.0 | 1856.8 |
| **Context Growth (Per Turn)**| 1612.5 | 1372.2 |
| **Context Growth (Per Step)**| 38.4 | 129.5 |

## 3. Breakdown by Meta-Category

### Meta Category Totals
| Meta Category | Tests | Successes | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | LLM Latency | Runtime Errors | Tool Errors | Redundant Calls | Self-Corrects (Runtime) | Self-Corrects (Tool) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 1140 | 937 | 1678975 | 57192 | 0 | 1161 | 1161 | 5405.95s | 0 | 0 | 9 | 0 | 0 |
| multi_turn | 798 | 176 | 100055848 | 336443 | 0 | 3331 | 7740 | 219484.66s | 0 | 0 | 602 | 0 | 0 |
| single_turn | 2061 | 1283 | 3492756 | 84925 | 0 | 2061 | 2061 | 9016.11s | 0 | 0 | 13 | 0 | 0 |

### Meta Category Averages
| Meta Category | Success Rate | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | Latency (Total/Turn/Step) | Context Growth (Total/Turn/Step) | Runtime Errors | Tool Errors | Redundant | Runtime Recovery % | Tool Recovery % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 82.19% | 1472.8 | 50.2 | 0.0 | 1.0 | 1.0 | 4.74s / 4.72s / 4.72s | 1472.8 / 1469.8 / 0.0 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |
| multi_turn | 22.06% | 125383.3 | 421.6 | 0.0 | 4.2 | 9.7 | 275.04s / 69.09s / 28.38s | 2683.3 / 1121.4 / 375.6 | 0.00 | 0.00 | 0.75 | 0.0% | 0.0% |
| single_turn | 62.25% | 1694.7 | 41.2 | 0.0 | 1.0 | 1.0 | 4.37s / 4.37s / 4.37s | 1694.7 / 1694.7 / 0.0 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |

## 4. Breakdown by Category

### Category Totals
| Category | Tests | Successes | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | LLM Latency | Runtime Errors | Tool Errors | Redundant Calls | Self-Corrects (Runtime) | Self-Corrects (Tool) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 240 | 202 | 143437 | 11307 | 0 | 240 | 240 | 819.41s | 0 | 0 | 0 | 0 | 0 |
| live_irrelevance | 884 | 721 | 1503997 | 42719 | 0 | 905 | 905 | 4289.97s | 0 | 0 | 9 | 0 | 0 |
| live_multiple | 1053 | 679 | 2704010 | 50088 | 0 | 1053 | 1053 | 5857.67s | 0 | 0 | 9 | 0 | 0 |
| live_relevance | 16 | 14 | 31541 | 3166 | 0 | 16 | 16 | 296.57s | 0 | 0 | 0 | 0 | 0 |
| live_simple | 258 | 163 | 194039 | 9930 | 0 | 258 | 258 | 688.80s | 0 | 0 | 0 | 0 | 0 |
| multi_turn_base | 200 | 69 | 21812457 | 54547 | 0 | 734 | 1814 | 83890.95s | 0 | 0 | 119 | 0 | 0 |
| multi_turn_long_context | 198 | 48 | 30867131 | 122694 | 0 | 729 | 1928 | 26464.42s | 0 | 0 | 132 | 0 | 0 |
| multi_turn_miss_func | 200 | 5 | 22563376 | 80182 | 0 | 934 | 1937 | 9447.68s | 0 | 0 | 151 | 0 | 0 |
| multi_turn_miss_param | 200 | 54 | 24812884 | 79020 | 0 | 934 | 2061 | 99681.61s | 0 | 0 | 200 | 0 | 0 |
| multiple | 200 | 126 | 244999 | 6290 | 0 | 200 | 200 | 910.88s | 0 | 0 | 0 | 0 | 0 |
| simple_java | 100 | 43 | 69349 | 3841 | 0 | 100 | 100 | 339.85s | 0 | 0 | 1 | 0 | 0 |
| simple_javascript | 50 | 36 | 35952 | 1759 | 0 | 50 | 50 | 143.10s | 0 | 0 | 0 | 0 | 0 |
| simple_python | 400 | 236 | 244407 | 13017 | 0 | 400 | 400 | 1075.82s | 0 | 0 | 3 | 0 | 0 |

### Category Averages
| Category | Success Rate | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | Latency (Total/Turn/Step) | Context Growth (Total/Turn/Step) | Runtime Errors | Tool Errors | Redundant | Runtime Recovery % | Tool Recovery % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 84.17% | 597.7 | 47.1 | 0.0 | 1.0 | 1.0 | 3.41s / 3.41s / 3.41s | 597.7 / 597.7 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| live_irrelevance | 81.56% | 1701.4 | 48.3 | 0.0 | 1.0 | 1.0 | 4.85s / 4.83s / 4.83s | 1701.4 / 1697.5 / 0.0 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |
| live_multiple | 64.48% | 2567.9 | 47.6 | 0.0 | 1.0 | 1.0 | 5.56s / 5.56s / 5.56s | 2567.9 / 2567.9 / 0.0 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |
| live_relevance | 87.50% | 1971.3 | 197.9 | 0.0 | 1.0 | 1.0 | 18.54s / 18.54s / 18.54s | 1971.3 / 1971.3 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| live_simple | 63.18% | 752.1 | 38.5 | 0.0 | 1.0 | 1.0 | 2.67s / 2.67s / 2.67s | 752.1 / 752.1 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| multi_turn_base | 34.50% | 109062.3 | 272.7 | 0.0 | 3.7 | 9.1 | 419.45s / 116.89s / 45.52s | 622.8 / 293.1 / 72.5 | 0.00 | 0.00 | 0.59 | 0.0% | 0.0% |
| multi_turn_long_context | 24.24% | 155894.6 | 619.7 | 0.0 | 3.7 | 9.7 | 133.66s / 37.04s / 13.36s | 8701.6 / 3797.6 / 1266.6 | 0.00 | 0.00 | 0.67 | 0.0% | 0.0% |
| multi_turn_miss_func | 2.50% | 112816.9 | 400.9 | 0.0 | 4.7 | 9.7 | 47.24s / 10.44s / 5.11s | 795.0 / 228.5 / 98.7 | 0.00 | 0.00 | 0.76 | 0.0% | 0.0% |
| multi_turn_miss_param | 27.00% | 124064.4 | 395.1 | 0.0 | 4.7 | 10.3 | 498.41s / 111.66s / 49.37s | 674.1 / 193.4 / 73.6 | 0.00 | 0.00 | 1.00 | 0.0% | 0.0% |
| multiple | 63.00% | 1225.0 | 31.4 | 0.0 | 1.0 | 1.0 | 4.55s / 4.55s / 4.55s | 1225.0 / 1225.0 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| simple_java | 43.00% | 693.5 | 38.4 | 0.0 | 1.0 | 1.0 | 3.40s / 3.40s / 3.40s | 693.5 / 693.5 / 0.0 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |
| simple_javascript | 72.00% | 719.0 | 35.2 | 0.0 | 1.0 | 1.0 | 2.86s / 2.86s / 2.86s | 719.0 / 719.0 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| simple_python | 59.00% | 611.0 | 32.5 | 0.0 | 1.0 | 1.0 | 2.69s / 2.69s / 2.69s | 611.0 / 611.0 / 0.0 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |

