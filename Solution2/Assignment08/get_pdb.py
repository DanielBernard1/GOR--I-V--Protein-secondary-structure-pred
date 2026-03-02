#!/usr/bin/python3
import argparse
import os
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("--id",required=True)
parser.add_argument("--output",required=False)
parser.add_argument("--fasta",action="store_true",required=False)

args = parser.parse_args()
output = args.output
id = args.id


if args.fasta:
    if args.output == "-":
        with urllib.request.urlopen("https://www.rcsb.org/fasta/entry/" + id ) as r:
            text = r.read().decode("utf-8")
            print(text)
    else:
        urllib.request.urlretrieve(
            f"https://www.rcsb.org/fasta/entry/{id}.fasta",
            os.path.join(output, f"{id}.pdb")
        )
if not args.fasta:
    if args.output == "-":
        with urllib.request.urlopen("https://files.rcsb.org/download/"+ id +".pdb") as r:
            text = r.read().decode("utf-8")
            print(text)
    else:
        urllib.request.urlretrieve(
            f"https://files.rcsb.org/download/{id}.pdb",
            os.path.join(output, f"{id}.pdb")
        )








url = "https://files.rcsb.org/download/1CRN.pdb"
urllib.request.urlretrieve(url, "1CRN.pdb")




