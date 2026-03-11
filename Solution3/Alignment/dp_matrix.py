#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

traceback_file = sys.argv[1]
output_image   = sys.argv[2]

# Traceback-Matrix einlesen — Buchstaben = Pfad, 0 = kein Pfad
path_i = []
path_j = []
with open(traceback_file) as f:
    for i, line in enumerate(f):
        for j, val in enumerate(line.strip().split("\t")):
            if val.strip() and val.strip() != "0":
                path_i.append(i)
                path_j.append(j)

plt.figure(figsize=(8, 8))
plt.scatter(path_j, path_i, s=1, color="red")
plt.title("Traceback Path")
plt.gca().invert_yaxis()  # (0,0) oben-links wie in der Matrix
plt.savefig(output_image, dpi=120)
plt.close()