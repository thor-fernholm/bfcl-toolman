# Fair Metric Comparison: `regular-fc` vs `ptc-fc`
**Model:** `vLLM/google/gemma-4-E4B-it`

> This report compares metrics ONLY on the exact same tasks where both setups achieved the same outcome (both succeeded or both failed).

## 1. Tasks Where BOTH Succeeded (Based on 2082 exact matching tasks)
| Metric (Average per task) | `regular-fc` | `ptc-fc` | Difference | % Change |
|---|---|---|---|---|
| **Total Input Tokens** | 7539.72 | 4217.92 | -3321.80 | -44.06% |
| **Total Output Tokens** | 58.03 | 78.63 | +20.60 | +35.49% |
| **Total Thinking Tokens** | 0.00 | 0.00 | 0.00 | 0.00% |
| **Total Cost $** | 0.00000 | 0.00000 | 0.00000 | 0.00000% |
| **Task Horizon (Turns)** | 1.15 | 1.15 | 0.00 | 0.00% |
| **Steps** | 1.43 | 1.45 | +0.01 | +0.94% |
| **LLM Latency (sec)** | 21.97 | 13.66 | -8.30 | -37.80% |
| **Context Growth (Total)** | 1738.03 | 1419.30 | -318.73 | -18.34% |
| **Tool Calls (Total)** | 0.84 | 0.84 | -0.00 | -0.23% |
| **Redundant Tool Calls** | 0.02 | 0.17 | +0.15 | +802.56% |
| **Runtime Errors** | 0.00 | 0.00 | 0.00 | 0.00% |
| **Tool Errors** | 0.00 | 0.01 | +0.01 | 0.00% |

## 2. Tasks Where BOTH Failed (Based on 1053 exact matching tasks)
| Metric (Average per task) | `regular-fc` | `ptc-fc` | Difference | % Change |
|---|---|---|---|---|
| **Total Input Tokens** | 68009.12 | 27972.13 | -40036.99 | -58.87% |
| **Total Output Tokens** | 249.51 | 380.99 | +131.48 | +52.69% |
| **Total Thinking Tokens** | 0.00 | 0.00 | 0.00 | 0.00% |
| **Total Cost $** | 0.00000 | 0.00000 | 0.00000 | 0.00000% |
| **Task Horizon (Turns)** | 2.77 | 2.75 | -0.02 | -0.62% |
| **Steps** | 5.75 | 5.11 | -0.64 | -11.10% |
| **LLM Latency (sec)** | 135.68 | 127.39 | -8.29 | -6.11% |
| **Context Growth (Total)** | 1889.33 | 1487.78 | -401.55 | -21.25% |
| **Tool Calls (Total)** | 3.57 | 2.77 | -0.80 | -22.31% |
| **Redundant Tool Calls** | 0.47 | 1.75 | +1.28 | +275.36% |
| **Runtime Errors** | 0.00 | 0.00 | 0.00 | 0.00% |
| **Tool Errors** | 0.00 | 0.61 | +0.61 | 0.00% |

