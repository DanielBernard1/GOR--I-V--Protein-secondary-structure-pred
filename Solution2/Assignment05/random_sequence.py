#!/usr/bin/env python3
import argparse
from random import *

#Input: Länge, gc Gehalt (in Prozent), optional: Sequenzname
#Output:
    # Sequenzname
    # erzeugt eine Sequenz mit bestimmten gc gehalt und länge
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

#argument parsing
parser = argparse.ArgumentParser(description="Convert CRISPR sequences")
parser.add_argument("--fasta", type=str, required=True, help="Path to FASTA file")

args = parser.parse_args()
file_path = args.fasta

reader = FASTAreader()

with open(file_path, "r") as f:
    seq = reader.read_fasta_function(f)


def gc_content_HefeChr1(seq):
    gc = 0
    for i in seq:
        if i == "G" or i == "C":
            gc += 1
    return gc / len(seq)

parser = argparse.ArgumentParser(description="Generates a random sequence with a given gc content")
parser.add_argument("--length", type=int, required=True, help="Length of the sequence")
parser.add_argument("--gc", type=float, required=True, help="GC content of the sequence")
parser.add_argument("--name", type=str, default=None, help="Name of the sequence")

args = parser.parse_args()

length = args.length
#gc = int(args.gc * length)
gc = gc_content_HefeChr1(seq)
name = args.name

random_sequence = ""

for i in range(length):
    if int(random_sequence.count("G")) + int(random_sequence.count("C")) < gc:
        random_sequence += choice(["G", "C"])
    else:
        random_sequence += choice(["A", "T"])

seq = list(random_sequence)
shuffle(seq)
random_sequence = "".join(seq)

print(f">{name}")
print(random_sequence)
