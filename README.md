# PySeq - A Python tool kit for biological sequence data
Python development tool kit for common biological sequence data manipulations

pyseq is a python package intended to facilitate development or exploration of biological sequence data and is always a WIP. As such, there are many limitations and optimizations to be made. 

### Quick start
pyseq is a pip installable python package. To begin using, clone the repo, and install the package in your environment.

```
git clone https://github.com/jacobbierstedt/pyseq.git
cd pyseq
pip install .
```
## Developing with pyseq
pyseq consists of several modules that facilitate development parsing, manipulating, and querying sequence data.
### Parsing a fastq/a file
```python
from pyseq.sequence_io import SequenceFile

sf = SequenceFile()
sf.load_sequence_blocks_from_file("path/to/file1.fasta")
sf.load_sequence_blocks_from_file("path/to/file2.fasta")

# The data from file1 and file2 are stored in SequenceBlock objects in SequenceFile.sequence_blocks
for block in sf.sequence_blocks:
    for read in block.sequences:
        print(f"name={read.name}  sequence={read.sequence}")
```
### Getting k-mers from a nucleotide sequence
```python
from pyseq.kmer_utils import get_kmers, get_minimized_kmers

sequence = "ATGCATGCATGCATGCATGCATGCAGATGTCGCGAGTGATGCGCGAGCGAGCT"
kmer_len = 25
minimizer_len = 17
kmers = get_kmers(sequence, kmer_len)
minimized_kmers = get_minimized_kmers(sequence, kmer_len, minimizer_len)
```
## Using the pyseq tools
There are (or will be) several available command line tools with the pyseq package for various purposes. These are available through a common entrypoint `pyseq`.
To use these tools, call pyseq and a subcommand:
```
pyseq <subcommand>
```
To list available subcommands:
```
pyseq -h
```
### pyseq bin_reads
`bin_reads` builds a minimized kmer database from a set of reference sequences and an associated json that defines the bins. It then assigns reads to the bins using weighted kmer counts based on matches between read minimizers and database minimizers. The read is classified to the bin with the highest weighted kmer count.

An example of the json file defining the bins:
```json
{
  "reference_1" : "bin_1",
  "reference_2" : "bin_1",
  "reference_3" : "bin_2"
}
```
Example reference fasta:
```
>reference_1
ATGCATCATGCATGCATGC
>reference_2
ATGCATGCATGCGATGAT
>reference_3
ATGCATGCATGCATGCATGCATGC
```
Usage:
```
pyseq bin_reads -r references.fasta -i reads.fastq -b bins.json -k 29 -m 22 -a 2 -o binned_reads.json
```
