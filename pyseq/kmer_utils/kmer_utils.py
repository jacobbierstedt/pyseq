import os
import sys
import math




NT_ALPHABET = {
    "A" : "T",
    "T" : "A",
    "G" : "C",
    "C" : "G",
    "N" : "N",
    "a" : "t",
    "t" : "a",
    "g" : "c",
    "c" : "g",
    "n" : "n",
}


def reverse_complement(sequence: str) -> str:
    """
    Compute the reverse complement of given sequence.
    :param sequence: nucleotide sequence
    """
    rc = []
    for base in reversed(sequence):
        rc.append(NT_ALPHABET.get(base, "N"))
    return "".join(rc)


def get_kmers(sequence: str, kmer_length: int) -> list:
    """
    Get all kmers of fixed length from sequence.
    :param sequence: nuclotide or AA sequence string
    :param kmer_length: length of kmers
    """
    seq_length  = len(sequence)
    sequence_rc = reverse_complement(sequence)
    i     = 0
    kmers = []
    while i < (seq_length - kmer_length + 1):
        kmer = sequence[i : (i + kmer_length)]
        rev_kmer = sequence_rc[(seq_length - kmer_length - i) : (seq_length - i)]
        kmers.append(kmer)
        kmers.append(rev_kmer)
        i += 1
    return kmers


def get_kmer_minimizer(kmer: str, rev_kmer: str, minimizer_length) -> str:
    """
    Get kmer minimizer
    """
    min = chr(sys.maxunicode)
    for i in range(0, len(kmer) - minimizer_length + 1):
        sub_kmer = kmer[i : i + minimizer_length]
        if sub_kmer < min:
            min = sub_kmer
        sub_r = rev_kmer[i : i + minimizer_length]
        if sub_r < min:
            min = sub_r
    return min


def get_minimized_kmers(
    sequence         : str,
    kmer_length      : int,
    minimizer_length : int,
    max_ambiguous    : float
    ) -> dict:
    """
    Get a map of minimizers to kmer counts from sequence.
    :param sequence: nucleotide sequence string
    :param kmer_length: length of kmers
    :param minimizer_length: length of minimizers
    """
    seq_length = len(sequence)
    sequence_rc = reverse_complement(sequence)
    i = 0
    minimized = {}
    while i < (seq_length - kmer_length + 1):
        kmer      = sequence[i : (i + kmer_length)]
        if apply_ambiguous_threshold(kmer, max_ambiguous) == False:
            i += 1
            continue
        rev_kmer  = sequence_rc[(seq_length - kmer_length - i) : (seq_length - i)]
        if apply_ambiguous_threshold(rev_kmer, max_ambiguous) == False:
            i += 1
            continue
        minimizer = get_kmer_minimizer(kmer, rev_kmer, minimizer_length)
        minimized.setdefault(minimizer, 0)
        minimized[minimizer] += 1
        i += 1
    return minimized


def query_seq_against_reference(
    query            : str,
    reference        : str,
    kmer_length      : int,
    minimizer_length : int
    ) -> int:
    """
    Get number of kmer matches between reference sequence and query sequence
    using a minimizer-based approach.
    :param query: sequence to search
    :param reference: sequence to serve as database
    :param kmer_length: length of kmer
    :param minimizer_length: length of minimizer
    """
    ref_kmers  = get_minimized_kmers(reference, kmer_length, minimizer_length)
    query_kmers = get_minimized_kmers(query, kmer_length, minimizer_length)
    matches = 0
    for kmer, n in query_kmers.items():
        if kmer in ref_kmers.keys():
            matches += n
    return matches


def query_seq_against_reference_no_minimizer(
    query            : str,
    reference        : str,
    kmer_length      : int
    ) -> int:
    """
    Get the number of kmer matches between reference sequence and query
    sequence using direct kmer matching.
    """
    ref_kmers   = get_kmers(reference, kmer_length)
    query_kmers = get_kmers(query, kmer_length)
    matches = 0
    for qk in query_kmers:
        if qk in ref_kmers:
            matches += 1
    return matches / 2


def apply_ambiguous_threshold(kmer: str, max_ambiguous: float) -> bool:
    """
    """
    fraction_ambiguous = kmer.count("N") / len(kmer)
    if fraction_ambiguous > max_ambiguous:
        return False
    else:
        return True
