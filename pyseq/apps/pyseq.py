import os
import sys
import argparse
import pyseq
from pyseq.apps.pyseq_bin_reads import main
from pyseq.apps.pyseq_build_db import main


SUBCOMMANDS = {
    "bin_reads" : pyseq.apps.pyseq_bin_reads.main,
    "build_db"  : pyseq.apps.pyseq_build_db.main
}

USAGE = """Usage: pyseq <subcommand> <subcommand_arguments>

Available subcommands:
build_db     | Create a minimizer-based kmer reference database and write to file
bin_reads    | Bin reads against a minimizer-based kmer reference database
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
