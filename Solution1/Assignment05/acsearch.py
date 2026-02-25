#!/usr/bin/python3

import urllib.request
import argparse




parser = argparse.ArgumentParser()
parser.add_argument("--ac",required=True)

args = parser.parse_args()

ac2 = args.ac


url = "https://rest.uniprot.org/uniprotkb/" + ac2 + ".fasta"

try:
    response = urllib.request.urlopen(url)
    data = response.read()
    data = data.decode("utf-8")
    print(data)
except:
    SystemExit("Invalid accession number")


