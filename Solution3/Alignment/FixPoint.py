#!/usr/bin/env python3
#fixpoint --> html Tabelle

import sys

with open(sys.argv[1]) as f:
    lines = f.readlines()

min, max = map(int, lines[0].strip().split("\t"))

outputMatrix = []
for line in lines[1:]:
    if line.strip():
        outputMatrix.append(list(map(int, line.strip().split("\t"))))

def color(val):
    if max == min:
        t = 0.5
    else:
        t = (val - min) / (max - min)
    r = int(t * 255)
    g = int(t * 100)
    b = int((1 - t) * 255)
    return f"rgb({r},{g},{b})"

print("<table border='0' cellpadding='2' style='border-collapse:collapse;font-family:monospace;font-size:11px;'>")
for row in outputMatrix:
    print("<tr>")
    for val in row:
        c = color(val)
        print(f"<td style='background-color:{c};color:white;'>{val}</td>")
    print("</tr>")
print("</table>")
