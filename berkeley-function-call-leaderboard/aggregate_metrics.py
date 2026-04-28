import os
import numpy as np
import pandas as pd
from pathlib import Path

def get_model_cost(model_name):
    match model_name:
        case "OpenAI/gpt-5-mini-2025-08-07":
            return (0.25 * 1e-06, 2.0 * 1e-06, 2.0 * 1e-06)
        case _:
            return None

def m_s(values, dec=1, suffix=""):
    """Helper to format lists of values into 'Mean ± StdDev' strings safely."""
    # filter out NaNs or Nones if a metric didn't exist in a specific run
    v = [x for x in values if x is not None and not pd.isna(x)]
    if not v:
        return f"0.0{suffix} ± 0.0{suffix}"

    mean = np.mean(v)
    std = np.std(v, ddof=1) if len(v) > 1 else 0.0
    return f"{mean:.{dec}f}{suffix} ± {std:.{dec}f}{suffix}"

def m_s_diff(values, dec=1, suffix=""):
    """Same as m_s, but prepends a '+' sign for positive means (used in comparison differences)."""
    v = [x for x in values if x is not None and not pd.isna(x)]
    if not v:
        return f"0.0{suffix} ± 0.0{suffix}"

    mean = np.mean(v)
    std = np.std(v, ddof=1) if len(v) > 1 else 0.0
    sign = "+" if mean > 0 else ""
    return f"{sign}{mean:.{dec}f}{suffix} ± {std:.{dec}f}{suffix}"

def generate_aggregated_report(model_t, setup_t, dfs):
    """Aggregates metrics for a single setup (e.g., ptc-fc) across multiple runs."""
    safe_model_tag = model_t.replace("/", "_").replace("\\", "_")
    safe_setup_tag = setup_t.replace("/", "_").replace("\\", "_")

    # create the output directory for the aggregated data
    output_dir = Path(f"metrics/{safe_model_tag}/{safe_setup_tag}_aggregated")
    output_dir.mkdir(parents=True, exist_ok=True)

    md_path = output_dir / "summary_aggregated.md"
    raw_csv_path = output_dir / "metrics_data_aggregated.csv"

    # save a concatenated version of the raw data with a 'run_id' tracking column
    for i, df in enumerate(dfs, 1):
        df['run_id'] = i
    pd.concat(dfs).to_csv(raw_csv_path, index=False)

    md = f"# Aggregated Benchmark Metrics: `{setup_t} | {model_t}` (Over {len(dfs)} runs)\n\n"

    # quick lambdas to grab the Sum or Mean of a column across all DataFrames
    sm = lambda col: [df[col].sum() if not df.empty else 0 for df in dfs]
    mn = lambda col: [df[col].mean() if not df.empty else 0 for df in dfs]

    n_tests = [len(df) for df in dfs]
    successes = sm('success')
    success_rates = [(s / t * 100) if t else 0 for s, t in zip(successes, n_tests)]
    errs = sm('error')
    err_rates = [(e / t * 100) if t else 0 for e, t in zip(errs, n_tests)]

    # dynamic Self-Correction Rates
    rt_err_traces = [len(df[df['runtime_error_count'] > 0]) for df in dfs]
    sc_rt = sm('self_corrected_runtime')
    sc_rt_rate = [(s / e * 100) if e else 0 for s, e in zip(sc_rt, rt_err_traces)]

    tl_err_traces = [len(df[df['tool_error_count'] > 0]) for df in dfs]
    sc_tl = sm('self_corrected_tool')
    sc_tl_rate = [(s / e * 100) if e else 0 for s, e in zip(sc_tl, tl_err_traces)]

    # --- GLOBAL TOTALS & AVERAGES ---
    md += "## 1. Global Totals & Averages\n"
    md += "| Metric | Total (Sum) | Average (Mean per test) |\n"
    md += "|---|---|---|\n"
    md += f"| **Tests Run** | {m_s(n_tests, 0)} | - |\n"
    md += f"| **Successes** | {m_s(successes, 0)} | {m_s(success_rates, 2, '%')} (Success Rate) |\n"
    md += f"| **Input Tokens** | {m_s(sm('total_input_tokens'), 0)} | {m_s(mn('total_input_tokens'), 1)} |\n"
    md += f"| **Output Tokens** | {m_s(sm('total_output_tokens'), 0)} | {m_s(mn('total_output_tokens'), 1)} |\n"
    md += f"| **Thinking Tokens** | {m_s(sm('total_thinking_tokens'), 0)} | {m_s(mn('total_thinking_tokens'), 1)} |\n"
    md += f"| **Cost $** | {m_s(sm('total_cost'), 4)} | {m_s(mn('total_cost'), 5)} |\n"
    md += f"| **Turns** | {m_s(sm('turn_count'), 0)} | {m_s(mn('turn_count'), 1)} |\n"
    md += f"| **Steps** | {m_s(sm('step_count'), 0)} | {m_s(mn('step_count'), 1)} |\n"
    md += f"| **LLM Latency (sec)** | {m_s(sm('total_llm_latency_sec'), 2, 's')} | {m_s(mn('total_llm_latency_sec'), 2, 's')} (Total) / {m_s(mn('avg_llm_latency_per_turn_sec'), 2, 's')} (Per Turn) / {m_s(mn('avg_llm_latency_per_step_sec'), 2, 's')} (Per Step) |\n"
    md += f"| **Errors (Total)** | {m_s(errs, 0)} | {m_s(err_rates, 2, '%')} |\n"
    md += f"| **Runtime Errors (Goja)** | {m_s(sm('runtime_error_count'), 0)} | {m_s(mn('runtime_error_count'), 2)} |\n"
    md += f"| **Tool Errors (BFCL)** | {m_s(sm('tool_error_count'), 0)} | {m_s(mn('tool_error_count'), 2)} |\n"
    md += f"| **Tool Calls** | {m_s(sm('tool_call_count'), 0)} | {m_s(mn('tool_call_count'), 1)} (Total) / {m_s(mn('avg_tool_calls_per_turn'), 1)} (Per Turn) |\n"
    md += f"| **Task Horizon (Length)** | - | {m_s(mn('turn_count'), 2)} Turns |\n"
    md += f"| **Redundant Tool Calls** | {m_s(sm('redundant_tool_calls'), 0)} | {m_s(mn('redundant_tool_calls'), 2)} |\n"
    md += f"| **Self-Correct (Runtime)** | {m_s(sc_rt, 0)} | {m_s(sc_rt_rate, 1, '%')} (Recovery Rate) |\n"
    md += f"| **Self-Correct (Tool)** | {m_s(sc_tl, 0)} | {m_s(sc_tl_rate, 1, '%')} (Recovery Rate) |\n"
    md += f"| **Context Growth** | - | {m_s(mn('context_growth_total'), 0)} (Total) / {m_s(mn('avg_context_growth_per_turn'), 0)} (Turn) / {m_s(mn('avg_context_growth_per_step'), 0)} (Step) |\n\n"

    # --- SPLIT BY SUCCESS/FAIL ---
    md += "## 2. Averages by Outcome (Success vs. Failure)\n"
    md += "| Metric | Successes | Failures |\n"
    md += "|---|---|---|\n"

    dfs_succ = [df[df['success'] == 1] for df in dfs]
    dfs_fail = [df[df['success'] == 0] for df in dfs]
    s_mn = lambda col: [d[col].mean() if not d.empty else np.nan for d in dfs_succ]
    f_mn = lambda col: [d[col].mean() if not d.empty else np.nan for d in dfs_fail]

    md += f"| **Input Tokens (Test/Turn/Step)** | {m_s(s_mn('total_input_tokens'),1)} / {m_s(s_mn('avg_input_tokens_per_turn'),1)} / {m_s(s_mn('avg_input_tokens_per_step'),1)} | {m_s(f_mn('total_input_tokens'),1)} / {m_s(f_mn('avg_input_tokens_per_turn'),1)} / {m_s(f_mn('avg_input_tokens_per_step'),1)} |\n"
    md += f"| **Output Tokens (Test/Turn/Step)** | {m_s(s_mn('total_output_tokens'),1)} / {m_s(s_mn('avg_output_tokens_per_turn'),1)} / {m_s(s_mn('avg_output_tokens_per_step'),1)} | {m_s(f_mn('total_output_tokens'),1)} / {m_s(f_mn('avg_output_tokens_per_turn'),1)} / {m_s(f_mn('avg_output_tokens_per_step'),1)} |\n"
    md += f"| **Thinking Tokens (Test/Turn/Step)** | {m_s(s_mn('total_thinking_tokens'),1)} / {m_s(s_mn('avg_thinking_tokens_per_turn'),1)} / {m_s(s_mn('avg_thinking_tokens_per_step'),1)} | {m_s(f_mn('total_thinking_tokens'),1)} / {m_s(f_mn('avg_thinking_tokens_per_turn'),1)} / {m_s(f_mn('avg_thinking_tokens_per_step'),1)} |\n"
    md += f"| **Turns** | {m_s(s_mn('turn_count'),1)} | {m_s(f_mn('turn_count'),1)} |\n"
    md += f"| **Steps** | {m_s(s_mn('step_count'),1)} | {m_s(f_mn('step_count'),1)} |\n"
    md += f"| **LLM Latency (Total)** | {m_s(s_mn('total_llm_latency_sec'),2,'s')} | {m_s(f_mn('total_llm_latency_sec'),2,'s')} |\n"
    md += f"| **LLM Latency (Per Turn)** | {m_s(s_mn('avg_llm_latency_per_turn_sec'),2,'s')} | {m_s(f_mn('avg_llm_latency_per_turn_sec'),2,'s')} |\n"
    md += f"| **LLM Latency (Per Step)** | {m_s(s_mn('avg_llm_latency_per_step_sec'),2,'s')} | {m_s(f_mn('avg_llm_latency_per_step_sec'),2,'s')} |\n"
    md += f"| **Context Growth (Total)** | {m_s(s_mn('context_growth_total'),1)} | {m_s(f_mn('context_growth_total'),1)} |\n"
    md += f"| **Context Growth (Per Turn)**| {m_s(s_mn('avg_context_growth_per_turn'),1)} | {m_s(f_mn('avg_context_growth_per_turn'),1)} |\n"
    md += f"| **Context Growth (Per Step)**| {m_s(s_mn('avg_context_growth_per_step'),1)} | {m_s(f_mn('avg_context_growth_per_step'),1)} |\n\n"

    # --- BREAKDOWN BY META-CATEGORY (WEIGHTED) ---
    md += "## 3. Breakdown by Meta-Category\n\n"

    meta_cats = get_categories()

    md += "### Meta-Category Totals (Unweighted Sums)\n"
    md += "| Meta-Category | Tests | Successes | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | LLM Latency | Runtime Errors | Tool Errors | Redundant Calls | Self-Corrects (Runtime) | Self-Corrects (Tool) |\n"
    md += "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"

    meta_cat_avgs_str = ""
    # run_meta_successes = [[] for _ in range(len(dfs))]
    # Custom 3:2:1 Meta-Category Weights
    META_WEIGHTS = {"multi_turn": 3.0, "single_turn": 2.0, "irrelevance": 1.0}
    run_meta_weighted_sums = [0.0] * len(dfs)
    run_meta_weight_totals = [0.0] * len(dfs)

    for m_cat, subcats in meta_cats.items():
        # Calculate Raw Totals (Sums are never weighted)
        mc_dfs = [df[df['category'].isin(subcats)] for df in dfs]
        mc_sm = lambda col: [d[col].sum() if not d.empty else 0 for d in mc_dfs]
        mc_n = [len(d) for d in mc_dfs]
        mc_succ = mc_sm('success')

        md += f"| {m_cat} | {m_s(mc_n,0)} | {m_s(mc_succ,0)} | {m_s(mc_sm('total_input_tokens'),0)} | {m_s(mc_sm('total_output_tokens'),0)} | {m_s(mc_sm('total_thinking_tokens'),0)} | {m_s(mc_sm('turn_count'),0)} | {m_s(mc_sm('step_count'),0)} | {m_s(mc_sm('total_llm_latency_sec'),2,'s')} | {m_s(mc_sm('runtime_error_count'),0)} | {m_s(mc_sm('tool_error_count'),0)} | {m_s(mc_sm('redundant_tool_calls'),0)} | {m_s(mc_sm('self_corrected_runtime'),0)} | {m_s(mc_sm('self_corrected_tool'),0)} |\n"

        # Calculate Weighted Averages per run
        def mc_w_mn(col, is_ratio=False, den_col=None):
            run_vals = []
            for df in dfs:
                num = 0.0
                den = 0.0
                for cat in subcats:
                    cat_df = df[df['category'] == cat]
                    if not cat_df.empty:
                        w = CATEGORY_WEIGHTS.get(cat, 1.0)
                        if is_ratio:
                            # For recovery rates: sum(sc)/sum(err) per category, then weight it
                            cat_den = cat_df[den_col].apply(lambda x: 1 if x > 0 else 0).sum()
                            cat_num = cat_df[col].sum()
                            val = (cat_num / cat_den) if cat_den > 0 else 0.0
                        else:
                            val = cat_df[col].mean()

                        num += val * w
                        den += w
                run_vals.append(num / den if den > 0 else np.nan)
            return run_vals

        mc_succ_rate = [v * 100 for v in mc_w_mn('success')]

        # for i, rate in enumerate(mc_succ_rate):
        #     if not pd.isna(rate):
        #         run_meta_successes[i].append(rate)
        m_weight = META_WEIGHTS.get(m_cat, 1.0)
        for i, rate in enumerate(mc_succ_rate):
            if not pd.isna(rate):
                run_meta_weighted_sums[i] += rate * m_weight
                run_meta_weight_totals[i] += m_weight

        c_lat = f"{m_s(mc_w_mn('total_llm_latency_sec'),2,'s')} / {m_s(mc_w_mn('avg_llm_latency_per_turn_sec'),2,'s')} / {m_s(mc_w_mn('avg_llm_latency_per_step_sec'),2,'s')}"
        c_ctx = f"{m_s(mc_w_mn('context_growth_total'),1)} / {m_s(mc_w_mn('avg_context_growth_per_turn'),1)} / {m_s(mc_w_mn('avg_context_growth_per_step'),1)}"

        c_sc_rt_rate = [v * 100 for v in mc_w_mn('self_corrected_runtime', True, 'runtime_error_count')]
        c_sc_tl_rate = [v * 100 for v in mc_w_mn('self_corrected_tool', True, 'tool_error_count')]

        meta_cat_avgs_str += f"| {m_cat} | {m_s(mc_succ_rate,2,'%')} | {m_s(mc_w_mn('total_input_tokens'),1)} | {m_s(mc_w_mn('total_output_tokens'),1)} | {m_s(mc_w_mn('total_thinking_tokens'),1)} | {m_s(mc_w_mn('turn_count'),1)} | {m_s(mc_w_mn('step_count'),1)} | {c_lat} | {c_ctx} | {m_s(mc_w_mn('runtime_error_count'),2)} | {m_s(mc_w_mn('tool_error_count'),2)} | {m_s(mc_w_mn('redundant_tool_calls'),2)} | {m_s(c_sc_rt_rate,1,'%')} | {m_s(c_sc_tl_rate,1,'%')} |\n"

    md += "\n### Meta-Category Averages (Weighted)\n"
    md += "| Meta-Category | Success Rate | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | Latency (Total/Turn/Step) | Context Growth (Total/Turn/Step) | Runtime Errors | Tool Errors | Redundant | Runtime Recovery % | Tool Recovery % |\n"
    md += "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
    md += meta_cat_avgs_str + "\n\n"

    # Calculate the unweighted average of the meta-categories
    # cat_acc_per_run = [np.mean(vals) if vals else np.nan for vals in run_meta_successes]
    # md += f"**Category Accuracy (Unweighted Average of the {len(meta_cats)} Meta-Categories):** {m_s(cat_acc_per_run, 2, '%')}\n\n"
    # Calculate the custom weighted average (3:2:1) of the meta-categories
    cat_acc_per_run = [
        (s / w) if w > 0 else np.nan
        for s, w in zip(run_meta_weighted_sums, run_meta_weight_totals)
    ]
    md += f"**Category Accuracy (Weighted 3:2:1 for Multi:Single:Irrelevance):** {m_s(cat_acc_per_run, 2, '%')}\n\n"

    # --- BREAKDOWN BY CATEGORY ---
    md += "## 4. Breakdown by Category\n\n"
    all_cats = pd.concat(dfs)['category'].unique()

    md += "### Category Totals\n"
    md += "| Category | Tests | Successes | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | LLM Latency | Runtime Errors | Tool Errors | Redundant Calls | Self-Corrects (Runtime) | Self-Corrects (Tool) |\n"
    md += "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"

    cat_avgs_str = ""

    for cat in sorted(all_cats):
        c_dfs = [df[df['category'] == cat] for df in dfs]
        c_sm = lambda col: [d[col].sum() if not d.empty else 0 for d in c_dfs]
        c_mn = lambda col: [d[col].mean() if not d.empty else np.nan for d in c_dfs]
        c_n = [len(d) for d in c_dfs]
        c_succ = c_sm('success')
        c_succ_rate = [(s/t*100) if t else 0.0 for s, t in zip(c_succ, c_n)]

        md += f"| {cat} | {m_s(c_n,0)} | {m_s(c_succ,0)} | {m_s(c_sm('total_input_tokens'),0)} | {m_s(c_sm('total_output_tokens'),0)} | {m_s(c_sm('total_thinking_tokens'),0)} | {m_s(c_sm('turn_count'),0)} | {m_s(c_sm('step_count'),0)} | {m_s(c_sm('total_llm_latency_sec'),2,'s')} | {m_s(c_sm('runtime_error_count'),0)} | {m_s(c_sm('tool_error_count'),0)} | {m_s(c_sm('redundant_tool_calls'),0)} | {m_s(c_sm('self_corrected_runtime'),0)} | {m_s(c_sm('self_corrected_tool'),0)} |\n"

        c_rt_errs = [len(d[d['runtime_error_count']>0]) for d in c_dfs]
        c_tl_errs = [len(d[d['tool_error_count']>0]) for d in c_dfs]
        c_sc_rt_rate = [(s/e*100) if e else 0.0 for s, e in zip(c_sm('self_corrected_runtime'), c_rt_errs)]
        c_sc_tl_rate = [(s/e*100) if e else 0.0 for s, e in zip(c_sm('self_corrected_tool'), c_tl_errs)]

        c_lat = f"{m_s(c_mn('total_llm_latency_sec'),2,'s')} / {m_s(c_mn('avg_llm_latency_per_turn_sec'),2,'s')} / {m_s(c_mn('avg_llm_latency_per_step_sec'),2,'s')}"
        c_ctx = f"{m_s(c_mn('context_growth_total'),1)} / {m_s(c_mn('avg_context_growth_per_turn'),1)} / {m_s(c_mn('avg_context_growth_per_step'),1)}"

        cat_avgs_str += f"| {cat} | {m_s(c_succ_rate,1,'%')} | {m_s(c_mn('total_input_tokens'),1)} | {m_s(c_mn('total_output_tokens'),1)} | {m_s(c_mn('total_thinking_tokens'),1)} | {m_s(c_mn('turn_count'),1)} | {m_s(c_mn('step_count'),1)} | {c_lat} | {c_ctx} | {m_s(c_mn('runtime_error_count'),2)} | {m_s(c_mn('tool_error_count'),2)} | {m_s(c_mn('redundant_tool_calls'),2)} | {m_s(c_sc_rt_rate,1,'%')} | {m_s(c_sc_tl_rate,1,'%')} |\n"

    md += "\n### Category Averages\n"
    md += "| Category | Success Rate | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | Latency (Total/Turn/Step) | Context Growth (Total/Turn/Step) | Runtime Errors | Tool Errors | Redundant | Runtime Recovery % | Tool Recovery % |\n"
    md += "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
    md += cat_avgs_str

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"   -> Saved: {md_path.name}")


def generate_aggregated_comparison(model_t, succ_dfs, fail_dfs):
    """Aggregates metrics for the 'fair comparison' intersection across multiple runs."""
    safe_model_tag = model_t.replace("/", "_").replace("\\", "_")
    output_dir = Path(f"metrics/{safe_model_tag}/comparison_aggregated")
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / "fair_comparison_aggregated.md"

    # concat and save raw merged files
    for i, (s, f) in enumerate(zip(succ_dfs, fail_dfs), 1):
        s['run_id'] = i
        f['run_id'] = i
    pd.concat(succ_dfs).to_csv(output_dir / "both_succeeded_raw_aggregated.csv", index=False)
    pd.concat(fail_dfs).to_csv(output_dir / "both_failed_raw_aggregated.csv", index=False)

    md = f"# Aggregated Fair Metric Comparison: `regular-fc` vs `ptc-fc`\n"
    md += f"**Model:** `{model_t}` (Over {len(succ_dfs)} runs)\n\n"
    md += "> This report compares metrics ONLY on the exact same tasks where both setups achieved the same outcome (both succeeded or both failed).\n\n"

    metrics_to_compare = [
        ("Total Input Tokens", "total_input_tokens", 2),
        ("Total Output Tokens", "total_output_tokens", 2),
        ("Total Thinking Tokens", "total_thinking_tokens", 2),
        ("Total Cost $", "total_cost", 5),
        ("Task Horizon (Turns)", "turn_count", 2),
        ("Steps", "step_count", 2),
        ("LLM Latency (sec)", "total_llm_latency_sec", 2),
        ("Context Growth (Total)", "context_growth_total", 2),
        ("Tool Calls (Total)", "tool_call_count", 2),
        ("Redundant Tool Calls", "redundant_tool_calls", 2),
        ("Runtime Errors", "runtime_error_count", 2),
        ("Tool Errors", "tool_error_count", 2)
    ]

    def build_table(subset_dfs, title):
        n_tasks = [len(df) for df in subset_dfs]
        t = f"## {title} (Based on {m_s(n_tasks, 0)} exact matching tasks)\n"
        t += "| Metric (Average per task) | `regular-fc` | `ptc-fc` | Difference | % Change |\n"
        t += "|---|---|---|---|---|\n"

        for label, col, dec in metrics_to_compare:
            val_reg = [df[f"{col}_reg"].mean() if not df.empty else np.nan for df in subset_dfs]
            val_ptc = [df[f"{col}_ptc"].mean() if not df.empty else np.nan for df in subset_dfs]
            diffs = [p - r for p, r in zip(val_ptc, val_reg)]

            pct_changes = [(d / r * 100) if r and not pd.isna(r) and r != 0 else 0.0 for d, r in zip(diffs, val_reg)]

            t += f"| **{label}** | {m_s(val_reg, dec)} | {m_s(val_ptc, dec)} | {m_s_diff(diffs, dec)} | {m_s_diff(pct_changes, dec, '%')} |\n"
        return t + "\n"

    md += build_table(succ_dfs, "1. Tasks Where BOTH Succeeded")
    md += build_table(fail_dfs, "2. Tasks Where BOTH Failed")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"   -> Saved: {md_path.name}")


def get_categories():
    single_turn = ["simple_java", "simple_javascript", "simple_python", "multiple", "live_simple", "live_multiple"]
    multi_turn = ["multi_turn_base", "multi_turn_long_context", "multi_turn_miss_func", "multi_turn_miss_param"]
    irrelevance = ["irrelevance", "live_irrelevance", "live_relevance"]
    return {"single_turn": single_turn, "multi_turn": multi_turn, "irrelevance": irrelevance}

# Build a fast lookup dictionary for Pandas: {'simple_java': 'single_turn', ...}
CATEGORY_LOOKUP = {
    subcat: meta_cat
    for meta_cat, subcats in get_categories().items()
    for subcat in subcats
}

# Official BFCL Weighting Scheme Implementation
# BFCL mixes Unweighted (equal representation) and Weighted (test count representation) averages.
CATEGORY_WEIGHTS = {

    # ==========================================
    # SINGLE-TURN META-CATEGORY
    # Mixes "Live" (Weighted) and "Non-Live" (Unweighted).
    # We assign a total weight of 0.5 to Live and 0.5 to Non-Live to keep them balanced.
    # ==========================================

    # --- NON-LIVE (Unweighted across structure) ---
    # 'Simple' gets 0.25 total weight, split equally among its 3 languages
    "simple_java":       0.25 / 3.0,
    "simple_javascript": 0.25 / 3.0,
    "simple_python":     0.25 / 3.0,
    # 'Multiple' gets 0.25 total weight (equal to the entire Simple category)
    "multiple":          0.25,

    # --- LIVE (Weighted by test counts) ---
    # 258 (Simple) and 1053 (Multiple) out of 1311 total live tests
    "live_simple":       0.50 * (258.0 / 1311.0),
    "live_multiple":     0.50 * (1053.0 / 1311.0),


    # ==========================================
    # MULTI-TURN META-CATEGORY
    # BFCL explicitly states: "Unweighted Average"
    # All subcategories get an equal weight of 1.0.
    # ==========================================
    "multi_turn_base":         1.0,
    "multi_turn_long_context": 1.0,
    "multi_turn_miss_func":    1.0,
    "multi_turn_miss_param":   1.0,


    # ==========================================
    # IRRELEVANCE META-CATEGORY
    # Custom Hybrid Weighting:
    # 'irrelevance' and 'live_irrelevance' are weighted equally to each other.
    # However, the combined "Irrelevance" concept (1124 tests) vs "Relevance" (16 tests)
    # is weighted proportionally by their actual test case counts.
    # ==========================================
    # Total Irrelevance tests = 240 + 884 = 1124. Split equally -> 562 each.
    "irrelevance":      562.0,
    "live_irrelevance": 562.0,
    "live_relevance":   16.0
}

# --- Execution ---
if __name__ == "__main__":
    model_tags = ["OpenAI/gpt-5-mini-2025-08-07"]
    # model_tags = ["vLLM/google/gemma-4-E4B-it"]
    setups = ["ptc-fc", "regular-fc"]
    runs = [1, 2, 3]

    for model_t in model_tags:
        safe_model = model_t.replace("/", "_").replace("\\", "_")
        print(f"\n=============================================")
        print(f"Processing Aggregates for {model_t}")
        print(f"=============================================")

        # aggregate Single Setups (ptc-fc and regular-fc)
        for setup_t in setups:
            dfs = []
            for r in runs:
                p = Path(f"metrics/{safe_model}/{setup_t}-runs/run-{r}/metrics_data.csv")
                if p.exists():
                    df = pd.read_csv(p)
                    # Add meta_category to older CSV data retroactively
                    df['meta_category'] = df['category'].map(CATEGORY_LOOKUP).fillna('unknown')
                    # backwards compatibility: calculate total_cost if not present in older runs
                    if 'total_cost' not in df.columns:
                        costs = get_model_cost(model_t)
                        if costs:
                            df['total_cost'] = (df['total_input_tokens'] * costs[0] +
                                                df['total_thinking_tokens'] * costs[1] +
                                                df['total_output_tokens'] * costs[2])
                        else:
                            df['total_cost'] = 0.0
                    dfs.append(df)

            if dfs:
                print(f"\nFound {len(dfs)} runs for {setup_t}. Aggregating...")
                generate_aggregated_report(model_t, setup_t, dfs)

        # aggregate fair comparisons
        succ_dfs, fail_dfs = [], []
        for r in runs:
            p_s = Path(f"metrics/{safe_model}/comparison-runs/run-{r}/both_succeeded_raw.csv")
            p_f = Path(f"metrics/{safe_model}/comparison-runs/run-{r}/both_failed_raw.csv")
            if p_s.exists() and p_f.exists():
                succ_dfs.append(pd.read_csv(p_s))
                fail_dfs.append(pd.read_csv(p_f))

        if succ_dfs and fail_dfs:
            print(f"\nFound {len(succ_dfs)} runs for Comparison Intersection. Aggregating...")
            generate_aggregated_comparison(model_t, succ_dfs, fail_dfs)