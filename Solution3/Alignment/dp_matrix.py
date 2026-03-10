#!/usr/bin/env python3
import sys

with open(sys.argv[1]) as f:
    lines = f.readlines()

with open(sys.argv[2]) as f:
    lines2 = f.readlines()

# erste Zeile: Pfad-Koordinaten
path_coords = set()
for line in lines2:
    coord = line[0].strip().strip("(").strip(")")
    i, j = coord.replace(" ", "").split(",")
    path_coords.add((int(i), int(j)))

# Rest: Matrix
matrix = []
for line in lines[1:]:
    if line.strip():
        matrix.append(line.strip().split("\t"))

print("<table "
      "border='1' cellpadding='4' style='border-collapse:collapse;font-family:monospace;font-size:12px;'>")
for i, row in enumerate(matrix):
    print("<tr>")
    for j, val in enumerate(row):
        if (i, j) in path_coords:
            print(f"<td style='background-color:red;color:white;'>{val}</td>")
        else:
            print(f"<td>{val}</td>")
    print("</tr>")
print("</table>")