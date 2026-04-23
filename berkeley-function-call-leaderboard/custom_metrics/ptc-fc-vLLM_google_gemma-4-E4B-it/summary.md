# Benchmark Metrics: `ptc-fc | vLLM/google/gemma-4-E4B-it`

## 1. Global Totals & Averages
| Metric | Total (Sum) | Average (Mean per test) |
|---|---|---|
| **Tests Run** | 200 | - |
| **Successes** | 51 | 25.50% (Success Rate) |
| **Input Tokens** | 17103084 | 85515.4 |
| **Output Tokens** | 210614 | 1053.1 |
| **Thinking Tokens** | 0 | 0.0 |
| **Turns** | 731 | 3.7 |
| **Steps** | 1575 | 7.9 |
| **LLM Latency (sec)** | 9433.83s | 47.17s (Total) / 12.06s (Per Turn) / 5.51s (Per Step) |
| **Runtime Errors (Goja)** | 0 | 0.00 |
| **Tool Errors (BFCL)** | 183 | 0.92 |
| **Tool Calls** | 845 | 4.2 (Total) / 1.2 (Per Turn) |
| **Task Horizon (Length)** | - | 3.65 Turns |
| **Redundant Tool Calls** | 640 | 3.20 |
| **Self-Correct (Runtime)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Self-Correct (Tool)** | 2 (out of 101 err traces) | 2.0% (Recovery Rate) |
| **Context Growth** | - | 1540 (Total) / 687 (Turn) / 225 (Step) |

## 2. Averages by Outcome (Success vs. Failure)
| Metric | Successes | Failures |
|---|---|---|
| **Input Tokens (Test/Turn/Step)** | 81231.2 / 22337.2 / 9869.7 | 86981.8 / 24024.8 / 11026.5 |
| **Output Tokens (Test/Turn/Step)** | 955.3 / 280.2 / 124.9 | 1086.5 / 316.7 / 143.2 |
| **Thinking Tokens (Test/Turn/Step)** | 0.0  / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 |
| **Turns** | 3.7 | 3.6 |
| **Steps** | 8.2 | 7.8 |
| **LLM Latency (Total)** | 64.47s | 41.25s |
| **LLM Latency (Per Turn)** | 17.01s | 10.36s |
| **LLM Latency (Per Step)** | 7.65s | 4.78s |
| **Context Growth (Total)** | 1494.7 | 1554.9 |
| **Context Growth (Per Turn)**| 620.2 | 710.5 |
| **Context Growth (Per Step)**| 227.3 | 224.8 |

## 3. Breakdown by Category

### Category Totals
| Category | Tests | Successes | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | LLM Latency | Runtime Errors | Tool Errors | Redundant Calls | Self-Corrects (Runtime) | Self-Corrects (Tool) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| multi_turn_base | 200 | 51 | 17103084 | 210614 | 0 | 731 | 1575 | 9433.83s | 0 | 183 | 640 | 0 | 2 |

### Category Averages
| Category | Success Rate | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | Latency (Total/Turn/Step) | Context Growth (Total/Turn/Step) | Runtime Errors | Tool Errors | Redundant | Runtime Recovery % | Tool Recovery % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| multi_turn_base | 25.5% | 85515.4 | 1053.1 | 0.0 | 3.7 | 7.9 | 47.17s / 12.06s / 5.51s | 1539.6 / 687.5 / 225.4 | 0.00 | 0.92 | 3.20 | 0.0% | 2.0% |
