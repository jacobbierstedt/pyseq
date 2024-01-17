import os
import json
import pytest

from pyseq.formats.jsonl import Jsonl

def test_jsonl():
    data = [
        {
        "field1" : 3,
        "field2" : "value2",
        },
        {
        "field1" : 123,
        "field2" : "value5"
        }
    ]

    with open("tmp.jsonl", "w") as f:
        for d in data:
            f.write(f"{json.dumps(d)}\n")

    jsonl = Jsonl()
    jsonl.load_jsonl_file("tmp.jsonl")
    assert jsonl.info == data
    os.remove("tmp.jsonl")
