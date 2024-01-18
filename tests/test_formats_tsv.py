import os
import pytest
from pyseq.formats.tsv import Tsv



def test_tsv():
    data = R"""column1	column2	column3	column4	column5	column6
1	gene	2.2	True	["exon_1"]	{"key1": null, "key2": 1.2345}
2	transcript	3.4		["exon_2", "exon_1"]	{"key1": "dna", "key2": "protein"}
"""

    with open("tsv.tmp.tsv", "w") as f:
        f.write(data)

    tsv = Tsv()
    tsv.load_from_file("tsv.tmp.tsv")
    assert tsv._n_fields == 6
    assert tsv.info[0]["column1"] == 1
    assert tsv.info[0]["column2"] == "gene"
    assert tsv.info[0]["column3"] == 2.2
    assert tsv.info[0]["column4"] == True
    assert tsv.info[0]["column5"] == ["exon_1"]
    assert tsv.info[0]["column6"] == {"key2" : 1.2345, "key1" : None}
    assert tsv.info[1]["column1"] == 2
    assert tsv.info[1]["column2"] == "transcript"
    assert tsv.info[1]["column3"] == 3.4
    assert tsv.info[1]["column4"] == None
    assert tsv.info[1]["column5"] == ["exon_2","exon_1"]
    assert tsv.info[1]["column6"] == {"key1" : "dna", "key2" : "protein"}
    tsv.write_file("tsv.2.txt", sep="Anything")

    csv = Tsv()
    csv.load_from_file("tsv.2.txt", sep="Anything")
    assert tsv._n_fields == 6
    assert tsv.info[0]["column1"] == 1
    assert tsv.info[0]["column2"] == "gene"
    assert tsv.info[0]["column3"] == 2.2
    assert tsv.info[0]["column4"] == True
    assert tsv.info[0]["column5"] == ["exon_1"]
    assert tsv.info[0]["column6"] == {"key2" : 1.2345, "key1" : None}
    assert tsv.info[1]["column1"] == 2
    assert tsv.info[1]["column2"] == "transcript"
    assert tsv.info[1]["column3"] == 3.4
    assert tsv.info[1]["column4"] == None
    assert tsv.info[1]["column5"] == ["exon_2","exon_1"]
    assert tsv.info[1]["column6"] == {"key1" : "dna", "key2" : "protein"}
    os.remove("tsv.tmp.tsv")
    os.remove("tsv.2.txt")
