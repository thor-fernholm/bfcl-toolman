from langfuse import Langfuse
from pathlib import Path
from dotenv import load_dotenv
import os
import time

root_env_path = Path(__file__).resolve().parents[2] / ".env"
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

def score_langfuse_trace(test_id, model_name, success):
    """
    Attach per-test scores to an existing Langfuse trace.
    """
    trace_id = get_trace_id_by_tags(test_id, model_name)

    if not trace_id:
        print(f"[Langfuse scoring error] Trace not found for test_id={test_id}, model={model_name}")
        return

    try:
        langfuse.create_score(
            trace_id=trace_id,
            name="success",
            value=success,
            data_type="BOOLEAN",
        )
    except Exception as e:
        print(f"[Langfuse scoring error] trace_id={trace_id}: {e}")

def get_trace_id_by_tags(test_id, model_name, retries=3, sleep_seconds=0.01):
    """
    Look up the Langfuse trace by tag and return its trace_id.
    """
    tags = make_trace_tags(test_id, model_name)
    # print("tags:", tags)
    for attempt in range(retries):
        try:
            traces = langfuse.api.trace.list(
                # page=1,
                limit=10,
                tags=tags,
            ).data

            if traces:
                # should normally be unique; take first match
                return traces[0].id

        except Exception as e:
            print(f"[Langfuse lookup error] {tags}: {e}")

        if attempt < retries - 1:
            time.sleep(sleep_seconds)

    return None


def make_trace_tags(test_id, model_name):
    # model_name = f"{ptc_flag}-{bellman_model}"
    ptc_flag = "ptc-fc" if "ptc-fc" in model_name else "regular-fc"
    bellman_model = model_name.replace(f"{ptc_flag}-", "").replace("_","/")

    return [
        test_id,
        ptc_flag,
        bellman_model,
    ]