#!/usr/bin/env python3
import argparse
import sys

# 2. In mRna umwandeln

#Input: Fasta die mit genome2orfNeu.py in die DNA Sequencen umgewandelt wird
#Output: LocusTag und darunter DNA in mRna umgewandelt
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



#Datei einlesen
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




for header in geg_fasta:
    sequence = geg_fasta[header]
    sequence = sequence.upper()
    mRNA = sequence.replace('T', 'U')

    print(header)
    print(mRNA)


