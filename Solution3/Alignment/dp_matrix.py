#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matrix_file    = sys.argv[1]
traceback_file = sys.argv[2]
output_image   = sys.argv[3]

# Scoring-Matrix einlesen
matrix = []
with open(matrix_file) as f:
    for line in f:
        row = []
        for v in line.strip().split("\t"):
            if v.strip():
                row.append(int(v))
        if row:
            matrix.append(row)

# Traceback-Matrix einlesen — Buchstaben = Pfad, 0 = kein Pfad
path_i = []
path_j = []
with open(traceback_file) as f:
    for i, line in enumerate(f):
        for j, val in enumerate(line.strip().split("\t")):
            val = val.strip()
            # alles was kein "0" und nicht leer ist → Pfad-Zelle
            if val and val != "0":
                path_i.append(i)
                path_j.append(j)

data = np.array(matrix)

plt.imshow(data, cmap="RdYlBu_r", aspect="auto")
plt.colorbar(label="Score")
if path_i:
    plt.scatter(path_j, path_i, color="red", s=2)  # scatter statt plot, da Reihenfolge egal
plt.title("DP Matrix")
plt.savefig(output_image, dpi=120)
plt.close()