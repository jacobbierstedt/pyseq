import os
import math
import json
import zlib

from .kmer_utils import get_minimized_kmers

class SequenceFile: pass
class SequenceBlock: pass


class BinResult(object):
    """docstring for BinResult."""
    def __init__(self, bin_name = None, weighted = 0, unweighted = 0):
        super(BinResult, self).__init__()
        self.bin_name = bin_name
        self.weighted = weighted
        self.unweighted = unweighted

    def to_dict(self) -> dict:
        return {"weighted" : self.weighted, "unweighted" : self.unweighted}

    def __str__(self):
        return json.dumps(self.__dict__)


class KmerDb(object):
    """
    Class to create a kmer database from reference sequences associated with
    bins and facilitate the querying and binning of query sequences.
    :param kmer_length: length of kmer
    :param minimizer_length: length of minimizer
    :param max_ambiguous: maximimum number of ambiguous nucleotides for a kmer to be considered
    """
    def __init__(self, kmer_length, minimizer_length, max_ambiguous = 0.2):
        super(KmerDb, self).__init__()
        self.kmer_length      = kmer_length
        self.minimizer_length = minimizer_length
        self.max_ambiguous    = max_ambiguous
        self.references       = {}
        self.bin_counts       = {}
        self.kmers            = {}
        self.weighted_kmers   = {}

    def build_kmer_database(self,
        reference     : SequenceFile,
        bins          : dict,
        bin_threshold : int):
        """
        Create kmer database from reference sequences.
        :param reference: SequenceBlock containing nucleotide references
        :param bins: dict to map reference seq names to bins, name -> {bin_name}
        :param bin_threshold: maximum number of bins a valid kmer can be assigned to
        """
        for block in reference.sequence_blocks:
            self.add_references(block, bins)
        self.finialize_database(bin_threshold)

    def write_pyseq_dbi(self, output_path:str):
        """
        Write finished database to a file.
        :param output_path: path to write database file
        """
        db = ""
        for minimizer, bins in self.kmers.items():
            info = {
                "kmer" : minimizer,
                "bins" : [{"bin_id" : bin_id, "n" : bin_result.unweighted} for bin_id, bin_result in bins.items()]
            }
            db += f"{json.dumps(info)}\n"
        cmp = zlib.compress(db.encode(), 3)
        with open(output_path, "wb") as f:
            f.write(cmp)

    def load_pyseq_dbi(self, database_path: str):
        """
        Load existing pyseq database from file.
        :param database_path: path to existing database
        """
        with open(database_path, "rb") as f:
            buf = f.read()
        data = zlib.decompress(buf).decode()
        for line in data.split("\n"):
            if len(line) > 2:
                info = json.loads(line)
                kmer = info["kmer"]
                bins = info["bins"]
                self.kmers.setdefault(kmer, {})
                for bin in bins:
                    self.kmers[kmer].setdefault(bin["bin_id"], BinResult(bin_name = bin["bin_id"]))
                    self.kmers[kmer][bin["bin_id"]].unweighted = bin["n"]

    def add_references(self, reference: SequenceBlock, bins: dict):
        """
        Add all reference sequences in block of sequences to database.
        :param reference: SequenceBlock containing nucleotide references
        :param bins: dict to map reference seq names to bins, name -> {bin_name}
        """
        for sequence in reference.sequences:
            bin_id = bins.get(sequence.name)
            if bin_id is not None:
                self.add_sequence_to_db(bin_id, sequence.sequence)

    def add_sequence_to_db(self, bin_id: str, sequence: str):
        """
        Kmerize reference sequence and add to database.
        :param bin_id: name of bin sequence belongs to
        :param sequence: nucleotide reference sequence string
        """
        minimized_kmers = get_minimized_kmers(sequence, self.kmer_length, self.minimizer_length, self.max_ambiguous)
        for minimizer, kmer_count in minimized_kmers.items():
            self.bin_counts.setdefault(bin_id, 0)
            self.bin_counts[bin_id] += kmer_count
            self.kmers.setdefault(minimizer, {})
            self.kmers[minimizer].setdefault(bin_id, BinResult(bin_name = bin_id))
            self.kmers[minimizer][bin_id].unweighted += kmer_count

    def finialize_database(self, bin_threshold: int):
        """
        Set kmers occurring in multiple bins to ambiguous bin. [WIP]
        :param bin_threshold: maximum number of bins a valid kmer can be assigned to
        """
        for kmer, bins in self.kmers.items():
            if len(bins.keys()) > bin_threshold:
                self.kmers[kmer].setdefault("ambiguous", BinResult(bin_name = "ambiguous"))
                for bin, count in bins.items():
                    if bin != "ambiguous":
                        self.kmers[kmer]["ambiguous"].unweighted += count.unweighted
                        self.kmers[kmer][bin].unweighted = 0

    def query_sequence(self, sequence: str) -> dict:
        """
        Query sequence kmers against database and return weighted and unweighted
        counts for each bin.
        :param sequence: nucloetide sequence string
        :return results: dict containing bin results, bin -> {BinResult}
        """
        minimized_kmers = get_minimized_kmers(sequence, self.kmer_length, self.minimizer_length, self.max_ambiguous)
        results = {}
        for minimizer, kmer_count in minimized_kmers.items():
            res = self.kmers.get(minimizer, {})
            for bin_id, counts in res.items():
                results.setdefault(bin_id, BinResult(bin_name = bin_id))
                results[bin_id].unweighted += kmer_count
                results[bin_id].weighted += kmer_count / len(res.keys())
        return results

    def assign_sequence_to_bin(self, kmer_counts: dict) -> str:
        """
        Assign read to in using weighted kmer counts.
        :param kmer_counts: dict containing bin results for seqence. bin -> {BinResult}
        """
        bin_w = {}
        for bin, kmer_count in kmer_counts.items():
            bin_w.update({bin : kmer_count.weighted})
        if len(bin_w) > 0:
            best_bin = max(bin_w, key=bin_w.get)
            return best_bin
        else:
            return None

    def bin_reads(self, block : SequenceBlock) -> dict:
        """
        Assign reads to database bins.
        :param block: SequenceBlock containing reads to bin
        """
        read_results = {}
        for sequence in block.sequences:
            kmer_counts = self.query_sequence(sequence.sequence)
            bin = self.assign_sequence_to_bin(kmer_counts)
            result = {
                "assigned_bin" : bin,
                "kmer_counts" : {}
            }
            for bin, bin_result in kmer_counts.items():
                result["kmer_counts"].update({bin : bin_result.to_dict()})
            read_results.update({sequence.name : result})
        return read_results
