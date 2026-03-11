#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matrix_file    = sys.argv[1]
traceback_file = sys.argv[2]
output_image   = sys.argv[3]

# Matrix einlesen
matrix = []
with open(matrix_file) as f:
    for line in f:
        row = line.strip().split("\t")
        if row:
            int_row = []
            for v in row:
                if v.strip() != "":
                    int_row.append(int(v))
            matrix.append(int_row)

# Traceback einlesen
path_i = [] #Zeile
path_j = [] #Spalte

with open(traceback_file) as f:
    for line in f:
        i, j = line.strip().strip("()").split(",")
        path_i.append(int(i))
        path_j.append(int(j))

data = np.array(matrix)

plt.imshow(data, cmap="RdYlBu_r", aspect="auto")
plt.colorbar(label="Score")
if path_i:
    plt.plot(path_j[::-1], path_i[::-1], color="red", linewidth=1.5)
plt.title("DP Matrix")
plt.savefig(output_image, dpi=120)
plt.close()