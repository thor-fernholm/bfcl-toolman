import os
import time
import re
import json
import datetime
from pathlib import Path
from dotenv import load_dotenv
from langfuse import Langfuse
import pandas as pd

# Load Environment Variables
root_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(root_env_path)

LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_BASE_URL = os.getenv("LANGFUSE_BASE_URL")

if not LANGFUSE_SECRET_KEY or not LANGFUSE_PUBLIC_KEY or not LANGFUSE_BASE_URL:
    raise ValueError("Missing Langfuse environment variables in .env")

langfuse = Langfuse(
    public_key=LANGFUSE_PUBLIC_KEY,
    secret_key=LANGFUSE_SECRET_KEY,
    host=LANGFUSE_BASE_URL,
)

class MetricsCalculator:
    def __init__(self, target_tags):
        self.results = []
        self.target_tags = target_tags
        # Create a safe folder name from the tags (e.g., ptc-fc_OpenAI_gpt-5-mini)
        safe_tag_name = "_".join(target_tags).replace("/", "_").replace("\\", "_")
        self.output_dir = Path(f"custom_metrics/{safe_tag_name}")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def fetch_10_traces_by_tags(self, tags, max_pages=10):
        """Fetches all traces matching the given tags handling pagination."""
        print(f"Fetching traces for tags: {tags}...")
        all_traces = []
        page = 1

        while page <= max_pages:
            response = langfuse.api.trace.list(tags=tags, page=page, limit=10)
            if not response.data:
                break
            all_traces.extend(response.data)
            page += 1
            if len(all_traces) >= 10:
                all_traces = all_traces[:10]
                break

        print(f"Found {len(all_traces)} traces.")
        return all_traces

    def fetch_traces_by_tags(self, tags, max_pages=100):
        """Fetches all traces matching the given tags handling pagination."""
        print(f"Fetching traces for tags: {tags}...")
        all_traces = []
        page = 1

        while page <= max_pages:
            response = langfuse.api.trace.list(tags=tags, page=page, limit=100)
            if not response.data:
                break
            all_traces.extend(response.data)
            page += 1

        print(f"Found {len(all_traces)} traces.")
        return all_traces

    def fetch_trace_observations(self, trace_id, max_pages=100):
        """Fetches all observations attached to a specific trace."""
        return langfuse.api.legacy.observations_v1.get_many(trace_id=trace.id, limit=100).data

    def fetch_trace_scores(self, trace_id):
        """Fetches all scores attached to a specific trace."""
        scores = langfuse.api.scores.get_many(trace_id=trace_id).data
        return {score.name: score.value for score in scores}

    def extract_category(self, test_id):
        """
        Extracts the benchmark category from the test_id.
        Example: 'multi_turn_base_42' -> 'multi_turn_base'
        """
        if not test_id:
            return "unknown"
        # Removes the trailing underscore and number
        return re.sub(r'_\d+$', '', test_id)

    def process_trace(self, trace):
        """Calculates metrics for a single trace (test case)."""
        observations = self.fetch_trace_observations(trace.id)
        scores = self.fetch_trace_scores(trace.id)
        test_id = trace.name
        is_success = scores.get("success", False)

        # Sort observations chronologically to properly calculate context growth over time
        observations = sorted(observations, key=lambda x: getattr(x, 'start_time', None) or datetime.datetime.min)

        # Initialize Trace-Level Metrics
        trace_metrics = {
            "trace_id": trace.id,
            "test_id": test_id,
            "category": self.extract_category(test_id),
            "success": is_success,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_thinking_tokens": 0,
            "total_llm_latency_sec": 0.0,
            "turn_count": 0,
            "error_count": 0,             # Langfuse general errors
            "runtime_error_count": 0,     # Goja syntax/runtime errors
            "tool_error_count": 0,        # Benchmark tool constraints
            "tool_call_count": 0,
            "redundant_tool_calls": 0,
            "context_growth_total": 0,
            "avg_context_growth_per_step": 0.0,
            "self_corrected_runtime": False,
            "self_corrected_tool": False
        }

        turn_latencies = {}
        seen_tools = set()
        step_input_tokens_sequence = []

        # Iterate through the fully populated spans
        for obs in observations:
            # OTel nests everything under an "attributes" key in the metadata dictionary
            raw_metadata = obs.metadata or {}
            attributes = raw_metadata.get("attributes", raw_metadata)

            span_type = attributes.get("bench.span_type")
            span_tag = attributes.get("bench.span_tag")
            obs_name = getattr(obs, 'name', '') or ''

            # Fallback checks (just in case)
            if not span_type:
                if obs_name.startswith("chat"): span_type = "step"
                elif obs_name.startswith("turn_"): span_type = "turn"
                elif obs_name.startswith("execute_tool"): span_type = "tool"

            # Check for errors
            if getattr(obs, 'level', '') == "ERROR":
                trace_metrics["error_count"] += 1
            if span_tag == "runtime_error":
                trace_metrics["runtime_error_count"] += 1
            elif span_tag == "tool_error":
                trace_metrics["tool_error_count"] += 1

            # Calculate Latency Safely
            span_latency = 0.0
            if getattr(obs, 'latency', None) is not None:
                span_latency = obs.latency
            elif getattr(obs, 'start_time', None) and getattr(obs, 'end_time', None):
                span_latency = (obs.end_time - obs.start_time).total_seconds()

            if span_type == "step":
                step_input = 0
                usage = getattr(obs, 'usage', None)
                if usage:
                    step_input += getattr(usage, 'input', 0) or 0
                    trace_metrics["total_output_tokens"] += getattr(usage, 'output', 0) or 0

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
            trace_metrics["avg_context_growth_per_step"] = trace_metrics["context_growth_total"] / (len(step_input_tokens_sequence) - 1)
        elif len(step_input_tokens_sequence) == 1:
            trace_metrics["context_growth_total"] = step_input_tokens_sequence[0] # Single step context size

        # Self-Correction Check
        # True if the trace ultimately succeeded despite encountering a runtime or tool error
        if is_success and trace_metrics["runtime_error_count"] > 0:
            trace_metrics["self_corrected_runtime"] = True
        if is_success and trace_metrics["tool_error_count"] > 0:
            trace_metrics["self_corrected_tool"] = True

        # Average latency per turn
        if trace_metrics["turn_count"] > 0:
            trace_metrics["avg_llm_latency_per_turn_sec"] = trace_metrics["total_llm_latency_sec"] / trace_metrics["turn_count"]

        self.results.append(trace_metrics)


    def generate_report(self):
        if not self.results:
            print("No data to report.")
            return None

        df = pd.DataFrame(self.results)
        df['success'] = df['success'].astype(int)

        # Filter successes and failures
        df_success = df[df['success'] == 1]
        df_fail = df[df['success'] == 0]

        # Calculate specific global metrics
        global_success_rate = df['success'].mean() * 100

        traces_with_runtime_errors = len(df[df['runtime_error_count'] > 0])
        self_corrected_runtime_rate = (len(df[df['self_corrected_runtime'] == True]) / traces_with_runtime_errors * 100) if traces_with_runtime_errors > 0 else 0.0
        traces_with_tool_errors = len(df[df['tool_error_count'] > 0])
        self_corrected_tool_rate = (len(df[df['self_corrected_tool'] == True]) / traces_with_tool_errors * 100) if traces_with_tool_errors > 0 else 0.0

        # Build Markdown content
        md = f"# Benchmark Metrics: `{' | '.join(self.target_tags)}`\n\n"
        md += f"**Total Tests Run:** {len(df)}\n"
        md += f"**Global Success Rate:** {global_success_rate:.2f}%\n\n"

        md += "## 1. Operational Efficiency & Latency Trade-offs\n"
        md += "| Metric | All Tests | Successes | Failures |\n"
        md += "|---|---|---|---|\n"
        md += f"| **Avg Input Tokens** | {df['total_input_tokens'].mean():.1f} | {df_success['total_input_tokens'].mean():.1f} | {df_fail['total_input_tokens'].mean():.1f} |\n"
        md += f"| **Avg Output Tokens** | {df['total_output_tokens'].mean():.1f} | {df_success['total_output_tokens'].mean():.1f} | {df_fail['total_output_tokens'].mean():.1f} |\n"
        md += f"| **Avg Thinking Tokens** | {df['total_thinking_tokens'].mean():.1f} | {df_success['total_thinking_tokens'].mean():.1f} | {df_fail['total_thinking_tokens'].mean():.1f} |\n"
        md += f"| **Avg Latency (Total)** | {df['total_llm_latency_sec'].mean():.2f}s | {df_success['total_llm_latency_sec'].mean():.2f}s | {df_fail['total_llm_latency_sec'].mean():.2f}s |\n"
        md += f"| **Avg Latency (Per Turn)** | {df['avg_llm_latency_per_turn_sec'].mean():.2f}s | {df_success['avg_llm_latency_per_turn_sec'].mean():.2f}s | {df_fail['avg_llm_latency_per_turn_sec'].mean():.2f}s |\n"
        md += f"| **Total Context Growth** | {df['context_growth_total'].mean():.1f} | {df_success['context_growth_total'].mean():.1f} | {df_fail['context_growth_total'].mean():.1f} |\n"
        md += f"| **Context Growth (Per Step)**| {df['avg_context_growth_per_step'].mean():.1f} | {df_success['avg_context_growth_per_step'].mean():.1f} | {df_fail['avg_context_growth_per_step'].mean():.1f} |\n\n"

        md += "## 2. Robustness, Errors & Hallucinations\n"
        md += f"- **Self-Correction runtime Success Rate:** {self_corrected_runtime_rate:.2f}% *(Solved {len(df[df['self_corrected_runtime']==True])} out of {traces_with_runtime_errors} tests that encountered a runtime error)*\n"
        md += f"- **Self-Correction tool Success Rate:** {self_corrected_tool_rate:.2f}% *(Solved {len(df[df['self_corrected_tool']==True])} out of {traces_with_tool_errors} tests that encountered a tool error)*\n"
        md += f"- **Avg Runtime Errors (Syntax/Goja):** {df['runtime_error_count'].mean():.2f} per test\n"
        md += f"- **Avg Tool Constraints Errors (BFCL):** {df['tool_error_count'].mean():.2f} per test\n"
        md += f"- **Avg Redundant Tool Calls:** {df['redundant_tool_calls'].mean():.2f} per test *(Proxy for hallucination/forgetfulness)*\n"
        md += f"- **Avg Task Horizon Length (Turns):** {df['turn_count'].mean():.2f} turns per test\n\n"

        md += "## 3. Breakdown by Category\n"

        # Calculate Category Aggregations
        cat_df = df.groupby('category').agg(
            tests=('test_id', 'count'),
            success_rate=('success', lambda x: x.mean() * 100),
            avg_turns=('turn_count', 'mean'),
            avg_latency=('total_llm_latency_sec', 'mean'),
            avg_input=('total_input_tokens', 'mean'),
            avg_runtime_err=('runtime_error_count', 'mean'),
            avg_redundant_calls=('redundant_tool_calls', 'mean')
        ).reset_index()

        # Build Markdown Table
        md += "| Category | Tests | Success Rate | Avg Turns | Avg Latency | Avg Input Tokens | Runtime Errs | Redundant Calls |\n"
        md += "|---|---|---|---|---|---|---|---|\n"
        for _, row in cat_df.iterrows():
            md += f"| {row['category']} | {row['tests']} | {row['success_rate']:.1f}% | {row['avg_turns']:.1f} | {row['avg_latency']:.2f}s | {row['avg_input']:.0f} | {row['avg_runtime_err']:.2f} | {row['avg_redundant_calls']:.2f} |\n"

        # Save files to the newly created directory
        timestamp = int(time.time())
        raw_csv_path = self.output_dir / f"metrics_raw_{timestamp}.csv"
        summary_md_path = self.output_dir / "summary.md"

        df.to_csv(raw_csv_path, index=False)
        with open(summary_md_path, "w", encoding="utf-8") as f:
            f.write(md)

        print("\n" + "="*50)
        print(f" REPORT GENERATED in '{self.output_dir}'")
        print("="*50)
        print(f"-> Raw Data: {raw_csv_path.name}")
        print(f"-> Summary:  summary.md\n")

        # Print a snippet of the MD to console
        print(md[:500] + "\n...\n")

        return df

# Bulletproof casting helper
def safe_int(val):
    if val is None:
        return 0

    # Handle if OTel passed it as a parsed Python dictionary
    if isinstance(val, dict):
        return safe_int(val.get('intValue', val.get('int_value', 0)))

    # Handle if OTel passed it as a raw JSON string
    if isinstance(val, str):
        val = val.strip()
        if val.startswith('{') and val.endswith('}'):
            try:
                parsed = json.loads(val)
                return safe_int(parsed.get('intValue', parsed.get('int_value', 0)))
            except Exception:
                return 0

    # Base case: attempt standard cast (float first to handle "12.0")
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return 0

# --- Execution ---
if __name__ == "__main__":
    target_tags = ["ptc-fc", "OpenAI/gpt-5-mini-2025-08-07"]

    calculator = MetricsCalculator(target_tags)

    # traces = calculator.fetch_traces_by_tags(target_tags)
    traces = calculator.fetch_10_traces_by_tags(target_tags)

    for i, trace in enumerate(traces):
        calculator.process_trace(trace)
        if (i + 1) % 50 == 0:
            print(f"Processed {i + 1}/{len(traces)} traces...")

    calculator.generate_report()
