import argparse
import copy
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--output", required=True)
parser.add_argument("--windowsize", required=False)


args = parser.parse_args()

input = args.input
output = args.output

window = int(args.windowsize) if args.windowsize else 5

proteins = []

with open(input) as g:
    half = window // 2

    for line in g:
        if line.startswith(">"):
            header = line.strip()
            seq = g.readline()
            predicted =(g.readline()[2:].strip())
            proteins.append((header, list(seq), list(predicted)))



print(proteins[1][2])
proteinsmoothed = copy.deepcopy(proteins)
for a ,p in enumerate(proteins):
    for i, char in enumerate(p[2]):
        if i - half < 0 or i + half >= len(p[2]):
            continue
        seen = []
        for j in range(i - half, i + half + 1):
            seen.append(p[2][j])
        häufigster = Counter(seen).most_common(1)[0][0]
        proteinsmoothed[a][2][i] = häufigster

with open(output, "w", newline="\n") as f:
    for row in proteinsmoothed:
        f.write(row[0] + "\n" + ''.join(row[1]) + "SS " +''.join(row[2]) + "\n")

print(proteinsmoothed[1][2])
