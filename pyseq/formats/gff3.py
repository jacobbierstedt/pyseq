import os
from pyseq.formats import Tsv

class GffFeature(object):
    """
    Class to handle data associated with a single feature in a GFF3.
    """
    def __init__(self):
        super(GffFeature, self).__init__()
        # Primary
        self.seqid      = ""
        self.source     = ""
        self.type       = ""
        self.start      = 0
        self.end        = 0
        self.score      = 0
        self.strand     = ""
        self.phase      = ""
        self.attributes = {}
        # Secondary
        self.Id           = ""
        self.parent       = ""
        self.name         = ""
        self.gene         = ""
        self.product      = ""
        self.locus_tag    = ""
        self.gene_biotype = ""

    def add_all_attributes(self, attributes: dict):
        """
        Add all attributes of the particular feature as object attributes.
        :param attributes: dictionary of k:v pairs from 9th GFF3 column
        """
        self.Id           = attributes["ID"]
        self.parent       = attributes.get("Parent")
        self.name         = attributes.get("Name")
        self.gene         = attributes.get("gene")
        self.product      = attributes.get("product")
        self.locus_tag    = attributes.get("locus_tag")
        self.gene_biotype = attributes.get("gene_biotype")


class Gff(Tsv):
    """
    Class to parse and store data for GFF3 file format.
    """
    GFF3_COLUMNS = [
        "seqid",
        "source",
        "type",
        "start",
        "end",
        "score",
        "strand",
        "phase",
        "attributes"
    ]
    TYPE_GENE = "gene"
    TYPE_CDS = "CDS"
    def __init__(self):
        super(Gff, self).__init__()
        self.features = {}
        self.genes    = {}
        self.CDS      = {}

    def load_gff(self, path):
        """
        Load GFF3 from filepath.
        :param path: path to gff3 file
        """
        self.load_from_file(
            path, sep = "\t",
            skip_char = "#",
            columns = Gff.GFF3_COLUMNS)

        for feature in self.info:
            atts = feature["attributes"].split(";")
            attributes = {}
            for att in atts:
                pair = att.split("=")
                if len(pair) == 2:
                    attributes.update({pair[0] : pair[1]})

            feat = GffFeature()
            feat.seqid      = feature["seqid"]
            feat.source     = feature["source"]
            feat.type       = feature["type"]
            feat.start      = feature["start"]
            feat.end        = feature["end"]
            feat.score      = feature["score"]
            feat.strand     = feature["strand"]
            feat.phase      = feature["phase"]
            feat.attributes = feature["attributes"]
            feat.add_all_attributes(attributes)
            self.features.update({feat.Id : feat})

            if feat.type == Gff.TYPE_GENE:
                self.genes.update({feat.Id : feat})
            elif feat.type == Gff.TYPE_CDS:
                self.CDS.update({feat.Id : feat})
