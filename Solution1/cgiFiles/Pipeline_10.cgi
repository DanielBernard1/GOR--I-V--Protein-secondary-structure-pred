#!/usr/bin/biopython

import os
import subprocess

import mycgi

print ("Content-Type: text/html\n")
#genom --> orf

form = mycgi.Form()

#Inputs
fasta = form["fasta"]
features = form["features"]

#Datein speichern
os.makedirs("uploads", exist_ok=True)
orf_path = "uploads/cgi.fasta"
feat_path = "uploads/cgi.features.tsv"

with open(orf_path, "wb") as f:
    f.write(fasta.value)

with open(feat_path, "wb") as f:
    f.write(features.value)
#orf_path = "C:/Users/LauMa/UNI/3.Semester/propragruppe15/Solution1/Assignment10/Downloads_Datensätze/genome_files/E_coli_K-12_MG1655_genomic.fna"
#feat_path= "C:/Users/LauMa/UNI/3.Semester/propragruppe15/Solution1/Assignment10/Downloads_Datensätze/genome_files/E_coli_K-12_MG1655_feature_table.txt"
# 1) GENOM to ORF
try:
    output1 = subprocess.run(["python3", "../Assignment10/genome2orf.py", "--organism", orf_path, "--features", feat_path], capture_output=True, text = True, check = True)
except Exception as e:
    print(e)
    print(" ".join(["python3", "../Assignment10/genome2orf.py", "--organism", orf_path, "--features", feat_path]))
    print(output1)

#if (output1.returncode == 0):


# 2) DNA to mRNA
output2 = subprocess.run(["python3", "../Assignment10/dna2mrna.py", "--fasta", "-"], input = output1.stdout, capture_output=True, text = True, check = True)

# 3) mRNA to PROTEIN
output3 = subprocess.run(["python3", "../Assignment10/mrna2aa.py", "--fasta", "-"], input = output2.stdout, capture_output=True, text = True, check = True)

#Output
result = output3.stdout

print("<pre>")
print(result)
print("</pre>")
