import os
import argparse
import json

from pyseq.kmer_utils import KmerDb
from pyseq.sequence_io import SequenceFile


USAGE = """pyseq bin_reads [-h] -r REFERENCES -i INPUT -b BINS_JSON [-k KMER_LENGTH] [-m MINIMIZER_LENGTH] [-a AMBIGUITY_THRESHOLD]
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description =
        f"""Create a minimizer-based kmer reference database and write to file.""",
        usage=USAGE,
        formatter_class=lambda prog: argparse.MetavarTypeHelpFormatter(prog, max_help_position=60)
    )
    parser.add_argument(
        "build_db",
        type = str,
        help = argparse.SUPPRESS
    )
    parser.add_argument(
        "-r", "--references",
        type     = str,
        required = True,
        help     = "fasta containing nucleotide reference sequences"
    )
    parser.add_argument(
        "-o", "--output",
        type     = str,
        required = False,
        default  = "database.pyseq.dbi",
        help     = "output database file"
    )
    parser.add_argument(
        "-b", "--bins_json",
        type     = str,
        required = True,
        help     = "JSON file mapping reference sequences to bins"
    )
    parser.add_argument(
        "-k", "--kmer_length",
        type     = int,
        required = False,
        default  = 31,
        help     = "kmer length"
    )
    parser.add_argument(
        "-m", "--minimizer_length",
        type     = int,
        required = False,
        default  = 19,
        help     = "minimizer length"
    )
    parser.add_argument(
        "-a", "--ambiguity_threshold",
        type     = int,
        required = False,
        default  = 2,
        help     = "kmer bin assignment abiguity threshold"
    )
    return parser.parse_args()

def load_bin_json(path):
    """
    Load json file mapping reference sequence names to bins.
    :param path: path to file
    """
    with open(path, "r") as f:
        bins = json.load(f)
    return bins

def main():
    args = parse_args()
    kmer_db = KmerDb(args.kmer_length, args.minimizer_length)
    bins = load_bin_json(args.bins_json)

    db_ref = SequenceFile()
    db_ref.load_sequence_blocks_from_file(args.references)

    kmer_db.build_kmer_database(db_ref, bins, args.ambiguity_threshold)
    kmer_db.write_pyseq_dbi(args.output)

if __name__ == '__main__':
    main()
