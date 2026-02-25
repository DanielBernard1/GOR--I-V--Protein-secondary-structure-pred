#!/usr/bin/env python3
import argparse
import sys


# 3. translatieren
#Input: Gibt mRNA aus Pipeline oder Fasta
#Datei einlesen
ct = {"UUU" : "F", "CUU" : "L", "AUU" : "I", "GUU" : "V",
"UUC" : "F", "CUC" : "L", "AUC" : "I", "GUC" : "V",
"UUA" : "L", "CUA" : "L",  "AUA" : "I"  ,"GUA" : "V",
"UUG" : "L", "CUG" : "L", "AUG" : "M"  ,"GUG" : "V",
"UCU" : "S" ,"CCU" : "P" ,"ACU" : "T"  ,"GCU" : "A",
"UCC" : "S" ,"CCC" : "P" ,"ACC" : "T"  ,"GCC" : "A",
"UCA" : "S" ,"CCA" : "P" ,"ACA" : "T"  ,"GCA" : "A",
"UCG" : "S" ,"CCG" : "P" ,"ACG" : "T"  ,"GCG" : "A",
"UAU" : "Y" ,"CAU" : "H" ,"AAU" : "N"  ,"GAU" : "D",
"UAC" : "Y" ,"CAC" : "H" ,"AAC" : "N"  ,"GAC" : "D",
"UAA" : "Stop","CAA" : "Q" ,"AAA" : "K","GAA" : "E",
"UAG" : "Stop","CAG" : "Q" ,"AAG" : "K","GAG" : "E",
"UGU" : "C" ,"CGU" : "R" ,"AGU" : "S"  ,"GGU" : "G",
"UGC" : "C" ,"CGC" : "R" ,"AGC" : "S"  ,"GGC" : "G",
"UGA" : "Stop","CGA" : "R" ,"AGA" : "R","GGA" : "G",
"UGG" : "W" ,"CGG" : "R" ,"AGG" : "R","GGG" : "G", "" : ""}


class FASTAreader:
    def read_fasta_function(self, filepath):
        self.motifs = {}
        self.indexes = []

        current_key = None
        for line in filepath:
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




parser = argparse.ArgumentParser(description="ORFs aus einer Genomsequenz extrahieren")
parser.add_argument("--fasta", type=str, required=True, help="FASTA-Datei einlesen")

args = parser.parse_args()
path = args.fasta

reader = FASTAreader()

if path == '-':
    geg_fasta = reader.read_fasta_function(sys.stdin)

else:
    with open(path, "r") as f:
        geg_fasta = reader.read_fasta_function(f)

with open("MyFile.txt", "w") as f:# file
    for header, seq in geg_fasta.items():
        codon = ""
        amino = ""
        i = 0

        seq = seq.upper()

        if len(seq) % 3 != 0: continue

        wrong_base = False

        for j in seq:

            if j != "A" and j != "U" and j != "G" and j != "C":
                wrong_base = True
                break
            codon += j
            if i % 3 == 2:
                if ct[codon] == "Stop": break
                amino += ct[codon]
                codon = ""
            i += 1
        if wrong_base: continue
        f.write(header + "\n") # file
        f.write(amino + "\n") # file
        print(header)
        print(amino)





