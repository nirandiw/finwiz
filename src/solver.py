from functools import lru_cache
from typing import Any
import json
from pathlib import Path
import os

DATA_PATH = Path(os.getenv("DATA_PATH", "data/convfinqa_dataset.json"))


@lru_cache(maxsize=1)
def _records() -> dict[str, dict[str, Any]]:
    """Every record keyed by id. Cached: the file is 21MB."""
    data = json.loads(DATA_PATH.read_text())
    return {record["id"]: record for split in data.values() for record in split}
 
 
def get_doc(record_id: str) -> tuple[str, str, Table]:
    """Return (pre_text, post_text, table) for one record.
 
    Only doc is returned. The record also holds dialogue, with gold programs
    and answers, which must never reach the prompt.
    """
    records = _records()
    if record_id not in records:
        raise KeyError(f"No record with id {record_id!r}")
    doc = records[record_id]["doc"]
    return doc["pre_text"], doc["post_text"], doc["table"]


def solver(question, history, record_id):
    """
    A simple solver function that takes a question, history, and record_id
    and returns a response. This is a placeholder for the actual implementation.
    """

    dsl_answer = "subtract(206588, 181001), divide(#0, 181001)"
    return dsl_answer
