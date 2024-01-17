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
        f"""Bin reads against a minimizer-based kmer reference database.""",
        usage=USAGE,
        formatter_class=lambda prog: argparse.MetavarTypeHelpFormatter(prog, max_help_position=60)
    )
    parser.add_argument(
        "bin_reads",
        type = str,
        help = argparse.SUPPRESS
    )
    parser.add_argument(
        "-d", "--database",
        type     = str,
        required = False,
        help     = "Path to pyseq kmer db"
    )
    parser.add_argument(
        "-r", "--references",
        type     = str,
        required = False,
        help     = "Fasta containing nucleotide reference sequences"
    )
    parser.add_argument(
        "-i", "--input",
        type     = str,
        required = True,
        help     = "Input reads fastq/a format"
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
    parser.add_argument(
        "-o", "--output_file",
        type     = str,
        required = False,
        default  = "binned_reads.json",
        help     = "Output json file with binned reads"
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


def write_output_file(info, path):
    with open(path, "w") as f:
        json.dump(info, f)


def main():
    args = parse_args()
    kmer_db = KmerDb(args.kmer_length, args.minimizer_length)
    bins = load_bin_json(args.bins_json)

    if args.database:
        kmer_db.load_pyseq_dbi(args.database)
    else:
        db_ref = SequenceFile()
        db_ref.load_sequence_blocks_from_file(args.references)
        kmer_db.build_kmer_database(db_ref, bins, args.ambiguity_threshold)

    query_seqs = SequenceFile()
    query_seqs.load_sequence_blocks_from_file(args.input)

    results = {}
    for block in query_seqs.sequence_blocks:
        block_results = kmer_db.bin_reads(block)
        results.update(block_results)

    write_output_file(results, args.output_file)


if __name__ == '__main__':
    main()
