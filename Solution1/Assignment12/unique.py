#!/usr/bin/env python3
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


#from FASTAreader import *
import argparse

#argument parsing
parser = argparse.ArgumentParser(description="Amount of Gene unique sequences of length k")
parser.add_argument("--fasta", type=str, required=True, help="Path to FASTA file")
parser.add_argument("--k", nargs="+", required=True, help="lengths of unique sequences")
parser.add_argument("--start", type=int, required=False, help="start index", default=None)

args = parser.parse_args()
file_path = args.fasta
ks = args.k   
start = args.start 

#fasta reader
fastareader = FASTAreader()
sequences = fastareader.read_fasta_function(file_path)

for k in ks:
    kmers = {}
    for key, seq in sequences.items():
        short_seqs = set()

        if start == None:
            for i in range(len(seq) - int(k) + 1):
                short_seqs.add(seq[i:i+int(k)])
        else:
            if len(seq[start:start+int(k)]) == int(k): 
                short_seqs.add(seq[start:start + int(k)])
        
        for short_seq in short_seqs:
            if short_seq not in kmers:
                kmers[short_seq] = set()
            kmers[short_seq].add(key)

    #count unique 
    uniques = set()
    for kmer, v in kmers.items():
        if len(v) == 1:
            uniques.add(next(iter(v)))
        
    
    print(k + "\t" + str(len(uniques)))
    #print(count/len(sequences))