import os
import sys
import gzip

from .sequence_block import SequenceBlock, SequenceRead
from .sequence_io_utils import is_gz_file, is_fastq, is_fasta

class SequenceFile(object):
    """
    Class for fastq/a IO.
    """
    def __init__(self):
        super(SequenceFile, self).__init__()
        self.sequence_blocks = []

    def load_single_sequence_block(self, file : str):
        """
        Read entire contents of provided file into a single sequence block
        :param file: path to input fasta or fastq file
        """
        f = self._open(file)
        seq_data = f.read()
        block = SequenceBlock()
        block.add_sequence_block_from_str(seq_data)
        self.sequence_blocks.append(block)
        f.close()

    def load_sequence_blocks_from_file(self,
        file       : str,
        chunksize  : int = 1000000,
        max_chunks : int = 20):
        """
        Load a sequence file in chunks.
        :param chunksize: number of reads per chunk
        :param max_chunks: maximum number of chunks
        """
        # Parse fastq/a file
        f = self._open(file)
        reads = []
        line = f.readline()
        while len(line) > 0:
            if is_fasta(line[0]):
                read = SequenceRead(name = line.strip().replace(">", ""))
                line = f.readline().strip()
                while len(line) > 0 and not is_fasta(line[0]):
                    read.sequence += line.strip()
                    line = f.readline().strip()
                read.set_default_quality()
                reads.append(read)
            elif is_fastq(line[0]):
                fq = line
                for i in range(0, 3):
                    fq += f.readline()
                read = SequenceRead()
                read.from_fastq_string(fq)
                reads.append(read)
                line = f.readline()
        f.close()
        # Get chunk parameters
        n_chunks = int(len(reads) / chunksize) + 1
        if n_chunks > max_chunks:
            n_chunks = max_chunks
            chunksize = int(len(reads) / n_chunks) + 1
        if chunksize >= len(reads):
            chunksize = len(reads)
            n_chunks = 1
        # Split reads into chunks
        chunks = []
        for i in range(0, n_chunks):
            block = SequenceBlock()
            block_start = i * chunksize
            block_end   = i * chunksize + chunksize
            if block_end >= len(reads):
                block_end = len(reads)
            for j in range(block_start, block_end):
                block.sequences.append(reads[j])
            self.sequence_blocks.append(block)

    def _open(self, input_file):
        """
        Open file object for reading.
        :param input_file: path to file
        """
        if is_gz_file(input_file):
            f = gzip.open(input_file, "rt")
        else:
            f = open(input_file, "r")
        return f
