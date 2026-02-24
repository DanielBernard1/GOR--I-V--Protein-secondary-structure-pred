#!/usr/bin/python3
import argparse


class FASTAreader:
    def read_fasta_function(self, filepath):
        self.motifs = {}
        self.indexes = []

        with open(filepath, "r") as f:
            current_key = None
            for line in f:
                s = line.strip()
                if not s:
                    continue

                if s.startswith(">"):
                    current_key = s
                    self.motifs[current_key] = []
                    self.indexes.append(s)
                elif current_key is not None:
                    self.motifs[current_key].append(s)


        for k in self.motifs:
            self.motifs[k] = "".join(self.motifs[k])

        return self.motifs

#Einlesen übergebene Parameter
parser = argparse.ArgumentParser(description="ORFs aus einer Genomsequenz extrahieren")
parser.add_argument("--organism", type=str, required=True, help="FASTA-Datei einlesen")
parser.add_argument("--features", type=str, required=True, help="Feature-Table einlesen")

args = parser.parse_args()
organism_path = args.organism
features_path = args.features
# 1. Extrahierung ORFs
# Was sind ORFs= "Open Reading Frames", beginnt mit Startcodon (DNA: ATG) endet mit Stopcodon (DNA: TAA, TGA, TAG)
#sind im Feature Table unter CDS (=Coding Sequence) gespeichert, dort von Start bis Ende
#bei - Strang --> reverse Complement

reader = FASTAreader() #dict(id:seq), aber noch mit "<"
organism = reader.read_fasta_function(organism_path)

with open(features_path, "r") as g:
    header = g.readline().rstrip("\n").split("\t")
    #wird benötigt: features, genomic_accession, start, end, strand, locus_tag (=Ausgabename)
    feature_i = header.index("# feature")
    genom_acc_i = header.index("genomic_accession")
    start_i = header.index("start")
    end_i = header.index("end")
    strand_i = header.index("strand")
    locus_i = header.index("locus_tag")

    for line in g:
        spalten = line.rstrip("\n").split("\t")

        if spalten[feature_i] != "CDS": continue

        start = int(spalten[start_i])
        end = int(spalten[end_i])

        genom_acc = spalten[genom_acc_i] # genom_acc mit dem Faster-Header abgleichen --> diese Sequenzen brauchen wir

        genom = None
        for seq_id in organism:
            if genom_acc in seq_id:
                genom = organism[seq_id][start-1:end]
                locus = spalten[locus_i]
                break

        strand = spalten[strand_i]

        if genom is None: continue
        if (strand == "-"):
            rev_Base = ""
            for letter in genom[::-1]:
                if letter == "A":
                    rev_Base += "T"
                elif letter == "T":
                    rev_Base += "A"
                elif letter == "G":
                    rev_Base += "C"
                elif letter == "C":
                    rev_Base += "G"
                else:
                    genom = None
                    break

            if genom is None: continue
            genom = rev_Base

        print(">" + locus + "\n" + genom)

#TO-Do:
# diese dann wiederrum nur von Start- bis Endposition (1 basiert brauchen 0 basiert?)
# wenn wir - Strand haben dann noch reverse Complement bilden
#Ausgabe mit Locus (einfach drüber?)




