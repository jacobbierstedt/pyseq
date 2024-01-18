import os
import json


class Jsonl(object):
    """
    Class for jsonl file parsing.
    """
    def __init__(self):
        super(Jsonl, self).__init__()
        self.info = []

    def load_jsonl_file(self, path: str):
        """
        Load jsonl file from path.
        :param path: path to jsonl file
        """
        with open(path, "r") as f:
            for line in f:
                self.info.append(json.loads(line))

    def write_jsonl_file(self, output_path: str):
        """
        Write jsonl file to path
        :param output_path: path to write jsonl file
        """
        with open(output_path, "w") as f:
            for d in self.info:
                f.write(f"{json.dumps(d)}\n")
