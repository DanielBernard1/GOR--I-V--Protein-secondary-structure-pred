#!/usr/bin/env python3
import argparse
import matplotlib.pyplot as plt


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

#Eingabe: orf-file, lower, upper und bin_size
#Output = Histogramm (optional) und Ausgabe

# Aufgabe 1: welche Proteine kodieren zwischen einer bestimmten Länge von in diesem Fall 76 und 100 AA
# Aufgabe 2: Visualisiert in HIstogramm und bin Größe von 5 AA


#argument parsing
parser = argparse.ArgumentParser(description="Convert CRISPR sequences")
parser.add_argument("--fasta", type=str, required=True, help="Path to FASTA file")
parser.add_argument("--lower", type=int, default=76)
parser.add_argument("--upper", type=int, default=100)
parser.add_argument("--bin_size", type=int, default=5)
parser.add_argument("--histogram", type=str, default=None)

args = parser.parse_args()
file_path = args.fasta

#Einlesen Fasta
reader = FASTAreader()

with open(file_path, "r") as f:
    ORFs = reader.read_fasta_function(f)

#Einlesen lower/ upper/ bin-size
lower= args.lower
upper = args.upper
bin_size = args.bin_size
histogram = args.histogram

#brauchen für jeden Orf seine Proteinlänge
counter = 0
values = []

for seq in ORFs.values():
    if seq[-3:] in {"TAA", "TAG", "TGA"}:
        length = (len(seq)/3) -1
    else:
        length = len(seq)/3
    if length >= lower and length <= upper:
        counter+=1
        values.append(length)

print(counter)

#Output in histogram?
if histogram:
    with open(histogram, "w") as out:
        edges = list(range(lower, upper + bin_size , bin_size))

        plt.hist(values, bins=edges, edgecolor="black")
        plt.xlabel("Protein length (AA)")
        plt.ylabel("Number of ORFs")
        plt.savefig(args.histogram)
        plt.close()

