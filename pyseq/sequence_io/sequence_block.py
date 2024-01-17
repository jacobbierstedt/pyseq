import os




class SequenceRead(object):
    """
    Class to handle data associated with a nucleotide or amino acid sequence.
    :param sequence: DNA sequence string
    :param quality_scores: Fastq quality score string
    :param comment: Fastq comment string
    :param name: Name of sequence
    """
    DEFAULT_QUALITY = "I"
    ALPHABET = {
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
    def __init__(self,
        sequence       = "",
        quality_scores = "",
        comment        = "+",
        name           = ""):
        super(SequenceRead, self).__init__()
        self.sequence        = self.check_sequence(sequence.strip())
        self.quality_scores  = quality_scores.strip()
        self.comment         = comment.strip()
        self.name            = name.replace(">", "").replace("@", "")

        # Set default quality scores if absent or invalid
        self.set_default_quality()

    def set_default_quality(self):
        """
        Set default quality if quality information is absent or invalid
        """
        if len(self.quality_scores) != len(self.sequence):
            self.quality_scores = self.DEFAULT_QUALITY * len(self.sequence)

    def from_fastq_string(self, read: str):
        """
        Instantiate object from four lines of a fastq file.
        :param read: string containing fastq read
        """
        read = read.strip().split("\n")
        self.name           = read[0].replace("@", "")
        self.sequence       = read[1]
        self.comment        = read[2]
        self.quality_scores = read[3]

    @staticmethod
    def check_sequence(sequence: str) -> str:
        """
        Check sequence against alphabet and replace ambiguous baes
        :param sequence: nucleotide sequence
        """
        seq = []
        for base in sequence:
            if base in SequenceRead.ALPHABET.keys():
                seq.append(base)
            else:
                seq.append("N")
        return "".join(seq)

    def __str__(self):
            return f"@{self.name}\n{self.sequence}\n{self.comment}\n{self.quality_scores}"


class SequenceBlock(object):
    """
    Class to handle a block of sequence data.
    """
    def __init__(self):
        super(SequenceBlock, self).__init__()
        self.sequences       = []
        self.seq_buf         = ""
        self.is_fastq        = False
        self.invalid_reads   = 0
        self.kmer_count      = 0
        self.minimized_kmers = {}

    def add_sequence_block_from_str(self, sequence: str):
        """
        Create sequence block from sequence string.
        :pararm sequence: string containing sequence data in fasta or fastq format
        """
        if sequence[0] == ">":
            i = 0
            while i < len(sequence) -1:
                seq = ""
                name = ""
                while sequence[i] != "\n" and i < len(sequence):
                    if sequence[i] == ">":
                        i += 1
                        name, shift = self._get_until(sequence[i:], "\n")
                        i += shift + 1
                    else:
                        seq_line, shift = self._get_until(sequence[i:], ">")
                        seq += seq_line
                        i += shift - 1
                sr = SequenceRead(name = name, sequence = seq)
                self.sequences.append(sr)
                i += 1
        elif sequence[0] == "@":
            i = 0
            while i < len(sequence):
                if sequence[i] == "@":
                    i += 1
                    name = self._get_until(sequence[i:], "\n")
                    i += (len(name) + 1)
                    seq  = self._get_until(sequence[i:], "\n")
                    i += (len(seq) + 1)
                    comment = self._get_until(sequence[i:], "\n")
                    i += (len(comment) + 1)
                    quality = self._get_until(sequence[i:], "\n")
                    if len(quality) != len(seq):
                        self.invalid_reads += 1
                        continue;
                    i += len(quality) + 1
                    if i > len(sequence) or sequence[i] == "@":
                        sr = SequenceRead(
                            name           = name,
                            sequence       = seq,
                            comment        = comment,
                            quality_scores = quality)
                        self.sequences.append(sr)
                    else:
                        skip = self._get_until(sequence[i:], "@")
                        i += len(skip) + 1
                else:
                    i += 1

    @staticmethod
    def _get_until(string: str, char: str):
        """
        Return string leading up to where char is found with newlines removed.
        :param string: string to get characters from
        :param char: char to search for
        """
        r = string.split(char)[0]
        l = len(r)
        return r.replace("\n", ""), l

    def __str__(self):
        return f"SequenceBlock(n_seqs={len(self.sequences)})"
