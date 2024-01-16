import os
import argparse
import json

# from pyseq import kmer_utils
from pyseq.kmer_utils import KmerDb
from pyseq.sequence_io import SequenceFile

USAGE = """pyseq bin_reads [-h] -r REFERENCES -i INPUT -b BINS_JSON [-k KMER_LENGTH] [-m MINIMIZER_LENGTH] [-a AMBIGUITY_THRESHOLD]
"""

def parse_args():
    parser = argparse.ArgumentParser(
        description =
        f"""Create a minimizer-based kmer reference database and bin reads against it""",
        usage=USAGE,
        formatter_class = argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "bin_reads",
        type = str
    )
    parser.add_argument(
        "-r", "--references",
        type     = str,
        required = True,
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

    db_ref = SequenceFile()
    db_ref.load_sequence_blocks_from_file(args.references)

    query_seqs = SequenceFile()
    query_seqs.load_sequence_blocks_from_file(args.input)

    kmer_db.build_kmer_database(db_ref, bins, args.ambiguity_threshold)

    results = {}
    for block in query_seqs.sequence_blocks:
        block_results = kmer_db.bin_reads(block)
        results.update(block_results)

    write_output_file(results, args.output_file)




if __name__ == '__main__':
    main()
