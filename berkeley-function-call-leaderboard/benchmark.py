import sys
import os
from bfcl_eval import llm_response_generation
from bfcl_eval.constants import model_config
from bfcl_eval.model_handler.toolman_handler import ToolmanHandler

### How to use:
# 1. run 'benchmark.py'
# 2. run in terminal 'bfcl evaluate --model toolman-go --partial-eval'

# --- CONFIGURATION ---
RUN_CONFIG = {
    "model": ["toolman-go"], # BFCL expects a list of models
    #"test_category": ["multi_turn"], # All multi-turn
    "test_category": ["multi_turn_base"],
    #"test_category": ["single_turn"], # all single-turn
    #"test_category": ["simple_python", "simple_javascript", "simple_java"], # non-live simple
    #"test_category": ["parallel", "parallel_multiple", "live_parallel", "live_parallel_multiple"], # We skip parallel tests as execution replay is not supported for these
    #"test_category": ["memory_kv", "memory_vector", "memory_rec_sum", "web_search_base", "web_search_no_snippet", "format_sensitivity"], # We skip agentic tests as these test model reasoning capabilities more than tool-calling
    #"test_category": ["format_sensitivity"], # We skip format sensitivity as this is not a "prompting" model
    # "test_category": ["simple_python",
    #                   "simple_java",
    #                   "simple_javascript",
    #                   "multiple",
    #                   "irrelevance",
    #                   "live_simple",
    #                   "live_multiple",
    #                   "live_irrelevance",
    #                   "live_relevance",
    #                   "multi_turn_base",
    #                   "multi_turn_miss_func",
    #                   "multi_turn_miss_param",
    #                   "multi_turn_long_context",
    #                   ],
    "enable_ptc": False,
    # "bellman_model": "OpenAI/gpt-5-mini-2025-08-07",
    "bellman_model": "vLLM/google/gemma-4-E4B-it",
    "temperature": None,
    "thinking": None,
    "num_threads": 200,
}

class MockArgs:
    """ robust mock args """
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getattr__(self, item):
        return None

class ToolmanWrapper(ToolmanHandler):
    """ custom wrapper to inject args """
    def __init__(self, model_name, temperature, registry_name, is_fc_model, **kwargs):
        # inject custom config into the handler
        kwargs["enable_ptc"] = RUN_CONFIG["enable_ptc"]
        kwargs["bellman_model"] = RUN_CONFIG["bellman_model"]
        kwargs["thinking"] = RUN_CONFIG["thinking"]
        super().__init__(model_name, temperature, registry_name, is_fc_model, **kwargs)

def run_benchmark():
    """ run benchmark  """
    # configure custom args
    os.environ["TOOLMAN_ENABLE_PTC"] = str(RUN_CONFIG["enable_ptc"])
    os.environ["TOOLMAN_BELLMAN_MODEL"] = RUN_CONFIG["bellman_model"]

    if RUN_CONFIG["thinking"]:
        os.environ["TOOLMAN_THINKING"] = str(RUN_CONFIG["thinking"])

    if RUN_CONFIG["enable_ptc"] == True:
        RUN_CONFIG["model"] = ["toolman-go-ptc"]

    ptc_flag = "ptc-fc" if RUN_CONFIG["enable_ptc"] else "regular-fc"
    bellman_model = RUN_CONFIG["bellman_model"]
    RUN_CONFIG["model"] = f"{ptc_flag}-{bellman_model}"

    print(f"Starting Benchmark: {RUN_CONFIG['model'][0]} (PTC={RUN_CONFIG['enable_ptc']}, Thinking={RUN_CONFIG['thinking']})")

    # create the robust arguments object
    args = MockArgs(**RUN_CONFIG)

    # run the generation
    llm_response_generation.main(args)

if __name__ == "__main__":
    run_benchmark()