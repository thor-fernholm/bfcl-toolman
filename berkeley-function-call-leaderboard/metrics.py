import os
import re
import json
import datetime
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import clickhouse_connect

# Load Environment Variables
parent_path = Path(__file__).resolve().parent
root_env_path = parent_path / ".env"
load_dotenv(root_env_path)

# You may need to add these to your .env if they differ from the defaults below
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", 8123))
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "clickhouse")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "clickhouse")

LANGFUSE_PROJECT_ID = os.getenv("LANGFUSE_PROJECT_ID")
if not LANGFUSE_PROJECT_ID:
    raise ValueError("Missing LANGFUSE_PROJECT_ID in .env file")


class MetricsCalculator:
    def __init__(self, ptc_t, model_t):
        self.results = []
        self.target_tags = [ptc_t, model_t]
        self.model_name = model_t
        self.category_map = get_categories()
        # Create a safe folder name from the tags
        safe_ptc_tag = ptc_t.replace("/", "_").replace("\\", "_")
        safe_model_tag = model_t.replace("/", "_").replace("\\", "_")
        self.output_dir = Path(f"metrics/{safe_model_tag}/{safe_ptc_tag}")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize ClickHouse Client
        print(f"Connecting to ClickHouse at {CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}...")
        self.client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD
        )

    def fetch_all_data_from_db(self):
        """Fetches Traces, Observations, and Scores in 3 bulk queries, scoped to a specific project."""
        print(f"Fetching data for tags: {self.target_tags} in project {LANGFUSE_PROJECT_ID}...")

        tags_formatted = ", ".join([f"'{t}'" for t in self.target_tags])

        # Fetch Traces (Added project_id filter)
        traces_query = f"""
                SELECT id, name 
                FROM traces 
                WHERE project_id = '{LANGFUSE_PROJECT_ID}' 
                  AND hasAll(tags, [{tags_formatted}])
            """
        traces_df = self.client.query_df(traces_query)

        if traces_df.empty:
            print("No traces found matching those tags in this project.")
            return None, None, None

        trace_ids = traces_df['id'].tolist()
        print(f"Found {len(trace_ids)} traces. Fetching nested data...")

        if len(trace_ids) == 1:
            trace_ids_str = f"('{trace_ids[0]}')"
        else:
            trace_ids_str = str(tuple(trace_ids))

        # Fetch Observations (Added project_id filter)
        obs_query = f"""
                SELECT trace_id, id, name, start_time, end_time, type, level, metadata, status_message
                FROM observations
                WHERE project_id = '{LANGFUSE_PROJECT_ID}'
                  AND trace_id IN {trace_ids_str}
            """
        obs_df = self.client.query_df(obs_query)

        # Fetch Scores (Added project_id filter)
        scores_query = f"""
                SELECT trace_id, name, value
                FROM scores
                WHERE project_id = '{LANGFUSE_PROJECT_ID}'
                  AND trace_id IN {trace_ids_str}
            """
        scores_df = self.client.query_df(scores_query)

        print(f"Loaded {len(obs_df)} observations and {len(scores_df)} scores.")
        return traces_df, obs_df, scores_df

    def extract_category(self, test_id):
        """Extracts the benchmark category from the test_id."""
        if not test_id:
            return "unknown"
        return re.sub(r'[-_]\d+(?:[-_]\d+)*$', '', test_id)

    def process_all_traces(self):
        """
        Processes all data locally in memory using dictionaries.
        No thread pools or API limits required.
        """
        traces_df, obs_df, scores_df = self.fetch_all_data_from_db()
        if traces_df is None:
            return

        # Pre-group observations by trace_id for instant O(1) lookup
        obs_dict = {}
        if not obs_df.empty:
            obs_records = obs_df.to_dict('records')
            for obs in obs_records:
                tid = obs['trace_id']
                if tid not in obs_dict:
                    obs_dict[tid] = []

                # Parse ClickHouse JSON string into Python Dictionary
                meta = obs.get('metadata')
                if isinstance(meta, str) and meta.strip():
                    try:
                        obs['metadata'] = json.loads(meta)
                    except json.JSONDecodeError:
                        obs['metadata'] = {}
                elif not meta:
                    obs['metadata'] = {}

                obs_dict[tid].append(obs)

        # Pre-group scores by trace_id
        scores_dict = {}
        if not scores_df.empty:
            scores_records = scores_df.to_dict('records')
            for sc in scores_records:
                tid = sc['trace_id']
                if tid not in scores_dict:
                    scores_dict[tid] = {}
                scores_dict[tid][sc['name']] = sc['value']

        # Process locally
        traces_records = traces_df.to_dict('records')
        for trace in tqdm(traces_records, total=len(traces_records), desc="Processing Traces"):
            trace_id = trace['id']
            test_id = trace['name']

            trace_obs = obs_dict.get(trace_id, [])
            trace_scores = scores_dict.get(trace_id, {})

            data = self.process_trace(trace_id, test_id, trace_obs, trace_scores)
            if data:
                self.results.append(data)

    def process_trace(self, trace_id, test_id, observations, scores):
        """Calculates metrics for a single trace (test case) from dictionaries."""
        is_success = scores.get("success", False)

        if not scores:
            return

        # Sort observations chronologically
        # DB start_time is already a pandas/python datetime object
        observations = sorted(observations, key=lambda x: x.get('start_time') or datetime.datetime.min)

        # get categories
        category = self.extract_category(test_id)
        meta_category = self.get_meta_category(category)

        # Initialize Trace-Level Metrics
        trace_metrics = {
            "trace_id": trace_id,
            "test_id": test_id,
            "category": category,
            "meta_category": meta_category,
            "success": is_success,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_thinking_tokens": 0,
            "avg_input_tokens_per_step": 0.0,
            "avg_output_tokens_per_step": 0.0,
            "avg_thinking_tokens_per_step": 0.0,
            "total_llm_latency_sec": 0.0,
            "step_count": 0,
            "turn_count": 0,
            "error": False,
            "runtime_error_count": 0,
            "tool_error_count": 0,
            "tool_call_count": 0,
            "avg_tool_calls_per_turn": 0.0,
            "redundant_tool_calls": 0,
            "context_growth_total": 0,
            "avg_context_growth_per_turn": 0.0,
            "avg_context_growth_per_step": 0.0,
            "self_corrected_runtime": False,
            "self_corrected_tool": False
        }

        seen_tools = set()
        step_input_tokens_sequence = []

        for obs in observations:
            raw_metadata = obs.get('metadata', {})
            attributes = raw_metadata.get("attributes", raw_metadata)

            if isinstance(attributes, str):
                try:
                    attributes = json.loads(attributes)
                except Exception:
                    attributes = {}
            elif not isinstance(attributes, dict):
                attributes = {}

            span_type = attributes.get("bench.span_type")
            span_tag = attributes.get("bench.span_tag")
            obs_name = obs.get('name', '') or ''

            # Fallback checks
            if not span_type:
                if obs_name.startswith("chat"):
                    span_type = "step"
                elif obs_name.startswith("turn_"):
                    span_type = "turn"
                elif obs_name.startswith("execute_tool"):
                    span_type = "tool"

            # Check for errors
            if obs.get('level') == "ERROR":
                status_msg = str(obs.get('status_message') or "").lower()

                # Grab from the metadata payload
                raw_metadata = obs.get('metadata', {})
                metadata_str = str(raw_metadata).lower()

                # Check for rate limit signatures
                is_rate_limit = ("status code 429" in status_msg or
                                 "rate limit" in status_msg or
                                 "status code 429" in metadata_str or
                                 "rate limit" in metadata_str)

                if is_rate_limit:
                    # Silently ignore rate limit infrastructure noise
                    pass
                else:
                    trace_metrics["error"] = True

            if span_tag == "runtime_error":
                trace_metrics["runtime_error_count"] += 1
            elif span_tag == "tool_error":
                trace_metrics["tool_error_count"] += 1

            # Calculate Latency Safely
            span_latency = 0.0
            start = obs.get('start_time')
            end = obs.get('end_time')
            if pd.notna(start) and pd.notna(end):
                span_latency = (end - start).total_seconds()

            if span_type == "step":
                trace_metrics["step_count"] += 1
                step_input = 0

                # Extract tokens purely from OTel metadata attributes
                step_input += safe_int(attributes.get("gen_ai.usage.input_tokens", 0))

                trace_metrics["total_input_tokens"] += step_input
                trace_metrics["total_output_tokens"] += safe_int(attributes.get("gen_ai.usage.output_tokens", 0))
                trace_metrics["total_thinking_tokens"] += safe_int(attributes.get("gen_ai.usage.thinking_tokens", 0))
                trace_metrics["total_llm_latency_sec"] += span_latency

                if step_input > 0:
                    step_input_tokens_sequence.append(step_input)

            elif span_type == "turn":
                trace_metrics["turn_count"] += 1

            elif span_type == "tool":
                trace_metrics["tool_call_count"] += 1
                # Redundant Tool-Call Proxy Tracking
                t_name = attributes.get("gen_ai.tool.name", "")
                t_args = attributes.get("gen_ai.tool.call.arguments", "")
                signature = f"{t_name}_{t_args}"
                if signature in seen_tools:
                    trace_metrics["redundant_tool_calls"] += 1
                else:
                    seen_tools.add(signature)

        # Context Growth Calculation
        if len(step_input_tokens_sequence) > 1:
            trace_metrics["context_growth_total"] = step_input_tokens_sequence[-1] - step_input_tokens_sequence[0]
            trace_metrics["avg_context_growth_per_step"] = trace_metrics["context_growth_total"] / (
                        len(step_input_tokens_sequence) - 1)
        elif len(step_input_tokens_sequence) == 1:
            trace_metrics["context_growth_total"] = step_input_tokens_sequence[0]

        # Self-Correction Check
        if is_success and trace_metrics["runtime_error_count"] > 0:
            trace_metrics["self_corrected_runtime"] = True
        if is_success and trace_metrics["tool_error_count"] > 0:
            trace_metrics["self_corrected_tool"] = True

        if trace_metrics["turn_count"] > 1:
            trace_metrics["avg_context_growth_per_turn"] = trace_metrics["context_growth_total"] / (
                        trace_metrics["turn_count"] - 1)
        elif trace_metrics["turn_count"] == 1:
            trace_metrics["avg_context_growth_per_turn"] = trace_metrics["context_growth_total"]

        if trace_metrics["turn_count"] > 0:
            trace_metrics["avg_tool_calls_per_turn"] = trace_metrics["tool_call_count"] / trace_metrics["turn_count"]
            trace_metrics["avg_input_tokens_per_turn"] = trace_metrics["total_input_tokens"] / trace_metrics[
                "turn_count"]
            trace_metrics["avg_output_tokens_per_turn"] = trace_metrics["total_output_tokens"] / trace_metrics[
                "turn_count"]
            trace_metrics["avg_thinking_tokens_per_turn"] = trace_metrics["total_thinking_tokens"] / trace_metrics[
                "turn_count"]
            trace_metrics["avg_llm_latency_per_turn_sec"] = trace_metrics["total_llm_latency_sec"] / trace_metrics[
                "turn_count"]

        if trace_metrics["step_count"] > 0:
            trace_metrics["avg_input_tokens_per_step"] = trace_metrics["total_input_tokens"] / trace_metrics[
                "step_count"]
            trace_metrics["avg_output_tokens_per_step"] = trace_metrics["total_output_tokens"] / trace_metrics[
                "step_count"]
            trace_metrics["avg_thinking_tokens_per_step"] = trace_metrics["total_thinking_tokens"] / trace_metrics[
                "step_count"]
            trace_metrics["avg_llm_latency_per_step_sec"] = trace_metrics["total_llm_latency_sec"] / trace_metrics[
                "step_count"]

        return trace_metrics

    def generate_report(self):
        if not self.results:
            print("No data to report.")
            return None

        df = pd.DataFrame(self.results)
        df['success'] = df['success'].astype(int)
        df['error'] = df['error'].astype(int)
        df['self_corrected_runtime'] = df['self_corrected_runtime'].astype(int)
        df['self_corrected_tool'] = df['self_corrected_tool'].astype(int)

        # Build Markdown content
        md = f"# Benchmark Metrics: `{' | '.join(self.target_tags)}`\n\n"

        # --- GLOBAL TOTALS & AVERAGES ---
        md += "## 1. Global Totals & Averages\n"

        total_tests = len(df)
        successes = df['success'].sum()
        global_success_rate = (successes / total_tests * 100) if total_tests else 0.0

        df['total_cost'] = 0
        model_costs = get_model_cost(self.model_name)
        if model_costs:
            in_cost = df['total_input_tokens'] * model_costs[0]
            think_cost = df['total_thinking_tokens'] * model_costs[1]
            out_cost = df['total_output_tokens'] * model_costs[2]
            df['total_cost'] = in_cost + think_cost + out_cost

        traces_with_errors = df['error'].sum()
        global_error_rate = (traces_with_errors / total_tests * 100) if total_tests else 0.0

        traces_with_rt_errors = len(df[df['runtime_error_count'] > 0])
        total_sc_rt = df['self_corrected_runtime'].sum()
        sc_rt_rate = (total_sc_rt / traces_with_rt_errors * 100) if traces_with_rt_errors > 0 else 0.0

        traces_with_tool_errors = len(df[df['tool_error_count'] > 0])
        total_sc_tool = df['self_corrected_tool'].sum()
        sc_tool_rate = (total_sc_tool / traces_with_tool_errors * 100) if traces_with_tool_errors > 0 else 0.0

        md += "| Metric | Total (Sum) | Average (Mean per test) |\n"
        md += "|---|---|---|\n"
        md += f"| **Tests Run** | {total_tests} | - |\n"
        md += f"| **Successes** | {successes} | {global_success_rate:.2f}% (Success Rate) |\n"
        md += f"| **Input Tokens** | {df['total_input_tokens'].sum():.0f} | {df['total_input_tokens'].mean():.1f} |\n"
        md += f"| **Output Tokens** | {df['total_output_tokens'].sum():.0f} | {df['total_output_tokens'].mean():.1f} |\n"
        md += f"| **Thinking Tokens** | {df['total_thinking_tokens'].sum():.0f} | {df['total_thinking_tokens'].mean():.1f} |\n"
        md += f"| **Cost $** | {df['total_cost'].sum():.4f} | {df['total_cost'].mean():.5f} |\n"
        md += f"| **Turns** | {df['turn_count'].sum():.0f} | {df['turn_count'].mean():.1f} |\n"
        md += f"| **Steps** | {df['step_count'].sum():.0f} | {df['step_count'].mean():.1f} |\n"
        md += f"| **LLM Latency (sec)** | {df['total_llm_latency_sec'].sum():.2f}s | {df['total_llm_latency_sec'].mean():.2f}s (Total) / {df['avg_llm_latency_per_turn_sec'].mean():.2f}s (Per Turn) / {df['avg_llm_latency_per_step_sec'].mean():.2f}s (Per Step) |\n"
        md += f"| **Errors (Total)** | {traces_with_errors} | {global_error_rate} |\n"
        md += f"| **Runtime Errors (Goja)** | {df['runtime_error_count'].sum()} | {df['runtime_error_count'].mean():.2f} |\n"
        md += f"| **Tool Errors (BFCL)** | {df['tool_error_count'].sum()} | {df['tool_error_count'].mean():.2f} |\n"
        md += f"| **Tool Calls** | {df['tool_call_count'].sum()} | {df['tool_call_count'].mean():.1f} (Total) / {df['avg_tool_calls_per_turn'].mean():.1f} (Per Turn) |\n"
        md += f"| **Task Horizon (Length)** | - | {df['turn_count'].mean():.2f} Turns |\n"
        md += f"| **Redundant Tool Calls** | {df['redundant_tool_calls'].sum()} | {df['redundant_tool_calls'].mean():.2f} |\n"
        md += f"| **Self-Correct (Runtime)** | {total_sc_rt} (out of {traces_with_rt_errors} err traces) | {sc_rt_rate:.1f}% (Recovery Rate) |\n"
        md += f"| **Self-Correct (Tool)** | {total_sc_tool} (out of {traces_with_tool_errors} err traces) | {sc_tool_rate:.1f}% (Recovery Rate) |\n"
        md += f"| **Context Growth** | - | {df['context_growth_total'].mean():.0f} (Total) / {df['avg_context_growth_per_turn'].mean():.0f} (Turn) / {df['avg_context_growth_per_step'].mean():.0f} (Step) |\n\n"

        # --- SPLIT BY SUCCESS/FAIL ---
        df_success = df[df['success'] == 1]
        df_fail = df[df['success'] == 0]

        md += "## 2. Averages by Outcome (Success vs. Failure)\n"
        md += "| Metric | Successes | Failures |\n"
        md += "|---|---|---|\n"
        md += f"| **Input Tokens (Test/Turn/Step)** | {df_success['total_input_tokens'].mean():.1f} / {df_success['avg_input_tokens_per_turn'].mean():.1f} / {df_success['avg_input_tokens_per_step'].mean():.1f} | {df_fail['total_input_tokens'].mean():.1f} / {df_fail['avg_input_tokens_per_turn'].mean():.1f} / {df_fail['avg_input_tokens_per_step'].mean():.1f} |\n"
        md += f"| **Output Tokens (Test/Turn/Step)** | {df_success['total_output_tokens'].mean():.1f} / {df_success['avg_output_tokens_per_turn'].mean():.1f} / {df_success['avg_output_tokens_per_step'].mean():.1f} | {df_fail['total_output_tokens'].mean():.1f} / {df_fail['avg_output_tokens_per_turn'].mean():.1f} / {df_fail['avg_output_tokens_per_step'].mean():.1f} |\n"
        md += f"| **Thinking Tokens (Test/Turn/Step)** | {df_success['total_thinking_tokens'].mean():.1f}  / {df_success['avg_thinking_tokens_per_turn'].mean():.1f} / {df_success['avg_thinking_tokens_per_step'].mean():.1f} | {df_fail['total_thinking_tokens'].mean():.1f} / {df_fail['avg_thinking_tokens_per_turn'].mean():.1f} / {df_fail['avg_thinking_tokens_per_step'].mean():.1f} |\n"
        md += f"| **Turns** | {df_success['turn_count'].mean():.1f} | {df_fail['turn_count'].mean():.1f} |\n"
        md += f"| **Steps** | {df_success['step_count'].mean():.1f} | {df_fail['step_count'].mean():.1f} |\n"
        md += f"| **LLM Latency (Total)** | {df_success['total_llm_latency_sec'].mean():.2f}s | {df_fail['total_llm_latency_sec'].mean():.2f}s |\n"
        md += f"| **LLM Latency (Per Turn)** | {df_success['avg_llm_latency_per_turn_sec'].mean():.2f}s | {df_fail['avg_llm_latency_per_turn_sec'].mean():.2f}s |\n"
        md += f"| **LLM Latency (Per Step)** | {df_success['avg_llm_latency_per_step_sec'].mean():.2f}s | {df_fail['avg_llm_latency_per_step_sec'].mean():.2f}s |\n"
        md += f"| **Context Growth (Total)** | {df_success['context_growth_total'].mean():.1f} | {df_fail['context_growth_total'].mean():.1f} |\n"
        md += f"| **Context Growth (Per Turn)**| {df_success['avg_context_growth_per_turn'].mean():.1f} | {df_fail['avg_context_growth_per_turn'].mean():.1f} |\n"
        md += f"| **Context Growth (Per Step)**| {df_success['avg_context_growth_per_step'].mean():.1f} | {df_fail['avg_context_growth_per_step'].mean():.1f} |\n\n"

        # --- BREAKDOWN BY CATEGORY ---
        def aggregate_metrics(group_col):
            return df.groupby(group_col).agg(
                tests=('test_id', 'count'),
                successes=('success', 'sum'),
                success_rate=('success', lambda x: x.mean() * 100),
                sum_input=('total_input_tokens', 'sum'),
                avg_input=('total_input_tokens', 'mean'),
                sum_output=('total_output_tokens', 'sum'),
                avg_output=('total_output_tokens', 'mean'),
                sum_thinking=('total_thinking_tokens', 'sum'),
                avg_thinking=('total_thinking_tokens', 'mean'),
                sum_turns=('turn_count', 'sum'),
                avg_turns=('turn_count', 'mean'),
                sum_steps=('step_count', 'sum'),
                avg_steps=('step_count', 'mean'),
                sum_latency=('total_llm_latency_sec', 'sum'),
                avg_latency=('total_llm_latency_sec', 'mean'),
                avg_latency_turn=('avg_llm_latency_per_turn_sec', 'mean'),
                avg_latency_step=('avg_llm_latency_per_step_sec', 'mean'),
                avg_ctx_total=('context_growth_total', 'mean'),
                avg_ctx_turn=('avg_context_growth_per_turn', 'mean'),
                avg_ctx_step=('avg_context_growth_per_step', 'mean'),
                sum_runtime_err=('runtime_error_count', 'sum'),
                avg_runtime_err=('runtime_error_count', 'mean'),
                sum_tool_err=('tool_error_count', 'sum'),
                avg_tool_err=('tool_error_count', 'mean'),
                sum_redundant=('redundant_tool_calls', 'sum'),
                avg_redundant=('redundant_tool_calls', 'mean'),
                sum_sc_rt=('self_corrected_runtime', 'sum'),
                err_traces_rt=('runtime_error_count', lambda x: (x > 0).sum()),
                sum_sc_tool=('self_corrected_tool', 'sum'),
                err_traces_tool=('tool_error_count', lambda x: (x > 0).sum())
            ).reset_index()

        def format_markdown_tables(agg_df, col_name):
            txt = f"### {col_name.replace('_', ' ').title()} Totals\n"
            txt += f"| {col_name.replace('_', ' ').title()} | Tests | Successes | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | LLM Latency | Runtime Errors | Tool Errors | Redundant Calls | Self-Corrects (Runtime) | Self-Corrects (Tool) |\n"
            txt += "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
            for _, r in agg_df.iterrows():
                txt += f"| {r[col_name]} | {r['tests']} | {r['successes']} | {r['sum_input']:.0f} | {r['sum_output']:.0f} | {r['sum_thinking']:.0f} | {r['sum_turns']:.0f} | {r['sum_steps']:.0f} | {r['sum_latency']:.2f}s | {r['sum_runtime_err']} | {r['sum_tool_err']} | {r['sum_redundant']} | {r['sum_sc_rt']} | {r['sum_sc_tool']} |\n"

            txt += f"\n### {col_name.replace('_', ' ').title()} Averages\n"
            txt += f"| {col_name.replace('_', ' ').title()} | Success Rate | Input Tokens | Output Tokens | Thinking Tokens | Turns | Steps | Latency (Total/Turn/Step) | Context Growth (Total/Turn/Step) | Runtime Errors | Tool Errors | Redundant | Runtime Recovery % | Tool Recovery % |\n"
            txt += "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
            for _, r in agg_df.iterrows():
                sc_rt_rate = (r['sum_sc_rt'] / r['err_traces_rt'] * 100) if r['err_traces_rt'] > 0 else 0.0
                sc_tool_rate = (r['sum_sc_tool'] / r['err_traces_tool'] * 100) if r['err_traces_tool'] > 0 else 0.0
                latency_str = f"{r['avg_latency']:.2f}s / {r['avg_latency_turn']:.2f}s / {r['avg_latency_step']:.2f}s"
                ctx_str = f"{r['avg_ctx_total']:.1f} / {r['avg_ctx_turn']:.1f} / {r['avg_ctx_step']:.1f}"

                txt += f"| {r[col_name]} | {r['success_rate']:.2f}% | {r['avg_input']:.1f} | {r['avg_output']:.1f} | {r['avg_thinking']:.1f} | {r['avg_turns']:.1f} | {r['avg_steps']:.1f} | {latency_str} | {ctx_str} | {r['avg_runtime_err']:.2f} | {r['avg_tool_err']:.2f} | {r['avg_redundant']:.2f} | {sc_rt_rate:.1f}% | {sc_tool_rate:.1f}% |\n"
            return txt + "\n"

        # --- BREAKDOWN BY META-CATEGORY ---
        md += "## 3. Breakdown by Meta-Category\n\n"
        meta_cat_df = aggregate_metrics('meta_category')
        md += format_markdown_tables(meta_cat_df, 'meta_category')

        # --- BREAKDOWN BY SUBCATEGORY ---
        md += "## 4. Breakdown by Category\n\n"
        cat_df = aggregate_metrics('category')
        md += format_markdown_tables(cat_df, 'category')

        # Save files
        raw_csv_path = self.output_dir / "metrics_data.csv"
        summary_md_path = self.output_dir / "summary.md"
        plot_filename = self.output_dir / "context_dropoff_plot.pdf"

        plt.figure(figsize=(9, 5))
        if df['total_input_tokens'].nunique() > 1:
            try:
                df['context_bin'] = pd.qcut(df['total_input_tokens'], q=5, duplicates='drop')
                plot_df = df.groupby('context_bin', observed=False)['success'].mean() * 100

                ax = plot_df.plot(kind='bar', color='#4C72B0', edgecolor='black')
                plt.title("Context Size vs. Success Rate (Drop-off Metric)", fontsize=14)
                plt.xlabel("Context Size Range (Total Input Tokens)", fontsize=12)
                plt.ylabel("Success Rate (%)", fontsize=12)

                labels = [f"{int(interval.left)} - {int(interval.right)}" for interval in plot_df.index]
                ax.set_xticklabels(labels, rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig(plot_filename, dpi=300)
            except Exception as e:
                print(f"Plot generation skipped: {e}")
                plot_filename = None
        plt.close()

        df.drop(columns=['context_bin'], errors='ignore').to_csv(raw_csv_path, index=False)
        with open(summary_md_path, "w", encoding="utf-8") as f:
            f.write(md)

        print("\n" + "=" * 50)
        print(f" REPORT GENERATED in '{self.output_dir}'")
        print("=" * 50)
        print(f"-> Raw Data: {raw_csv_path.name}")
        print(f"-> Summary:  summary.md")
        if plot_filename and plot_filename.exists():
            print(f"-> Plot:     {plot_filename.name}\n")

        return df

    def get_meta_category(self, category):
        """Maps a subcategory to its meta-category."""
        for meta_cat, subcats in self.category_map.items():
            if category in subcats:
                return meta_cat
        return "unknown"


def safe_int(val):
    if val is None:
        return 0
    if pd.isna(val):
        return 0
    if isinstance(val, dict):
        return safe_int(val.get('intValue', val.get('int_value', 0)))
    if isinstance(val, str):
        val = val.strip()
        if val.startswith('{') and val.endswith('}'):
            try:
                parsed = json.loads(val)
                return safe_int(parsed.get('intValue', parsed.get('int_value', 0)))
            except Exception:
                return 0
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return 0


def generate_fair_comparison_report(df_ptc, df_reg, model_t):
    """
    Generates a fair comparison report by intersecting tasks where
    both ptc-fc and regular-fc achieved the exact same outcome.
    """
    if df_ptc is None or df_ptc.empty or df_reg is None or df_reg.empty:
        print(f"Skipping fair comparison for {model_t} due to missing data.")
        return

    # Merge on test_id to align the exact same tasks side-by-side
    df_merged = pd.merge(df_ptc, df_reg, on='test_id', suffixes=('_ptc', '_reg'))

    if df_merged.empty:
        print(f"No common test_ids found for {model_t}.")
        return

    # Filter for intersection sets
    both_succ = df_merged[(df_merged['success_ptc'] == 1) & (df_merged['success_reg'] == 1)]
    both_fail = df_merged[(df_merged['success_ptc'] == 0) & (df_merged['success_reg'] == 0)]

    safe_model_tag = model_t.replace("/", "_").replace("\\", "_")
    output_dir = Path(f"metrics/{safe_model_tag}/comparison")
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / "fair_comparison.md"

    # Save the raw merged data so you can inspect individual intersecting rows if needed
    both_succ.to_csv(output_dir / "both_succeeded_raw.csv", index=False)
    both_fail.to_csv(output_dir / "both_failed_raw.csv", index=False)

    md = f"# Fair Metric Comparison: `regular-fc` vs `ptc-fc`\n"
    md += f"**Model:** `{model_t}`\n\n"
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

    def build_table(subset_df, title):
        if subset_df.empty:
            return f"## {title}\n*No tasks found in this category.*\n\n"

        n_tasks = len(subset_df)
        t = f"## {title} (Based on {n_tasks} exact matching tasks)\n"
        t += "| Metric (Average per task) | `regular-fc` | `ptc-fc` | Difference | % Change |\n"
        t += "|---|---|---|---|---|\n"

        for label, col, dec in metrics_to_compare:
            val_reg = subset_df[f"{col}_reg"].mean()
            val_ptc = subset_df[f"{col}_ptc"].mean()
            diff = val_ptc - val_reg

            # Avoid division by zero
            pct_change = (diff / val_reg * 100) if val_reg != 0 else 0.0

            diff_str = f"+{diff:.{dec}f}" if diff > 0 else f"{diff:.{dec}f}"
            pct_str = f"+{pct_change:.{dec}f}%" if pct_change > 0 else f"{pct_change:.{dec}f}%"

            t += f"| **{label}** | {val_reg:.{dec}f} | {val_ptc:.{dec}f} | {diff_str} | {pct_str} |\n"

        return t + "\n"

    md += build_table(both_succ, "1. Tasks Where BOTH Succeeded")
    md += build_table(both_fail, "2. Tasks Where BOTH Failed")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"\n" + "=" * 50)
    print(f" FAIR COMPARISON REPORT GENERATED in '{output_dir}'")
    print("=" * 50)
    print(f"-> Summary: fair_comparison.md\n")


def get_model_cost(model_name):
    match model_name:
        case "OpenAI/gpt-5-mini-2025-08-07":
            return (0.25 * 1e-06, 2.0 * 1e-06, 2.0 * 1e-06)
        case _:
            return None


def get_categories():
    single_turn = ["simple_java", "simple_javascript", "simple_python", "multiple", "live_simple", "live_multiple"]
    multi_turn = ["multi_turn_base", "multi_turn_long_context", "multi_turn_miss_func", "multi_turn_miss_param"]
    irrelevance = ["irrelevance", "live_irrelevance", "live_relevance"]
    return {"single_turn": single_turn, "multi_turn": multi_turn, "irrelevance": irrelevance}


# --- Execution ---
if __name__ == "__main__":
    ptc_tags = ["ptc-fc", "regular-fc"]
    # model_tags = ["OpenAI/gpt-5-mini-2025-08-07"]
    model_tags = ["vLLM/google/gemma-4-E4B-it"]

    for model_t in model_tags:
        dfs = {}
        for ptc_t in ptc_tags:
            target_tags = [ptc_t, model_t]
            calculator = MetricsCalculator(ptc_t, model_t)
            calculator.process_all_traces()
            df = calculator.generate_report()
            dfs[ptc_t] = df

        # run the fair comparison
        if "ptc-fc" in dfs and "regular-fc" in dfs:
            generate_fair_comparison_report(dfs["ptc-fc"], dfs["regular-fc"], model_t)
