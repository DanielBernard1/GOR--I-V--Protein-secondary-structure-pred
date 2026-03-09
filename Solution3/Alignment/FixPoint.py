#!/usr/bin/env python3

#erstellen Bild
import sys
import matplotlib.pyplot as plt
import numpy as np

with open(sys.argv[1]) as f:
    lines = f.readlines()

min_val, max_val = map(int, lines[0].strip().split("\t"))

matrix = []
for line in lines[1:]:
    if line.strip():
        matrix.append(list(map(int, line.strip().split("\t"))))

data = np.array(matrix)
plt.imshow(data, cmap='rainbow', aspect='auto')
plt.colorbar()
plt.savefig(sys.argv[2])  # output pfad als zweites argument