import argparse
import os
import urllib
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("--pdb", required=True)
parser.add_argument("--gorout", required=True)

args = parser.parse_args()

id = args.pdb
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

with urllib.request.urlopen("https://files.rcsb.org/download/" + id + ".pdb") as r:
    text = r.read().decode("utf-8")

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
            sequence += as_map.get(resname, "X")
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
        if line.startswith(f">{id}"):
            g.readline()
            predicted = g.readline()[2:].strip()

chain_list = list(chains)
referencess = list(ss)
predicted_list = list(predicted)

matches = []
mismatches = []

for i in range(len(chain_list)):
    if i < len(predicted_list):
        if referencess[i] == predicted_list[i]:
            matches.append(residues[i])
        else:
            mismatches.append(residues[i])

parts = []
for chain, resnum in matches:
    parts.append(f"(resno={resnum} and :{chain})")
jsmolmatches = " or ".join(parts)

# HTML direkt auf stdout ausgeben
print(f'''<div id="jsmol-container">
<script type="text/javascript">
var Info = {{
    width: 700,
    height: 500,
    j2sPath: "jsmol/j2s"
}};
var viewer = Jmol.getApplet("viewer", Info);
Jmol.script(viewer, "background white; load ={id}; cartoon only; color red; select {jsmolmatches}; color green;");
</script>
<p><strong>Gruen</strong> = Match &nbsp; <strong>Rot</strong> = Mismatch &nbsp; | &nbsp; Matches: {len(matches)} / {len(matches)+len(mismatches)}</p>
</div>''')