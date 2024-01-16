import os

from .sequence_block import SequenceBlock

class SequenceFile(object):
    """docstring for SequenceFile."""

    def __init__(self):
        super(SequenceFile, self).__init__()
        self.sequence_blocks = []

    def load_sequence_blocks_from_file(self, file, chunks = 4):
        """
        """
        with open(file, "r") as f:
            seq_data = f.read()
            block = SequenceBlock()
            block.add_sequence_block(seq_data)
            self.sequence_blocks.append(block)
