#!/usr/bin/python3
import argparse
import os
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--id", required=True)
parser.add_argument("--output", default=".")
parser.add_argument("--colourized", action="store_true")
args = parser.parse_args()

id = args.id.upper()
output = args.output
os.makedirs(output, exist_ok=True)


outfile = os.path.join(output, f"{id}.png").replace("\\", "/")

script = f'''
load "https://files.rcsb.org/download/{id}.pdb"
restrict protein
cartoon
'''

if args.colourized:
    script += "color structure\n"

script += f'''
background white
set antialiasDisplay true
refresh
write PNG "{outfile}"
exit
'''



with tempfile.NamedTemporaryFile("w", delete=False, suffix=".spt") as f:
    f.write(script)
    script_path = f.name

subprocess.run(["java", "-jar", "/mnt/extsoft/software/jmol/JmolData.jar", "-n" ,"-s", script_path])

os.remove(script_path)

