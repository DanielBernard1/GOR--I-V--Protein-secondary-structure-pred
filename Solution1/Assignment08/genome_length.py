#!/usr/bin/python3
import urllib.request
import argparse
import re
import os

#regex argumente parsen 
parser = argparse.ArgumentParser(description="Filter by organism regex")
parser.add_argument("--organism", nargs="+", required=True, help="Regex organism names")
#parser.add_argument("--output", required=True, help="Path to output file")
args = parser.parse_args()

patterns = [re.compile(p) for p in args.organism]

#Datensatz über url zugreifen 
url = "https://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/prokaryotes.txt"

with urllib.request.urlopen(url) as response:
    #with open(args.output, "w") as f:
        #f.write("Name\tSize (Mb)\n")
        for raw_line in response:
            line = raw_line.decode("utf-8").rstrip()
            #header line ignorieren 
            if line.startswith("#"):
                continue
            #Attribute sind Tab seperated
            columns = line.rstrip().split("\t")
            name = columns[0]
            size = columns[6]
            status = columns[15]
            
            
            if any(p.search(name) for p in patterns):
                if "Complete" not in status:
                    continue
                print(f"{name}\t{size}")
             #   f.write(f"{name}\t{size}\n")
