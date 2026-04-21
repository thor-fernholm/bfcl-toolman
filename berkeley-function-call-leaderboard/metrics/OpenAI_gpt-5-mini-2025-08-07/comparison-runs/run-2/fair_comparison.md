# Fair Metric Comparison: `regular-fc` vs `ptc-fc`
**Model:** `OpenAI/gpt-5-mini-2025-08-07`

> This report compares metrics ONLY on the exact same tasks where both setups achieved the same outcome (both succeeded or both failed).

## 1. Tasks Where BOTH Succeeded (Based on 1819 exact matching tasks)
| Metric (Average per task) | `regular-fc` | `ptc-fc` | Difference | % Change |
|---|---|---|---|---|
| **Total Input Tokens** | 19271.46 | 8490.24 | -10781.22 | -55.94% |
| **Total Output Tokens** | 112.34 | 175.52 | +63.17 | +56.23% |
| **Total Thinking Tokens** | 635.32 | 1037.58 | +402.26 | +63.32% |
| **Total Cost $** | 0.00631 | 0.00455 | -0.00176 | -27.94839% |
| **Task Horizon (Turns)** | 1.36 | 1.36 | 0.00 | 0.00% |
| **Steps** | 4.23 | 2.14 | -2.09 | -49.48% |
| **LLM Latency (sec)** | 10.33 | 16.91 | +6.58 | +63.65% |
| **Context Growth (Total)** | 1640.38 | 1413.14 | -227.24 | -13.85% |
| **Tool Calls (Total)** | 2.05 | 1.59 | -0.45 | -22.17% |
| **Redundant Tool Calls** | 0.50 | 0.63 | +0.13 | +25.08% |
| **Runtime Errors** | 0.00 | 0.00 | 0.00 | 0.00% |
| **Tool Errors** | 0.00 | 0.06 | +0.06 | 0.00% |

## 2. Tasks Where BOTH Failed (Based on 995 exact matching tasks)
| Metric (Average per task) | `regular-fc` | `ptc-fc` | Difference | % Change |
|---|---|---|---|---|
| **Total Input Tokens** | 82794.27 | 24417.28 | -58376.99 | -70.51% |
| **Total Output Tokens** | 330.51 | 462.00 | +131.49 | +39.78% |
| **Total Thinking Tokens** | 2253.70 | 2928.56 | +674.86 | +29.94% |
| **Total Cost $** | 0.02587 | 0.01289 | -0.01298 | -50.18574% |
| **Task Horizon (Turns)** | 1.89 | 2.00 | +0.11 | +5.57% |
| **Steps** | 15.99 | 4.55 | -11.44 | -71.55% |
| **LLM Latency (sec)** | 34.53 | 40.17 | +5.64 | +16.33% |
| **Context Growth (Total)** | 3253.63 | 1785.80 | -1467.83 | -45.11% |
| **Tool Calls (Total)** | 6.61 | 3.20 | -3.41 | -51.58% |
| **Redundant Tool Calls** | 3.55 | 2.23 | -1.33 | -37.31% |
| **Runtime Errors** | 0.00 | 0.00 | 0.00 | 0.00% |
| **Tool Errors** | 0.00 | 0.44 | +0.44 | 0.00% |

