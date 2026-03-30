import os
import time
import requests
import json
import sys  # Import sys to kill the process
from bfcl_eval.model_handler.base_handler import BaseHandler
from bfcl_eval.model_handler.utils import (
    convert_to_function_call,
    extract_system_prompt,
    system_prompt_pre_processing_chat_model,
)

class ToolmanHandler(BaseHandler):
    def __init__(self, model_name, temperature, registry_name, is_fc_model, **kwargs):
        super().__init__(model_name, temperature, registry_name, is_fc_model, **kwargs)
        self.go_endpoint = "http://localhost:8080/bfcl"
        self.is_fc_model = True

        # Handle 'enable_ptc' (Convert string "True"/"False" to boolean)
        env_ptc = os.getenv("TOOLMAN_ENABLE_PTC")
        if env_ptc is not None:
            self.enable_ptc = (env_ptc.lower() == "true")
        else:
            self.enable_ptc = kwargs.get("enable_ptc", True) # Default

        # Handle 'bellman_model'
        self.bellman_model = os.getenv(
            "TOOLMAN_BELLMAN_MODEL",
            kwargs.get("bellman_model", "OpenAI/gpt-4o-mini")
        )

    def _query_FC(self, inference_data: dict):
        payload = {
            "messages": inference_data["message"],
            "new_tool_responses": inference_data["new_tool_responses"],
            "toolman_history": inference_data["toolman_history"],
            "tools": inference_data["tools"],
            "temperature": self.temperature,
            "system_prompt": inference_data.get("system_prompt", ""),
            "enable_ptc": self.enable_ptc,
            "bellman_model": self.bellman_model,
            "test_entry_id": inference_data["test_entry_id"]
        }

        start = time.time()
        try:
            response = requests.post(self.go_endpoint, json=payload)
            response.raise_for_status()
            return response.json(), time.time() - start

        except Exception as e:
            # Force exit to stop testing: This bypasses BFCL's internal error catching
            print(f"\n[FATAL] Toolman Connection Error: {e}")
            # print("[FATAL] The Go server likely crashed. Retrying...")
            print("[FATAL] The Go server likely crashed. Stopping benchmark immediately.")
            # sys.exit(1)


    def _pre_query_processing_FC(self, inference_data, test_entry):
        if "message" not in inference_data:
            inference_data["message"] = []
        if "toolman_history" not in inference_data:
            inference_data["toolman_history"] = []
        if "new_tool_responses" not in inference_data:
            inference_data["new_tool_responses"] = []

        functions: list = test_entry["function"]
        if self.enable_ptc: # replace tool list in system prompt for ptc
            functions = ["{ 'code_execution' }"]
        test_entry_id: str = test_entry["id"]
        test_entry["question"][0] = system_prompt_pre_processing_chat_model(
            test_entry["question"][0], functions, test_entry_id
        )
        inference_data["system_prompt"] = extract_system_prompt(test_entry["question"][0])
        # if system_prompt:
        #     inference_data["system_prompt"] = system_prompt

        # add test id to inference data
        inference_data["test_entry_id"] = test_entry_id

        return inference_data

    def _compile_tools(self, inference_data, test_entry):
        inference_data["tools"] = test_entry.get("function", [])
        return inference_data

    def _parse_query_response_FC(self, api_response):
        # Retrieve the List of Dictionaries from Go
        # e.g. [{"calculate_area": {"base": 10}}]
        model_responses = api_response.get("tool_calls", [])
        tool_call_ids = api_response.get("tool_call_ids", [])
        toolman_history = api_response.get("toolman_history", [])
        history_parts = []
        tool_call_func_names = []

        iterable_responses = model_responses if isinstance(model_responses, list) else [model_responses]

        for resp in iterable_responses:
            if isinstance(resp, dict):
                # Handle {"func_name": {"arg": val}}
                for name, args in resp.items():
                    # Convert args to "key=repr(val)"
                    # repr() handles quotes automatically: dir='temp', count=5
                    arg_str = ", ".join([f"{k}={repr(v)}" for k, v in args.items()])
                    history_parts.append(f"{name}({arg_str})")
                    tool_call_func_names.append(name)
            elif isinstance(resp, str):
                # Fallback if it's already a string
                history_parts.append(resp)
                tool_call_func_names.append("unknown")
            else:
                history_parts.append(str(resp))
                tool_call_func_names.append("unknown")

        # Join multiple calls with a semicolon (BFCL standard)
        content = "; ".join(history_parts)

        # Create History Log String (Safe JSON dump)
        # if isinstance(model_tool_calls, list) and len(model_tool_calls) > 0:
        #     content = json.dumps(model_tool_calls)
        # else:
        #     content = str(model_tool_calls)
        #
        # model_responses = model_tool_calls if model_tool_calls else text_parts

        return {
            "model_responses": model_responses, # {"func_name": {"arg": val}} for BFCL
            "model_responses_message_for_chat_history": {"role": "function-call", "content": content}, #TODO: remove
            "tool_call_ids": tool_call_ids,
            "tool_call_func_names": tool_call_func_names,
            "toolman_history": toolman_history,
            "input_token": api_response.get("input_tokens", 0),
            "output_token": api_response.get("output_tokens", 0)
        }

    def _add_execution_results_FC(self, inference_data, execution_results, model_response_data):
        # reset new tool responses (then add new ones)
        inference_data["new_tool_responses"] = []

        if execution_results and model_response_data["tool_call_ids"] and model_response_data["tool_call_func_names"]:
            if len(execution_results) != len(model_response_data["tool_call_ids"]) or len(execution_results) != len(model_response_data["tool_call_func_names"]):
                print("Incompatible execution results!! ")
            for execution_result, tool_id, tool_name in zip(
                    execution_results, model_response_data["tool_call_ids"], model_response_data["tool_call_func_names"]
            ):
                inference_data["message"].append({"role": "tool_response", "content": str(execution_result), "tool_call_id": tool_id, "tool_name": tool_name})
                inference_data["new_tool_responses"].append({"role": "tool_response", "content": str(execution_result), "tool_call_id": tool_id, "tool_name": tool_name})
        else:
            print("something went wrong...")
            print("execution_results: ", execution_results)
            print("tool_call_ids: ", model_response_data["tool_call_ids"])

        # add toolman conversation history
        inference_data["toolman_history"] = model_response_data["toolman_history"]

        return inference_data

    def decode_ast(self, result, language="Python", has_tool_call_tag=False):
        """
        Expects: List of Dicts [{"func": {args}}]
        Returns: List of Dicts (Pass-through for AST evaluation)
        """
        if not isinstance(result, list):
            result = [result]
        return result

    def decode_execute(self, result, has_tool_call_tag=False):
        """
        Expects: List of Dicts [{"func": {args}}]
        Returns: List of Strings ["func(a=1)"] (For Execution)
        """
        # return convert_to_function_call(result)
        func_call_list = []
        if not isinstance(result, list):
            result = [result]

        for function_call in result:
            # if not function call --> skip
            if not isinstance(function_call, dict):
                continue
            # function_call is {"func_name": {"arg": val}}
            # if isinstance(function_call, dict):
            try:
                for func_name, func_args in function_call.items():
                    # Handle cases where args might be None
                    if func_args is None:
                        func_args = {}

                    # specific fix for 'items' if func_args is somehow a string (double encoded JSON)
                    if isinstance(func_args, str):
                        # skip or try to json.loads(func_args) if you suspect double encoding
                        continue

                    args_str = ",".join([f"{k}={repr(v)}" for k, v in func_args.items()])
                    func_call_list.append(f"{func_name}({args_str})")
            except Exception as e:
                print(f"[Warning] decode_execute failed on item: {function_call} - {e}")
                continue

        return func_call_list

    def add_first_turn_message_FC(self, inference_data, first_turn_message):
        for msg in first_turn_message: inference_data["message"].append(msg)
        return inference_data

    def _add_next_turn_user_message_FC(self, inference_data, user_message):
        for msg in user_message: inference_data["message"].append(msg)
        return inference_data

    def _add_assistant_message_FC(self, inference_data, model_response_data):
        inference_data["message"].append(model_response_data["model_responses_message_for_chat_history"])
        # Fix: clear new_tool_responses every turn - responses are added later
        inference_data["new_tool_responses"] = []
        # fix: update the toolman hist in inference data (otherwise lost for next turn)
        inference_data["toolman_history"] = model_response_data["toolman_history"]
        return inference_data