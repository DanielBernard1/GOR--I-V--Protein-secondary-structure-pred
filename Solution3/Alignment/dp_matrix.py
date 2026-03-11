#!/usr/bin/env python3
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

traceback_file = sys.argv[1]
output_image   = sys.argv[2]

path_i = []
path_j = []
with open(traceback_file) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        i, j = line.strip("()").split(",")
        path_i.append(int(i))
        path_j.append(int(j))

plt.figure(figsize=(5, 5))
plt.scatter(path_j, path_i, s=1, color="red")
plt.title("Traceback Path")
plt.gca().invert_yaxis()
plt.savefig(output_image, dpi=120)
plt.close()