#!/usr/bin/python3
import argparse
import os
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--id", required=True)
parser.add_argument("--output", default=".")
parser.add_argument("--colourized", action="store_true")
parser.add_argument("--html", required=False,action="store_true")

args = parser.parse_args()

id = args.id.upper()
output = args.output
os.makedirs(output, exist_ok=True)


if args.html:
    outfile = os.path.join(output, f"{id}.html").replace("\\", "/")
    with open(outfile, "w") as f:
        f.write(f'''<!doctype html >
        <html>
        <title> A simple Jsmol example </title>
        <head>
        <script type = "text/javascript" src = "jsmol/JSmol.min.js"></script>
        <script type = "text/javascript">
        var Info = {{
            width: 1000,
            height: 1000,
            j2sPath: "jsmol/j2s"
        }}
    </script>
    </head>
    <body>
    <script type = "text/javascript">
    viewer = Jmol.getApplet("viewer", Info);
    Jmol.script(viewer, "background black; load ={id}; wireframe only; spin on")
    </script>

    </body>
    </html> ''')


else:
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

