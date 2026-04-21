# Benchmark Metrics: `regular-fc | OpenAI/gpt-5-mini-2025-08-07`

## 1. Global Totals & Averages
| Metric | Total (Sum) | Average (Mean per test) |
|---|---|---|
| **Tests Run** | 4001 | - |
| **Successes** | 2063 | 51.56% (Success Rate) |
| **Input Tokens** | 210925303 | 52718.1 |
| **Output Tokens** | 863800 | 215.9 |
| **Thinking Tokens** | 5452224 | 1362.7 |
| **Cost $** | 65.3634 | 0.01634 |
| **Turns** | 6286 | 1.6 |
| **Steps** | 20664 | 5.2 |
| **LLM Latency (sec)** | 107482.65s | 26.86s (Total) / 14.91s (Per Turn) / 8.34s (Per Step) |
| **Errors (Total)** | 100 | 2.499375156210947 |
| **Runtime Errors (Goja)** | 0 | 0.00 |
| **Tool Errors (BFCL)** | 0 | 0.00 |
| **Tool Calls** | 15958 | 4.0 (Total) / 2.0 (Per Turn) |
| **Task Horizon (Length)** | - | 1.57 Turns |
| **Redundant Tool Calls** | 7284 | 1.82 |
| **Self-Correct (Runtime)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Self-Correct (Tool)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Context Growth** | - | 2848 (Total) / 2287 (Turn) / 96 (Step) |

## 2. Averages by Outcome (Success vs. Failure)
| Metric | Successes | Failures |
|---|---|---|
| **Input Tokens (Test/Turn/Step)** | 41367.1 / 11622.4 / 3039.5 | 64801.3 / 29098.3 / 3349.1 |
| **Output Tokens (Test/Turn/Step)** | 166.6 / 71.2 / 46.0 | 268.3 / 141.5 / 63.6 |
| **Thinking Tokens (Test/Turn/Step)** | 889.3  / 420.7 / 282.8 | 1866.7 / 1160.9 / 579.6 |
| **Turns** | 1.5 | 1.6 |
| **Steps** | 4.1 | 6.3 |
| **LLM Latency (Total)** | 19.25s | 34.97s |
| **LLM Latency (Per Turn)** | 9.28s | 20.91s |
| **LLM Latency (Per Step)** | 6.20s | 10.62s |
| **Context Growth (Total)** | 2455.8 | 3265.7 |
| **Context Growth (Per Turn)**| 1731.5 | 2878.1 |
| **Context Growth (Per Step)**| 78.3 | 115.7 |

## 3. Breakdown by Category

### Category Totals
| Category | Tests | Successes | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | LLM Latency | Runtime Errors | Tool Errors | Redundant Calls | Self-Corrects (Runtime) | Self-Corrects (Tool) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 240 | 22 | 134297 | 14475 | 200576 | 240 | 243 | 3813.36s | 0 | 0 | 40 | 0 | 0 |
| live_irrelevance | 884 | 117 | 1241241 | 76756 | 765440 | 905 | 930 | 14490.07s | 0 | 0 | 45 | 0 | 0 |
| live_multiple | 1053 | 753 | 2188576 | 49274 | 325248 | 1053 | 1053 | 6847.20s | 0 | 0 | 36 | 0 | 0 |
| live_relevance | 16 | 15 | 26068 | 1789 | 10112 | 16 | 16 | 187.29s | 0 | 0 | 0 | 0 | 0 |
| live_simple | 258 | 180 | 180083 | 12651 | 65280 | 258 | 258 | 1457.43s | 0 | 0 | 14 | 0 | 0 |
| multi_turn_base | 200 | 128 | 25424890 | 105629 | 575808 | 710 | 2606 | 13452.34s | 0 | 0 | 872 | 0 | 0 |
| multi_turn_long_context | 200 | 99 | 107843868 | 220632 | 938432 | 645 | 6828 | 22113.56s | 0 | 0 | 1976 | 0 | 0 |
| multi_turn_miss_func | 200 | 69 | 38215010 | 190337 | 1508608 | 821 | 4504 | 24663.10s | 0 | 0 | 2601 | 0 | 0 |
| multi_turn_miss_param | 200 | 78 | 35135949 | 161917 | 900224 | 888 | 3476 | 16719.35s | 0 | 0 | 1697 | 0 | 0 |
| multiple | 200 | 166 | 204029 | 7818 | 41280 | 200 | 200 | 981.99s | 0 | 0 | 0 | 0 | 0 |
| simple_java | 100 | 62 | 67110 | 4705 | 30848 | 100 | 100 | 652.82s | 0 | 0 | 0 | 0 | 0 |
| simple_javascript | 50 | 26 | 35240 | 2303 | 18688 | 50 | 50 | 343.84s | 0 | 0 | 0 | 0 | 0 |
| simple_python | 400 | 348 | 228942 | 15514 | 71680 | 400 | 400 | 1760.30s | 0 | 0 | 3 | 0 | 0 |

### Category Averages
| Category | Success Rate | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | Latency (Total/Turn/Step) | Context Growth (Total/Turn/Step) | Runtime Errors | Tool Errors | Redundant | Runtime Recovery % | Tool Recovery % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| irrelevance | 9.2% | 559.6 | 60.3 | 835.7 | 1.0 | 1.0 | 15.89s / 15.89s / 15.35s | 559.6 / 559.6 / 0.0 | 0.00 | 0.00 | 0.17 | 0.0% | 0.0% |
| live_irrelevance | 13.2% | 1404.1 | 86.8 | 865.9 | 1.0 | 1.1 | 16.39s / 16.34s / 15.40s | 1404.1 / 1400.9 / 0.0 | 0.00 | 0.00 | 0.05 | 0.0% | 0.0% |
| live_multiple | 71.5% | 2078.4 | 46.8 | 308.9 | 1.0 | 1.0 | 6.50s / 6.50s / 6.50s | 2078.4 / 2078.4 / 0.0 | 0.00 | 0.00 | 0.03 | 0.0% | 0.0% |
| live_relevance | 93.8% | 1629.2 | 111.8 | 632.0 | 1.0 | 1.0 | 11.71s / 11.71s / 11.71s | 1629.2 / 1629.2 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| live_simple | 69.8% | 698.0 | 49.0 | 253.0 | 1.0 | 1.0 | 5.65s / 5.65s / 5.65s | 698.0 / 698.0 / 0.0 | 0.00 | 0.00 | 0.05 | 0.0% | 0.0% |
| multi_turn_base | 64.0% | 127124.4 | 528.1 | 2879.0 | 3.5 | 13.0 | 67.26s / 24.77s / 5.01s | 852.0 / 404.8 / 70.3 | 0.00 | 0.00 | 4.36 | 0.0% | 0.0% |
| multi_turn_long_context | 49.5% | 539219.3 | 1103.2 | 4692.2 | 3.2 | 34.1 | 110.57s / 45.92s / 3.88s | 31705.0 / 22621.3 / 1695.6 | 0.00 | 0.00 | 9.88 | 0.0% | 0.0% |
| multi_turn_miss_func | 34.5% | 191075.0 | 951.7 | 7543.0 | 4.1 | 22.5 | 123.32s / 50.19s / 5.66s | 1654.7 / 730.9 / 89.0 | 0.00 | 0.00 | 13.01 | 0.0% | 0.0% |
| multi_turn_miss_param | 39.0% | 175679.7 | 809.6 | 4501.1 | 4.4 | 17.4 | 83.60s / 25.00s / 4.70s | 1236.0 / 478.0 / 73.4 | 0.00 | 0.00 | 8.48 | 0.0% | 0.0% |
| multiple | 83.0% | 1020.1 | 39.1 | 206.4 | 1.0 | 1.0 | 4.91s / 4.91s / 4.91s | 1020.1 / 1020.1 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| simple_java | 62.0% | 671.1 | 47.0 | 308.5 | 1.0 | 1.0 | 6.53s / 6.53s / 6.53s | 671.1 / 671.1 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| simple_javascript | 52.0% | 704.8 | 46.1 | 373.8 | 1.0 | 1.0 | 6.88s / 6.88s / 6.88s | 704.8 / 704.8 / 0.0 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| simple_python | 87.0% | 572.4 | 38.8 | 179.2 | 1.0 | 1.0 | 4.40s / 4.40s / 4.40s | 572.4 / 572.4 / 0.0 | 0.00 | 0.00 | 0.01 | 0.0% | 0.0% |
