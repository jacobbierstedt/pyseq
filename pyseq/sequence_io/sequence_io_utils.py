import os
import gzip


def is_gz_file(filepath):
    with open(filepath, 'rb') as test_f:
        return test_f.read(2) == b'\x1f\x8b'

def is_fastq(char : chr):
    return char == "@"

def is_fasta(char : chr):
    return char == ">"
