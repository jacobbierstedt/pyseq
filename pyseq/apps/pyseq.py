import os
import sys
import argparse
import pyseq
from pyseq.apps.pyseq_bin_reads import main


SUBCOMMANDS = {
    "bin_reads" : pyseq.apps.pyseq_bin_reads.main
}

USAGE = """Usage: pyseq <subcommand>

Available subcommands:
build_db     |  Create kmer database from reference sequences and store in file
bin_reads    |  Create kmer database from reference sequence and search reads
"""


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        exit()
    subcommand = sys.argv[1]
    if any([subcommand == i for i in ["-h", "--help"]]):
        print(USAGE)
        exit()
    if subcommand not in SUBCOMMANDS:
        print(f"Invalid option: {subcommand}")
        print(USAGE)
        exit(1)

    _main = SUBCOMMANDS[subcommand]
    _main()


if __name__ == '__main__':
    main()
