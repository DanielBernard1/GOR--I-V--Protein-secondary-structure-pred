#!/usr/bin/python3
import re

import argparse as ap
import sys
import urllib.request
parser = ap.ArgumentParser()

parser.add_argument('--sequence', nargs="+", required=True)
parser.add_argument('--genome', required=True)

args = parser.parse_args()

filepath = args.genome
seq = args.sequence

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
reader = FASTAreader()
with open(filepath, "r") as f:
    dict_fasta = reader.read_fasta_function(f)

seq_all_with_ = ""
seq_all =""
for k,v in dict_fasta.items():
    seq_all_with_ += "$"+dict_fasta[k];
    seq_all += dict_fasta[k];

pattern_count = {}


for j in seq:
    temp = re.compile(f'(?={j})')
    pattern_count[j] = len(re.findall(temp, seq_all_with_))


for k,v in pattern_count.items():
    print(f"{k}: {v}")
    print(f"prozent  {v/len(seq_all)}")

print(len(seq_all))
print(seq_all.count("N"), len(seq_all))






