# Benchmark Metrics: `regular-fc | OpenAI/gpt-5-mini-2025-08-07`

## 1. Global Totals & Averages
| Metric | Total (Sum) | Average (Mean per test) |
|---|---|---|
| **Tests Run** | 4001 | - |
| **Successes** | 2085 | 52.11% (Success Rate) |
| **Input Tokens** | 202464365 | 50603.4 |
| **Output Tokens** | 837674 | 209.4 |
| **Thinking Tokens** | 5006144 | 1251.2 |
| **Cost $** | 62.3037 | 0.015572 |
| **Turns** | 6373 | 1.6 |
| **Steps** | 25577 | 6.4 |
| **LLM Latency (sec)** | 98464.52s | 24.61s (Total) / 11.78s (Per Turn) / 5.82s (Per Step) |
| **Errors (Total)** | 10 | 0.24993751562109473 |
| **Runtime Errors (Goja)** | 0 | 0.00 |
| **Tool Errors (BFCL)** | 0 | 0.00 |
| **Tool Calls** | 14878 | 3.7 (Total) / 1.8 (Per Turn) |
| **Task Horizon (Length)** | - | 1.59 Turns |
| **Redundant Tool Calls** | 6137 | 1.53 |
| **Self-Correct (Runtime)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Self-Correct (Tool)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Context Growth** | - | 2775 (Total) / 2167 (Turn) / 91 (Step) |

## 2. Averages by Outcome (Success vs. Failure)
| Metric | Successes | Failures |
|---|---|---|
| **Input Tokens (Test/Turn/Step)** | 40760.9 / 11652.1 / 2697.5 | 61314.1 / 25739.0 / 2869.0 |
| **Output Tokens (Test/Turn/Step)** | 158.1 / 70.8 / 45.1 | 265.2 / 151.5 / 91.8 |
| **Thinking Tokens (Test/Turn/Step)** | 862.8  / 415.8 / 287.0 | 1673.9 / 1002.5 / 578.3 |
| **Turns** | 1.6 | 1.6 |
| **Steps** | 5.1 | 7.8 |
| **LLM Latency (Total)** | 18.38s | 31.39s |
| **LLM Latency (Per Turn)** | 7.52s | 16.40s |
| **LLM Latency (Per Step)** | 4.44s | 7.32s |
| **Context Growth (Total)** | 2486.2 | 3089.3 |
| **Context Growth (Per Turn)**| 1795.9 | 2570.9 |
| **Context Growth (Per Step)**| 79.1 | 104.2 |

## 3. Breakdown by Category

### Category Totals
| Category | Tests | Successes | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | LLM Latency | Runtime Errors | Tool Errors | Redundant Calls | Self-Corrects (Runtime) | Self-Corrects (Tool) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 240 | 20 | 134297 | 26711 | 190144 | 240 | 241 | 2502.62s | 0 | 0 | 29 | 0 | 0 |
| live_irrelevance | 884 | 101 | 1241241 | 124026 | 783552 | 905 | 906 | 8958.75s | 0 | 0 | 71 | 0 | 0 |
| live_multiple | 1053 | 769 | 2188576 | 49724 | 353408 | 1053 | 1053 | 4829.59s | 0 | 0 | 34 | 0 | 0 |
| live_relevance | 16 | 15 | 26068 | 1769 | 8896 | 16 | 16 | 109.28s | 0 | 0 | 0 | 0 | 0 |
| live_simple | 258 | 179 | 180083 | 12517 | 65728 | 258 | 258 | 1031.97s | 0 | 0 | 15 | 0 | 0 |
| multi_turn_base | 200 | 134 | 24616763 | 90993 | 467456 | 729 | 2676 | 11467.48s | 0 | 0 | 593 | 0 | 0 |
| multi_turn_long_context | 200 | 100 | 103472544 | 188434 | 844224 | 665 | 8646 | 23483.80s | 0 | 0 | 1678 | 0 | 0 |
| multi_turn_miss_func | 200 | 67 | 36530222 | 183232 | 1333440 | 850 | 7111 | 28418.37s | 0 | 0 | 2422 | 0 | 0 |
| multi_turn_miss_param | 200 | 80 | 33539250 | 130011 | 795776 | 907 | 3920 | 14676.19s | 0 | 0 | 1292 | 0 | 0 |
| multiple | 200 | 170 | 204029 | 7813 | 41280 | 200 | 200 | 715.90s | 0 | 0 | 0 | 0 | 0 |
| simple_java | 100 | 62 | 67110 | 4601 | 32576 | 100 | 100 | 503.76s | 0 | 0 | 0 | 0 | 0 |
| simple_javascript | 50 | 30 | 35240 | 2367 | 17792 | 50 | 50 | 333.94s | 0 | 0 | 0 | 0 | 0 |
| simple_python | 400 | 358 | 228942 | 15476 | 71872 | 400 | 400 | 1432.86s | 0 | 0 | 3 | 0 | 0 |

### Category Averages
| Category | Success Rate | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | Latency (Total/Turn/Step) | Context Growth (Total/Turn/Step) | Runtime Errors | Tool Errors | Redundant | Runtime Recovery % | Tool Recovery % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 8.3% | 559.6 | 111.3 | 792.3 | 1.0 | 1.0 | 10.43s / 10.43s / 9.77s | 559.6 / 559.6 / 0.0 | 0.00 | 0.00 | 0.12 | 0.0% | 0.0% |
| live_irrelevance | 11.4% | 1404.1 | 140.3 | 886.4 | 1.0 | 1.0 | 10.13s / 10.09s / 9.92s | 1404.1 / 1400.9 / 0.0 | 0.00 | 0.00 | 0.08 | 0.0% | 0.0% |
| live_multiple | 73.0% | 2078.4 | 47.2 | 335.6 | 1.0 | 1.0 | 4.59s / 4.59s / 4.59s | 2078.4 / 2078.4 / 0.0 | 0.00 | 0.00 | 0.03 | 0.0% | 0.0% |
| live_relevance | 93.8% | 1629.2 | 110.6 | 556.0 | 1.0 | 1.0 | 6.83s / 6.83s / 6.83s | 1629.2 / 1629.2 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| live_simple | 69.4% | 698.0 | 48.5 | 254.8 | 1.0 | 1.0 | 4.00s / 4.00s / 4.00s | 698.0 / 698.0 / 0.0 | 0.00 | 0.00 | 0.06 | 0.0% | 0.0% |
| multi_turn_base | 67.0% | 123083.8 | 455.0 | 2337.3 | 3.6 | 13.4 | 57.34s / 17.06s / 4.45s | 766.7 / 325.4 / 67.9 | 0.00 | 0.00 | 2.96 | 0.0% | 0.0% |
| multi_turn_long_context | 50.0% | 517362.7 | 942.2 | 4221.1 | 3.3 | 43.2 | 117.42s / 46.77s / 2.68s | 30543.3 / 20461.5 / 1595.2 | 0.00 | 0.00 | 8.39 | 0.0% | 0.0% |
| multi_turn_miss_func | 33.5% | 182651.1 | 916.2 | 6667.2 | 4.2 | 35.6 | 142.09s / 49.79s / 5.10s | 1561.4 / 676.0 / 88.7 | 0.00 | 0.00 | 12.11 | 0.0% | 0.0% |
| multi_turn_miss_param | 40.0% | 167696.2 | 650.1 | 3978.9 | 4.5 | 19.6 | 73.38s / 20.02s / 3.80s | 1115.0 / 375.0 / 70.9 | 0.00 | 0.00 | 6.46 | 0.0% | 0.0% |
| multiple | 85.0% | 1020.1 | 39.1 | 206.4 | 1.0 | 1.0 | 3.58s / 3.58s / 3.58s | 1020.1 / 1020.1 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| simple_java | 62.0% | 671.1 | 46.0 | 325.8 | 1.0 | 1.0 | 5.04s / 5.04s / 5.04s | 671.1 / 671.1 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| simple_javascript | 60.0% | 704.8 | 47.3 | 355.8 | 1.0 | 1.0 | 6.68s / 6.68s / 6.68s | 704.8 / 704.8 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| simple_python | 89.5% | 572.4 | 38.7 | 179.7 | 1.0 | 1.0 | 3.58s / 3.58s / 3.58s | 572.4 / 572.4 / 0.0 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |
