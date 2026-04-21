# Fair Metric Comparison: `regular-fc` vs `ptc-fc`
**Model:** `OpenAI/gpt-5-mini-2025-08-07`

> This report compares metrics ONLY on the exact same tasks where both setups achieved the same outcome (both succeeded or both failed).

## 1. Tasks Where BOTH Succeeded (Based on 1822 exact matching tasks)
| Metric (Average per task) | `regular-fc` | `ptc-fc` | Difference | % Change |
|---|---|---|---|---|
| **Total Input Tokens** | 27243.74 | 10683.47 | -16560.27 | -60.79% |
| **Total Output Tokens** | 115.34 | 186.90 | +71.57 | +62.05% |
| **Total Thinking Tokens** | 650.22 | 1081.61 | +431.39 | +66.34% |
| **Total Cost $** | 0.00834 | 0.00521 | -0.00313 | -37.57068% |
| **Task Horizon (Turns)** | 1.37 | 1.37 | 0.00 | 0.00% |
| **Steps** | 3.07 | 2.21 | -0.85 | -27.85% |
| **LLM Latency (sec)** | 14.38 | 17.63 | +3.25 | +22.58% |
| **Context Growth (Total)** | 2261.75 | 1599.07 | -662.69 | -29.30% |
| **Tool Calls (Total)** | 2.14 | 1.65 | -0.49 | -22.86% |
| **Redundant Tool Calls** | 0.55 | 0.68 | +0.12 | +22.24% |
| **Runtime Errors** | 0.00 | 0.00 | 0.00 | 0.00% |
| **Tool Errors** | 0.00 | 0.07 | +0.07 | 0.00% |

## 2. Tasks Where BOTH Failed (Based on 1001 exact matching tasks)
| Metric (Average per task) | `regular-fc` | `ptc-fc` | Difference | % Change |
|---|---|---|---|---|
| **Total Input Tokens** | 83430.10 | 31721.57 | -51708.53 | -61.98% |
| **Total Output Tokens** | 342.94 | 510.03 | +167.09 | +48.72% |
| **Total Thinking Tokens** | 2148.12 | 2864.59 | +716.47 | +33.35% |
| **Total Cost $** | 0.02584 | 0.01468 | -0.01116 | -43.18952% |
| **Task Horizon (Turns)** | 1.89 | 1.99 | +0.10 | +5.34% |
| **Steps** | 8.35 | 4.61 | -3.74 | -44.82% |
| **LLM Latency (sec)** | 40.87 | 41.07 | +0.20 | +0.49% |
| **Context Growth (Total)** | 3391.68 | 2365.40 | -1026.27 | -30.26% |
| **Tool Calls (Total)** | 6.67 | 3.26 | -3.41 | -51.13% |
| **Redundant Tool Calls** | 3.60 | 2.28 | -1.32 | -36.71% |
| **Runtime Errors** | 0.00 | 0.00 | 0.00 | 0.00% |
| **Tool Errors** | 0.00 | 0.42 | +0.42 | 0.00% |

