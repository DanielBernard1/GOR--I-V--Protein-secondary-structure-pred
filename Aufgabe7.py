#!/usr/bin/python3
import re
#from FASTAreader import FASTAreader
import argparse as ap
import sys
import urllib.request
parser = ap.ArgumentParser()
parser.add_argument('--fasta', required=True)
src = parser.add_mutually_exclusive_group(required=True)
src.add_argument('--pattern')
src.add_argument('--web')


args = parser.parse_args()


class FASTAreader:
    def __init__(self):
        self.motifs = {}
        self.indexes = []
    def read_fasta_function(self, filepath):
        self.motifs = {}
        self.indexes = []
        if filepath =="-":
            f = sys.stdin
            lines = f.readlines()
        else:
            with open(filepath, 'r') as f:
                lines = f.readlines()
        current_key = None
        for line in lines:
            s = line.strip()
            if not s: continue
            
            if s.startswith('>'):
                current_key = s[1:]
                self.motifs[current_key] = ""
                self.indexes.append(line)
            elif current_key is not None:
                self.motifs[current_key] += s
        
        return self.motifs
    

    def get_indexes(self, index):
        return self.indexes[index]
        
filepath = "-"
filepath = args.fasta
reader = FASTAreader()
fasta_as_dict = reader.read_fasta_function(filepath)




input = ""


if args.web is not None:
    ac2 = args.web
    url = "https://prosite.expasy.org/" + ac2 + ".txt"
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")

    for line in data.splitlines(True):
        
        if line[:2] == "PA":
            pattern = line[5:-2]
            input = pattern
            break
        else: continue
else:
    input = args.pattern



output_list = []

for i in input:
    if i == "{":
        output_list.append("[^")
    elif i == "}": 
        output_list.append("]")
    elif i == "x": 
        output_list.append(".")
    elif i == "(": 
        output_list.append("{")
    elif i == ")": 
        output_list.append("}")
    elif i == "<": 
        output_list.append("^")
    elif i == ">": 
        output_list.append("$")
    elif i == "?": 
        output_list.append(".")
    elif i == "*": 
        output_list.append(".*")
    elif i == "-": 
        continue  
    else: 
        output_list.append(i)
output_list= "".join(output_list) 
input = re.compile(output_list) 
#print(output_list)

lookahead_pattern = re.compile(f'(?=({input.pattern}))')

for key, value in fasta_as_dict.items():
    if input.search(value):
        for m in re.finditer(lookahead_pattern, value): 
            print(f"{key}\t{m.start()}\t{m.group(1)}")
