import os
import pytest
from pyseq.formats import Gff


def test_gff():
    raw_gff = R"""##gff-version 3
#!gff-spec-version 1.21
#!processor NCBI annotwriter
#!genome-build ASM19595v2
#!genome-build-accession NCBI_Assembly:GCF_000195955.2
##sequence-region NC_000962.3 1 4411532
##species https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=83332
NC_000962.3	RefSeq	region	1	4411532	.	+	.	ID=NC_000962.3:1..4411532;Dbxref=taxon:83332;gbkey=Src;genome=genomic;mol_type=genomic DNA;strain=H37Rv;type-material=type strain of Mycobacterium tuberculosis
NC_000962.3	RefSeq	gene	1	1524	.	+	.	ID=gene-Rv0001;Dbxref=GeneID:885041;Name=dnaA;experiment=DESCRIPTION:Mutation analysis%2C gene expression[PMID: 10375628];gbkey=Gene;gene=dnaA;gene_biotype=protein_coding;locus_tag=Rv0001
NC_000962.3	RefSeq	CDS	1	1524	.	+	0	ID=cds-NP_214515.1;Parent=gene-Rv0001;Dbxref=GenBank:NP_214515.1,GeneID:885041;Name=NP_214515.1;experiment=DESCRIPTION:Mutation analysis%2C gene expression[PMID: 10375628],EXISTENCE:Mass spectrometry[PMID:15525680],EXISTENCE:Mass spectrometry[PMID:21085642],EXISTENCE:Mass spectrometry[PMID:21920479];gbkey=CDS;gene=dnaA;inference=protein motif:PROSITE:PS01008;locus_tag=Rv0001;product=chromosomal replication initiator protein DnaA;protein_id=NP_214515.1;transl_table=11
"""

    with open("tmp.gff", "w") as f:
        f.write(raw_gff)

    gff = Gff()
    gff.load_gff("tmp.gff")

    assert len(gff.genes.keys())    == 1
    assert len(gff.CDS.keys())      == 1
    assert len(gff.features.keys()) == 3
    assert gff.genes["gene-Rv0001"].source     == "RefSeq"
    assert gff.genes["gene-Rv0001"].strand     == "+"
    assert gff.CDS["cds-NP_214515.1"].parent == "gene-Rv0001"
    os.remove("tmp.gff")
