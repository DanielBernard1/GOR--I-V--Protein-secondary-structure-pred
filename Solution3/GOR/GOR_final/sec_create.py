#!/usr/bin/python3
import re
# from FASTAreader import FASTAreader
import argparse as ap
import sys
import urllib.request
import mysql.connector
import os
#dd
def dssp_reader(id):
    dssp_conversion_map = {
        "H": "H", "G": "H", "I": "H",  # Helix
        "E": "E", "B": "E",  # Sheet
        "S": "C", "T": "C"  # Coil
    }

    return id
def pdb_reader(id):

    as_map = {
        'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
        'GLU': 'E', 'GLN': 'Q', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
        'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P',
        'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
    }
    with open(f"All_pdb_files/{id}.pdb", 'r', encoding="utf-8") as f:
        lines = f.readlines()



    structures = {}
    seclib_temp = []
    current_chain_id = None
    chain_counter = 0
    current_sequence = []
    current_structure = []
    saw_model = False

    for line in lines:
        if line[0:5].strip()== "MODEL":
            saw_model = True

            continue
        if saw_model and line[0:5].strip() == "ENDMDL":
            break

        if line[0:5].strip() == "HELIX":
            chain_id = line[19].strip()
            start = int(line[21:25].strip())
            end = int(line[33:37].strip())
            if chain_id not in structures:
                structures[chain_id] = {"Helix": set(), "Sheet": set()}
            structures[chain_id]["Helix"].update(range(start, end +1))

        if line[0:5].strip() == "SHEET":
            chain_id = line[21].strip()
            start = int(line[22:26].strip())
            end = int(line[33:37].strip())
            if chain_id not in structures:
                structures[chain_id] = {"Helix": set(), "Sheet": set()}
            structures[chain_id]["Sheet"].update(range(start, end +1))


        if line[0:5].strip() == "ATOM" and line[12:16].strip() == "CA":
            res_name = line[17:20].strip()
            chain_id = line[21].strip()
            res_seq = int(line[22:26].strip())

            if chain_id not in structures:
                structures[chain_id] = {"Helix": set(), "Sheet": set()}

            if current_chain_id is None:
                current_chain_id = chain_id
                chain_counter += 1

            if chain_id == current_chain_id:
                current_sequence.append(as_map.get(res_name, "X"))

                if res_seq in structures[chain_id]["Helix"]:
                    current_structure.append("H")
                elif res_seq in structures[chain_id]["Sheet"]:
                    current_structure.append("E")
                else:
                    current_structure.append("C")

            else:
                if len(current_sequence) != len(current_structure):
                    print(f"Error with {id} on chain {current_chain_id}({chain_counter})")
                seclib_temp.append({
                    "id": f"{id}{chain_counter}",
                    "AS": "".join(current_sequence),
                    "SS": "".join(current_structure)
                })



                current_chain_id = chain_id
                chain_counter += 1
                current_sequence = [as_map.get(res_name, "X")]
                if res_seq in structures[chain_id]["Helix"]:
                    current_structure = ["H"]
                elif res_seq in structures[chain_id]["Sheet"]:
                    current_structure = ["E"]
                else:
                    current_structure = ["C"]
    if current_sequence:
        seclib_temp.append({
            "id": f"{id}{chain_counter}",
            "AS": "".join(current_sequence),
            "SS": "".join(current_structure)
        })

    return seclib_temp





parser = ap.ArgumentParser()
src = parser.add_mutually_exclusive_group(required=True)
src.add_argument('--id', nargs="+")
src.add_argument('--idlist')
#src2 = parser.add_mutually_exclusive_group(required=True)
#src2.add_argument('--outputfile')
#src2.add_argument('--web')

args = parser.parse_args()


#outfile = args.outputfile


all_pdb_ids = []
seclib = [] #List of dictionaries [{id: 1MB0 , seq: ASLJGAS, str: HHHEECC} {...}]

if args.idlist:
    with open(args.idlist) as f:
        for line in f:
            all_pdb_ids.append(line.strip())
else:
    all_pdb_ids = args.id


for pdb_id in all_pdb_ids:
    found = False

    for root, dirs, files in os.walk("../All_pdb_files"):
        if f"{pdb_id}.pdb" in files or f"{pdb_id}.dssp" in files:
            found = True
            break
    if not found:
        path = f"All_pdb_files/{pdb_id}.pdb"
        try:
            with urllib.request.urlopen("https://files.rcsb.org/download/" + pdb_id + ".pdb") as r:
                with open(path, "wb") as f:
                    f.write(r.read())
         #   print(f"just read {pdb_id}")
        except:
            print(f"pdb: {pdb_id} not found online")

for pdb_id in all_pdb_ids:
    for root, dirs, files in os.walk("../All_pdb_files"):
        if f"{pdb_id}.pdb" in files:
            for entry in pdb_reader(pdb_id):

                seclib.append(entry)
        elif f"{pdb_id}.dssp" in files:
            seclib.append(dssp_reader(pdb_id))

with open("../sec_lib.txt", "w") as f:
    for i in seclib:
        f.write(f">{i['id']}\n")
        f.write(f"AS {i['AS']}\n")
        f.write(f"SS {i['SS']}\n\n")
        print(f">{i['id']}")
        print(f"AS {i['AS']}")
        print(f"SS {i['SS']}\n")



