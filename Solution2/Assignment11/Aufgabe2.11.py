#!/usr/bin/biopython

print("chain\tpos\tserial\taa\tss\tglobal\tlocal")
import argparse
import os
import subprocess
import tempfile
import urllib
import urllib.request

import numpy as np



parser = argparse.ArgumentParser()
parser.add_argument("--id", required=True)
parser.add_argument("--distance", required=True)
parser.add_argument("--type", required=True)
parser.add_argument("--length", required=True)
args = parser.parse_args()

id = args.id
distance_threshhold = float(args.distance)
type = args.type
length = float(args.length)

as_map = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
    'GLU': 'E', 'GLN': 'Q', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
    'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P',
    'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
}
in_first_model = True
saw_model = False

with urllib.request.urlopen("https://files.rcsb.org/download/"+ id +".pdb") as r:
    text = r.read().decode("utf-8")
    distance = []

    helixes = set()
    sheets = set()

    for line in text.splitlines():

        if line.startswith("MODEL"):
            saw_model = True
            in_first_model = True
            continue
        if saw_model and line.startswith("ENDMDL"):
            break


        parts = line.split()


        if line.startswith("HELIX"):
            helixes.update(range(int(parts[5]), int(parts[8]) + 1))
            print(parts[5],parts[8])
        if line.startswith("SHEET"):
            print(parts[5],parts[9])
            sheets.update(range(int(parts[5]), int(parts[9]) + 1))

        if line.startswith("ATOM"):
            if parts[2] == type:

                as_converted = as_map[parts[3]]
                temp = [int(parts[5]), as_converted, parts[6], parts[7], parts[8], parts[4],parts[1]]
                distance.append(temp)







    for d in distance:
        count_global=0
        count_local=0
        current_chain = d[5]
        if d[0] in helixes:
            d.append("H")
        elif d[0] in sheets:
            d.append("E")
        else:
            d.append("C")



        coordinates_node = [float(x) for x in [d[2],d [3], d[4]]]
        for k in distance:
            other_chain = k[5]

            if k == d and current_chain == other_chain: continue
            coordinates=  [float(x) for x in [k[2], k[3], k[4]]]
            distanceA_B = np.sqrt(
                np.square(coordinates[0] - coordinates_node[0]) +
                np.square(coordinates[1] - coordinates_node[1]) +
                np.square(coordinates[2] - coordinates_node[2])
            )
            if distanceA_B < distance_threshhold :
                if abs(k[0]-d[0]) < length and current_chain == other_chain:
                    count_local += 1
                else:
                    count_global += 1



        print (f'{current_chain}\t{d[0]}\t{d[6]}\t{d[1]}\t{d[7]}\t{count_global}\t{count_local}')










