#!/usr/bin/python3
import argparse
import os
import subprocess
import tempfile
import urllib

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


with urllib.request.urlopen("https://files.rcsb.org/download/"+ id +".pdb") as r:
    text = r.read().decode("utf-8")
    connectionsAS = 0
    distance = []
    line_counter = 0
    for line in text.splitlines():

        if line.startswith("ATOM"):
            parts = line.split()



            if parts[2] == type:

                print(type)
                as_converted = as_map[parts[3]]
                temp = [float(parts[5]), as_converted, parts[6], parts[7], parts[8], parts[4]]
                distance.append(1)
    print(len(distance))
    print(line_counter)






    for d in distance:
        count_global=0
        count_local=0
        current_chain = d[5]

        coordinates_node = [float(x) for x in [d[2],d [3], d[4]]]
        for k in distance:
            other_chain = k[5]

            if k == d: continue
            coordinates=  [float(x) for x in [k[2], k[3], k[4]]]
            distanceA_B = np.sqrt(
                np.square(coordinates[0] - coordinates_node[0]) +
                np.square(coordinates[1] - coordinates_node[1]) +
                np.square(coordinates[2] - coordinates_node[2])
            )
            if distanceA_B <= distance_threshhold:
                if abs(k[0]-d[0]) <= length and current_chain == other_chain:
                    count_local += 1
                else:
                    count_global += 1
        print (f'chain {current_chain} | {d[1]} | {d[0]} | local {count_local} | global {count_global}')









