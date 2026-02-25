#!/usr/bin/python3
import argparse
#from FASTAreader import *
class FASTAreader:
    def __init__(self):
        self.motifs = {}
        self.indexes = []
    def read_fasta_function(self, filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()
        current_key = None
        for line in lines:
            s = line.strip()
            if not s: continue
            
            if s.startswith('>'):
                current_key = s[0:]
                self.motifs[current_key] = ""
                self.indexes.append(line)
            elif current_key is not None:
                self.motifs[current_key] += s
        
        return self.motifs
    def get_indexes(self, index):
        return self.indexes[index]

#argument parsing
parser = argparse.ArgumentParser(description="Convert CRISPR sequences")
parser.add_argument("--fasta", type=str, required=True, help="Path to FASTA file")

args = parser.parse_args()
file_path = args.fasta
fastareader = FASTAreader()
sequences = fastareader.read_fasta_function(file_path)

for seq_id, seq in sequences.items():
    for i, j in enumerate(seq):
        #avoid out of bounds
        if i + 1 == len(seq): continue 
        #check for 'GG' and verify sufficient length
        if j == "G" and seq[i+1] == "G" and i >= 21:
            print(seq_id + "\t" + str(i - 20))
            print(seq[i - 21 : i + 2])
