#!/usr/bin/env python3

#erstellen Bild
import sys
import matplotlib.pyplot as plt
import numpy as np

with open(sys.argv[1]) as f:
    lines = f.readlines()

min, max = map(int, lines[0].strip().split("\t"))

matrix = []
for line in lines[1:]:
    if line.strip():
        matrix.append(list(map(int, line.strip().split("\t"))))

data = np.array(matrix, dtype=float)
threshold = min + (max - min) * 0.9
data[data < threshold] = np.nan


plt.imshow(data, cmap='rainbow', aspect='auto')
cbar = plt.colorbar()
cbar.set_label("Alignment Score (top 10%)", rotation=270, labelpad=15)


plt.title("Fix Point Alignment")
plt.savefig(sys.argv[2])  # output pfad als zweites argument
plt.close()