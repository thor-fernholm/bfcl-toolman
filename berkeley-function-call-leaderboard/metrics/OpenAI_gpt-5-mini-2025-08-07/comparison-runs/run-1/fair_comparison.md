# Fair Metric Comparison: `regular-fc` vs `ptc-fc`
**Model:** `OpenAI/gpt-5-mini-2025-08-07`

> This report compares metrics ONLY on the exact same tasks where both setups achieved the same outcome (both succeeded or both failed).

## 1. Tasks Where BOTH Succeeded (Based on 1833 exact matching tasks)
| Metric (Average per task) | `regular-fc` | `ptc-fc` | Difference | % Change |
|---|---|---|---|---|
| **Total Input Tokens** | 25309.91 | 10727.38 | -14582.53 | -57.62% |
| **Total Output Tokens** | 125.37 | 188.20 | +62.83 | +50.12% |
| **Total Thinking Tokens** | 637.42 | 1102.45 | +465.04 | +72.96% |
| **Total Cost $** | 0.0079 | 0.0053 | -0.0026 | -32.9794% |
| **Task Horizon (Turns)** | 1.37 | 1.37 | 0.00 | 0.00% |
| **Steps** | 3.46 | 2.23 | -1.22 | -35.40% |
| **LLM Latency (sec)** | 13.13 | 27.58 | +14.44 | +109.97% |
| **Context Growth (Total)** | 2184.32 | 1501.42 | -682.89 | -31.26% |
| **Tool Calls (Total)** | 2.11 | 1.68 | -0.43 | -20.39% |
| **Redundant Tool Calls** | 0.52 | 0.70 | +0.18 | +34.78% |
| **Runtime Errors** | 0.00 | 0.00 | 0.00 | 0.00% |
| **Tool Errors** | 0.00 | 0.08 | +0.08 | 0.00% |

## 2. Tasks Where BOTH Failed (Based on 1013 exact matching tasks)
| Metric (Average per task) | `regular-fc` | `ptc-fc` | Difference | % Change |
|---|---|---|---|---|
| **Total Input Tokens** | 79938.02 | 27915.33 | -52022.69 | -65.08% |
| **Total Output Tokens** | 303.73 | 439.40 | +135.68 | +44.67% |
| **Total Thinking Tokens** | 1908.31 | 2722.62 | +814.31 | +42.67% |
| **Total Cost $** | 0.0244 | 0.0133 | -0.0111 | -45.4992% |
| **Task Horizon (Turns)** | 1.96 | 2.00 | +0.04 | +1.96% |
| **Steps** | 10.82 | 4.47 | -6.35 | -58.66% |
| **LLM Latency (sec)** | 38.91 | 60.99 | +22.07 | +56.72% |
| **Context Growth (Total)** | 3202.21 | 2162.96 | -1039.25 | -32.45% |
| **Tool Calls (Total)** | 5.78 | 3.12 | -2.67 | -46.10% |
| **Redundant Tool Calls** | 2.72 | 2.14 | -0.58 | -21.36% |
| **Runtime Errors** | 0.00 | 0.00 | 0.00 | 0.00% |
| **Tool Errors** | 0.00 | 0.42 | +0.42 | 0.00% |

