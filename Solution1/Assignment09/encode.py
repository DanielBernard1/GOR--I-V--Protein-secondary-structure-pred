#!/usr/bin/python3
import argparse
import csv
import os
import re

counts = {}

antibodys = {}
antibody_counts = {}
all_cells = set()


celltypes= []
list_of_rows = []
rna_seq = {}
chip_seq = {}

parser = argparse.ArgumentParser()
parser.add_argument("--input",required=True)
parser.add_argument("--output", required=True)


args = parser.parse_args()
input = args.input
outdir = args.output
os.makedirs(outdir, exist_ok=True)

with open(input) as f:

    reader = csv.DictReader(f)


    for row in reader:
        all_cells.add(row["Cell_Type"])



        a = row["Data_Type"]
        counts[a] = counts.get(a, 0) + 1

        if row["Data_Type"].__contains__("ChIP-seq") :
            r = row["Experimental_Factors"]
            if "Antibody=" in r :
                    a = r.split("Antibody=")[1].split()
                    cell = row["Cell_Type"]
                    antibodys.setdefault(cell, set()).add(a[0])
                    antibody_counts[cell] = len(antibodys[cell])






        if (row["Experimental_Factors"].__contains__("H3K27me3") and row["Data_Type"].__contains__("ChIP-seq") and not row["Experimental_Factors"].__contains__("H3K27me3B")) or row["Data_Type"].__contains__("RNA-seq") :
            list = [row["Data_Type"] + "$" + row["Cell_Type"] + "$" + row["DCC_Accession"]]
            list_of_rows.append(list)
            celltypes.append(row["Cell_Type"])



for celltype in celltypes:
    newlistrna = []
    newlistchip = []
    for list in list_of_rows:
         for string in list:
            list2 =  string.split("$")
            if celltype == list2[1]:
                if list2[0] == "RNA-seq" and list2[2] != "":
                    newlistrna.append(list2[2])
                if list2[0] == "ChIP-seq" and list2[2] != "":
                    newlistchip.append(list2[2])
                rna_seq[celltype] = sorted(newlistrna)
                chip_seq[celltype] = sorted(newlistchip)

with open(f"{outdir}/exptypes.tsv", "w") as out:
    for dtype in counts:
        out.write(f"{dtype}\t{counts[dtype]}\n")


with open(f"{outdir}/antibodies.tsv", "w") as out:
    for cell in sorted(all_cells):
        out.write(f"{cell}\t{antibody_counts.get(cell, 0)}\n")



with open(f"{outdir}/chip_rna_seq.tsv", "w") as out:
    common_cells = set(rna_seq.keys()) & set(chip_seq.keys())
    out.write("cell line\tRNAseq Accession\tChIPseq Accession\n")
    for key in sorted(common_cells):
        if len(rna_seq[key]) > 0 and len(chip_seq[key]) > 0:
             out.write(f'{key}\t{",".join(rna_seq[key])}\t{",".join(chip_seq[key])}\n')


#print("cell line\tRNAseq Accession\tChIPseq Accession")
#for key in sorted(common_cells):
   #print(f'{key}\t{",".join(rna_seq[key])}\t{",".join(chip_seq[key])}')

#print(antibody_counts)
#print(antibodys)
