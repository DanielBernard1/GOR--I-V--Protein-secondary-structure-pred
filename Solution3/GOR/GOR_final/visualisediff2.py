import argparse
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--pdb", required=True)
parser.add_argument("--gorout", required=True)

args = parser.parse_args()

id = args.pdb.strip()
gorout = args.gorout

as_map = {
        'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
        'GLU': 'E', 'GLN': 'Q', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
        'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P',
        'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
    }

chains = ""
sequence = ""
ss = ""
seen = set()

helixes = set()
sheets = set()
residues = []

pdb_path = f"uploads/{id.lower()}.pdb"
subprocess.run(["wget", "-q", f"https://files.rcsb.org/download/{id.lower()}.pdb", "-O", pdb_path])
with open(pdb_path) as r:
    text = r.read()

for line in text.splitlines():

    if line.startswith("HELIX"):
        chain = line[19]
        start = int(line[21:25].strip())
        end = int(line[33:37].strip())
        for i in range(start, end + 1):
            helixes.add((chain, i))

    if line.startswith("SHEET"):
        chain = line[21]
        start = int(line[22:26].strip())
        end = int(line[33:37].strip())
        for i in range(start, end + 1):
            sheets.add((chain, i))

    if line.startswith("ATOM"):
        chain = line[21]
        resnum = int(line[22:26].strip())
        resname = line[17:20].strip()

        key = (chain, resnum)
        if key not in seen:
            seen.add(key)
            chains += chain
            sequence += as_map.get(resname, 'X')
            residues.append(key)

            if key in helixes:
                ss += "H"
            elif key in sheets:
                ss += "E"
            else:
                ss += "C"

predicted = ""

with open(gorout) as g:
    for line in g:
        if line.startswith(">"):
            header = line[1:].strip()
            if id.lower() == header.lower():
                g.readline()
                predicted = g.readline()[3:].strip()
                break

chain = list(chains)
referencess = list(ss)
predicted = list(predicted)

matches = []
mismatches = []

for i in range(min(len(chain), len(predicted))):
    if referencess[i] == predicted[i]:
        matches.append(residues[i])
    else:
        mismatches.append(residues[i])

parts = []
for chain, resnum in matches:
    parts.append(f"(resno={resnum} and :{chain})")
jsmolmatches = " or ".join(parts)

# Ergebnis in uploads/vis_result.html schreiben
with open("uploads/vis_result.html", "w") as f:
    f.write(f'''<script type = "text/javascript">
viewer = Jmol.getApplet("viewer", Info);
Jmol.script(viewer, "background white; load ={id}; cartoon only; spin on; color red; select {jsmolmatches}; color green;")
</script>
<p><strong>Gruen</strong> = Match &nbsp; <strong>Rot</strong> = Mismatch &nbsp; | &nbsp; Matches: {len(matches)} / {len(matches)+len(mismatches)}</p>''')