import sys
import os
from bfcl_eval import llm_response_generation
from bfcl_eval.constants import model_config
from bfcl_eval.model_handler.toolman_handler import ToolmanHandler

### How to use:
# 1. run 'run_benchmark.py'
# 2. run in terminal 'bfcl evaluate --model toolman-go --partial-eval --test-category simple_python'

# --- CONFIGURATION ---
RUN_CONFIG = {
    "model": ["toolman-go-ptc"],              # BFCL expects a list of models
    #"test_category": ["multi_turn"],
    "test_category": ["multi_turn_base"], # BFCL expects a list of categories
    #"test_category": ["single_turn"], # BFCL expects a list of categories
    #"test_category": ["simple_python"], # BFCL expects a list of categories
    #"test_category": ["simple_java"], # BFCL expects a list of categories
    #"test_category": ["multiple"], # BFCL expects a list of categories
    #"test_category": ["multi_turn_long_context"], # BFCL expects a list of categories
    "enable_ptc": True,
    "bellman_model": "OpenAI/gpt-4o-mini",
    "temperature": 0.001,               # BFCL default is often 0.001
    "num_threads": 1,
    "num_gpus": 1,
    "gpu_memory_utilization": 0.9,
    "backend": "vllm",
    "include_input_log": True,
    "allow_overwrite": True,
    "run_ids": False                    # Run all tests in category
}

# --- ROBUST MOCK ARGUMENTS ---
class MockArgs:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getattr__(self, item):
        return None

# --- CUSTOM WRAPPER TO INJECT ARGS ---
class ToolmanWrapper(ToolmanHandler):
    def __init__(self, model_name, temperature, registry_name, is_fc_model, **kwargs):
        # Inject our custom config into the handler
        kwargs["enable_ptc"] = RUN_CONFIG["enable_ptc"]
        kwargs["bellman_model"] = RUN_CONFIG["bellman_model"]
        super().__init__(model_name, temperature, registry_name, is_fc_model, **kwargs)

def run_evaluation():
    print(f"🚀 Starting Benchmark: {RUN_CONFIG['model'][0]} (PTC={RUN_CONFIG['enable_ptc']})")

    os.environ["TOOLMAN_ENABLE_PTC"] = str(RUN_CONFIG["enable_ptc"])
    os.environ["TOOLMAN_BELLMAN_MODEL"] = RUN_CONFIG["bellman_model"]

    if RUN_CONFIG["enable_ptc"] == True:
        RUN_CONFIG["model"] = ["toolman-go-ptc"]

    # 1. Create the robust arguments object
    args = MockArgs(**RUN_CONFIG)

    # 2. Run the generation
    llm_response_generation.main(args)

if __name__ == "__main__":
    run_evaluation()