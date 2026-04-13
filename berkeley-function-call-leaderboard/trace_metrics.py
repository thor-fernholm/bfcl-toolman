import os
import time
import re
from pathlib import Path
from dotenv import load_dotenv
from langfuse import Langfuse
import pandas as pd
import json

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
    def __init__(self):
        self.results = []

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
        # observations = []
        # page = 1
        # while page <= max_pages:
        #     obs_resp = langfuse.api.legacy.observations_v1.get_many(trace_id=trace.id, page=page, limit=100)
        #     # obs_resp = langfuse.api.observations.get_many(trace_id=trace.id, limit=100)
        #     if not obs_resp.data:
        #         break
        #     observations.extend(obs_resp.data)
        #     page += 1
        #
        # return observations
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

        # Initialize Trace-Level Metrics
        trace_metrics = {
            "trace_id": trace.id,
            "test_id": test_id,
            "category": self.extract_category(test_id),
            "success": scores.get("success", False),
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_thinking_tokens": 0,
            "total_llm_latency_sec": 0.0,
            "turn_count": 0,
            "error_count": 0,
            "tool_call_count": 0
        }

        turn_latencies = {}

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
            if getattr(obs, 'level', '') == "ERROR" or span_tag in ["runtime_error", "tool_error"]:
                trace_metrics["error_count"] += 1

            # Calculate Latency Safely
            step_latency = 0.0
            if getattr(obs, 'latency', None) is not None:
                step_latency = obs.latency
            elif getattr(obs, 'start_time', None) and getattr(obs, 'end_time', None):
                step_latency = (obs.end_time - obs.start_time).total_seconds()

            if span_type == "step":
                # Check for tokens in Langfuse's native usage object
                usage = getattr(obs, 'usage', None)
                if usage:
                    trace_metrics["total_input_tokens"] += getattr(usage, 'input', 0) or 0
                    trace_metrics["total_output_tokens"] += getattr(usage, 'output', 0) or 0

                # Check for tokens still sitting in the OTel attributes
                trace_metrics["total_input_tokens"] += safe_int(attributes.get("gen_ai.usage.input_tokens", 0))
                trace_metrics["total_output_tokens"] += safe_int(attributes.get("gen_ai.usage.output_tokens", 0))
                trace_metrics["total_thinking_tokens"] += safe_int(attributes.get("gen_ai.usage.thinking_tokens", 0))

                trace_metrics["total_llm_latency_sec"] += step_latency

                parent_id = getattr(obs, 'parent_observation_id', None)
                if parent_id:
                    turn_latencies[parent_id] = turn_latencies.get(parent_id, 0) + step_latency

            elif span_type == "turn":
                trace_metrics["turn_count"] += 1

            elif span_type == "tool":
                trace_metrics["tool_call_count"] += 1

        # Calculate Turn Averages
        if trace_metrics["turn_count"] > 0:
            trace_metrics["avg_llm_latency_per_turn_sec"] = trace_metrics["total_llm_latency_sec"] / trace_metrics["turn_count"]
        else:
            trace_metrics["avg_llm_latency_per_turn_sec"] = 0.0

        self.results.append(trace_metrics)

    def process_trace_manual(self, trace):
        """Calculates metrics for a single trace (test case)."""
        full_trace = langfuse.api.trace.get(trace.id)
        observations = full_trace.observations
        scores = self.fetch_trace_scores(trace.id)
        test_id = trace.name

        # 1. Initialize Trace-Level Metrics
        trace_metrics = {
            "trace_id": trace.id,
            "test_id": test_id,
            "category": self.extract_category(test_id),
            "success": scores.get("success", False),
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_thinking_tokens": 0,
            "total_llm_latency_sec": 0.0,
            "turn_count": 0,
            "error_count": 0,
            "tool_call_count": 0
        }

        turn_latencies = {}

        # 3. Iterate through spans to extract data
        for obs in observations:
            metadata = obs.metadata or {}

            # --- BULLETPROOF SPAN TYPE CHECK ---
            span_type = metadata.get("bench.span_type")
            obs_name = getattr(obs, 'name', '') or ''

            if not span_type:
                # Fallback to the span names you set in your Go code
                if obs_name.startswith("chat"):
                    span_type = "step"
                elif obs_name.startswith("turn_"):
                    span_type = "turn"
                elif obs_name.startswith("execute_tool"):
                    span_type = "tool"

            span_tag = metadata.get("bench.span_tag")

            # Check for errors
            if getattr(obs, 'level', '') == "ERROR" or span_tag in ["runtime_error", "tool_error"]:
                trace_metrics["error_count"] += 1

            # --- EXTRACT METRICS ---

            # Calculate Latency Safely
            step_latency = 0.0
            if getattr(obs, 'latency', None) is not None:
                step_latency = obs.latency
            elif getattr(obs, 'start_time', None) and getattr(obs, 'end_time', None):
                step_latency = (obs.end_time - obs.start_time).total_seconds()

            if span_type == "step":
                # Langfuse automatically moves OTel 'gen_ai.usage.*' to the native usage object!
                usage = getattr(obs, 'usage', None)
                if usage:
                    trace_metrics["total_input_tokens"] += getattr(usage, 'input', 0) or 0
                    trace_metrics["total_output_tokens"] += getattr(usage, 'output', 0) or 0

                # Thinking tokens might still be in metadata if Langfuse hasn't natively mapped them yet
                trace_metrics["total_thinking_tokens"] += metadata.get("gen_ai.usage.thinking_tokens", 0)

                trace_metrics["total_llm_latency_sec"] += step_latency

                parent_id = getattr(obs, 'parent_observation_id', None)
                if parent_id:
                    turn_latencies[parent_id] = turn_latencies.get(parent_id, 0) + step_latency

            elif span_type == "turn":
                trace_metrics["turn_count"] += 1

            elif span_type == "tool":
                trace_metrics["tool_call_count"] += 1

        # 4. Calculate Turn Averages
        if trace_metrics["turn_count"] > 0:
            trace_metrics["avg_llm_latency_per_turn_sec"] = trace_metrics["total_llm_latency_sec"] / trace_metrics["turn_count"]
        else:
            trace_metrics["avg_llm_latency_per_turn_sec"] = 0.0

        self.results.append(trace_metrics)

    def generate_report(self, export_csv=True):
        """Converts results to a Pandas DataFrame and calculates category groupings."""
        if not self.results:
            print("No data to report.")
            return None

        df = pd.DataFrame(self.results)

        # Ensure success is treated as an integer (0 or 1) for accurate percentage math
        df['success'] = df['success'].astype(int)

        print("\n==================================================")
        print(" GLOBAL BENCHMARK SUMMARY")
        print("==================================================")
        print(f"Total Tests Run: {len(df)}")
        print(f"Global Success:  {(df['success'].mean() * 100):.2f}%")
        print(f"Avg Latency:     {df['total_llm_latency_sec'].mean():.2f}s")
        print(f"Avg Input Tokens:{df['total_input_tokens'].mean():.2f}")

        print("\n==================================================")
        print(" BREAKDOWN BY CATEGORY")
        print("==================================================")

        # Group by the newly extracted category and calculate means
        category_summary = df.groupby('category').agg(
            tests_run=('test_id', 'count'),
            success_rate=('success', lambda x: x.mean() * 100),
            avg_latency=('total_llm_latency_sec', 'mean'),
            avg_input_tokens=('total_input_tokens', 'mean'),
            avg_errors=('error_count', 'mean'),
            avg_tool_calls=('tool_call_count', 'mean')
        ).reset_index()

        # Print a formatted table to the console
        # Pandas to_string() makes it look very clean in the terminal
        print(category_summary.to_string(
            index=False,
            float_format=lambda x: f"{x:.2f}",
            justify='left'
        ))

        if export_csv:
            # Export raw data
            raw_filename = f"custom_metrics/benchmark_metrics_raw_{int(time.time())}.csv"
            df.to_csv(raw_filename, index=False)

            # Export the category summary
            summary_filename = f"custom_metrics/benchmark_metrics_summary_{int(time.time())}.csv"
            category_summary.to_csv(summary_filename, index=False)

            print(f"\n[Export] Raw trace data saved to: {raw_filename}")
            print(f"[Export] Category summary saved to: {summary_filename}")

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

    calculator = MetricsCalculator()

    # traces = calculator.fetch_traces_by_tags(target_tags)
    traces = calculator.fetch_10_traces_by_tags(target_tags)

    for i, trace in enumerate(traces):
        calculator.process_trace(trace)
        if (i + 1) % 50 == 0:
            print(f"Processed {i + 1}/{len(traces)} traces...")

    calculator.generate_report(export_csv=True)
