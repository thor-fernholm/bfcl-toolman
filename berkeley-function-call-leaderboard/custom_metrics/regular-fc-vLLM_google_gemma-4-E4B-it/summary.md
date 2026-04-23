# Benchmark Metrics: `regular-fc | vLLM/google/gemma-4-E4B-it`

## 1. Global Totals & Averages
| Metric | Total (Sum) | Average (Mean per test) |
|---|---|---|
| **Tests Run** | 200 | - |
| **Successes** | 65 | 32.50% (Success Rate) |
| **Input Tokens** | 43247204 | 216236.0 |
| **Output Tokens** | 115654 | 578.3 |
| **Thinking Tokens** | 0 | 0.0 |
| **Turns** | 734 | 3.7 |
| **Steps** | 1805 | 9.0 |
| **LLM Latency (sec)** | 131019.92s | 655.10s (Total) / 189.11s (Per Turn) / 74.65s (Per Step) |
| **Runtime Errors (Goja)** | 0 | 0.00 |
| **Tool Errors (BFCL)** | 0 | 0.00 |
| **Tool Calls** | 1146 | 5.7 (Total) / 1.7 (Per Turn) |
| **Task Horizon (Length)** | - | 3.67 Turns |
| **Redundant Tool Calls** | 137 | 0.69 |
| **Self-Correct (Runtime)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Self-Correct (Tool)** | 0 (out of 0 err traces) | 0.0% (Recovery Rate) |
| **Context Growth** | - | 1244 (Total) / 585 (Turn) / 144 (Step) |

## 2. Averages by Outcome (Success vs. Failure)
| Metric | Successes | Failures |
|---|---|---|
| **Input Tokens (Test/Turn/Step)** | 210298.4 / 65440.9 / 22820.5 | 219094.9 / 59875.0 / 24409.1 |
| **Output Tokens (Test/Turn/Step)** | 472.8 / 147.2 / 52.6 | 629.0 / 175.3 / 73.6 |
| **Thinking Tokens (Test/Turn/Step)** | 0.0  / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 |
| **Turns** | 3.5 | 3.7 |
| **Steps** | 9.4 | 8.9 |
| **LLM Latency (Total)** | 669.18s | 648.32s |
| **LLM Latency (Per Turn)** | 203.24s | 182.31s |
| **LLM Latency (Per Step)** | 73.61s | 75.16s |
| **Context Growth (Total)** | 1132.0 | 1298.2 |
| **Context Growth (Per Turn)**| 517.0 | 617.7 |
| **Context Growth (Per Step)**| 139.1 | 147.1 |

## 3. Breakdown by Category

### Category Totals
| Category | Tests | Successes | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | LLM Latency | Runtime Errors | Tool Errors | Redundant Calls | Self-Corrects (Runtime) | Self-Corrects (Tool) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| multi_turn_base | 200 | 65 | 43247204 | 115654 | 0 | 734 | 1805 | 131019.92s | 0 | 0 | 137 | 0 | 0 |

### Category Averages
| Category | Success Rate | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | Latency (Total/Turn/Step) | Context Growth (Total/Turn/Step) | Runtime Errors | Tool Errors | Redundant | Runtime Recovery % | Tool Recovery % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| multi_turn_base | 32.5% | 216236.0 | 578.3 | 0.0 | 3.7 | 9.0 | 655.10s / 189.11s / 74.65s | 1244.2 / 585.0 / 144.5 | 0.00 | 0.00 | 0.69 | 0.0% | 0.0% |
