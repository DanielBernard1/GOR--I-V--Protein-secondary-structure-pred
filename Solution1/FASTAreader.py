#!/usr/bin/python3

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