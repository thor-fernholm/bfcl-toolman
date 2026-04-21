# Aggregated Fair Metric Comparison: `regular-fc` vs `ptc-fc`
**Model:** `OpenAI/gpt-5-mini-2025-08-07` (Over 3 runs)

> This report compares metrics ONLY on the exact same tasks where both setups achieved the same outcome (both succeeded or both failed).

## 1. Tasks Where BOTH Succeeded (Based on 1825 ± 7 exact matching tasks)
| Metric (Average per task) | `regular-fc` | `ptc-fc` | Difference | % Change |
|---|---|---|---|---|
| **Total Input Tokens** | 23941.70 ± 4158.52 | 9967.03 ± 1279.13 | -13974.67 ± 2937.09 | -58.12% ± 2.46% |
| **Total Output Tokens** | 117.68 ± 6.82 | 183.54 ± 6.98 | +65.86 ± 4.95 | +56.13% ± 5.97% |
| **Total Thinking Tokens** | 640.99 ± 8.07 | 1073.88 ± 33.12 | +432.89 ± 31.42 | +67.54% ± 4.93% |
| **Total Cost $** | 0.00750 ± 0.00106 | 0.00501 ± 0.00040 | -0.00250 ± 0.00069 | -32.83282% ± 4.81282% |
| **Task Horizon (Turns)** | 1.37 ± 0.01 | 1.37 ± 0.01 | 0.00 ± 0.00 | 0.00% ± 0.00% |
| **Steps** | 3.59 ± 0.59 | 2.20 ± 0.05 | -1.39 ± 0.64 | -37.58% ± 10.98% |
| **LLM Latency (sec)** | 12.62 ± 2.07 | 20.70 ± 5.96 | +8.09 ± 5.75 | +65.40% ± 43.72% |
| **Context Growth (Total)** | 2028.82 ± 338.62 | 1504.54 ± 93.00 | -524.27 ± 257.44 | -24.81% ± 9.54% |
| **Tool Calls (Total)** | 2.10 ± 0.05 | 1.64 ± 0.04 | -0.46 ± 0.03 | -21.81% ± 1.27% |
| **Redundant Tool Calls** | 0.52 ± 0.03 | 0.67 ± 0.04 | +0.14 ± 0.03 | +27.37% ± 6.57% |
| **Runtime Errors** | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00% ± 0.00% |
| **Tool Errors** | 0.00 ± 0.00 | 0.07 ± 0.01 | +0.07 ± 0.01 | 0.00% ± 0.00% |

## 2. Tasks Where BOTH Failed (Based on 1003 ± 9 exact matching tasks)
| Metric (Average per task) | `regular-fc` | `ptc-fc` | Difference | % Change |
|---|---|---|---|---|
| **Total Input Tokens** | 82054.13 ± 1859.97 | 28018.06 ± 3653.23 | -54036.07 ± 3762.62 | -65.86% ± 4.32% |
| **Total Output Tokens** | 325.73 ± 20.04 | 470.48 ± 36.07 | +144.75 ± 19.46 | +44.39% ± 4.47% |
| **Total Thinking Tokens** | 2103.38 ± 176.99 | 2838.59 ± 105.40 | +735.21 ± 71.59 | +35.32% ± 6.59% |
| **Total Cost $** | 0.02537 ± 0.00083 | 0.01362 ± 0.00094 | -0.01175 ± 0.00107 | -46.29148% ± 3.56477% |
| **Task Horizon (Turns)** | 1.92 ± 0.04 | 2.00 ± 0.01 | +0.08 ± 0.04 | +4.29% ± 2.02% |
| **Steps** | 11.72 ± 3.90 | 4.54 ± 0.07 | -7.18 ± 3.92 | -58.34% ± 13.37% |
| **LLM Latency (sec)** | 38.11 ± 3.25 | 47.41 ± 11.77 | +9.30 ± 11.39 | +24.51% ± 28.99% |
| **Context Growth (Total)** | 3282.51 ± 97.98 | 2104.72 ± 294.16 | -1177.78 ± 251.27 | -35.94% ± 8.02% |
| **Tool Calls (Total)** | 6.36 ± 0.50 | 3.19 ± 0.07 | -3.16 ± 0.43 | -49.60% ± 3.04% |
| **Redundant Tool Calls** | 3.29 ± 0.50 | 2.22 ± 0.07 | -1.08 ± 0.43 | -31.79% ± 9.04% |
| **Runtime Errors** | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00% ± 0.00% |
| **Tool Errors** | 0.00 ± 0.00 | 0.43 ± 0.01 | +0.43 ± 0.01 | 0.00% ± 0.00% |

