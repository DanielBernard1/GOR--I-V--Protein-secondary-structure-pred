#!/usr/bin/biopython
import argparse
import os
import subprocess
import tempfile
import urllib
import numpy as np
import urllib.request
import textwrap

parser = argparse.ArgumentParser()
parser.add_argument("--id", required=True,nargs="+")
parser.add_argument("--output", required=False)
parser.add_argument("--colourized", action="store_true")
args = parser.parse_args()

id = args.id
output = args.output





if output is not None:
    os.makedirs(output, exist_ok=True)
    for i in args.id:

        outfile = os.path.join(output, f"{i}.png").replace("\\", "/")

        script = f'''
        load "https://files.rcsb.org/download/{i}.pdb"
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


#optinal bilder ende



for id in args.id:
    afirst = []
    alast = []

    bfirst = []
    blast = []


    minx = miny = minz = float("inf")
    maxx = maxy = maxz = float("-inf")

    allsecstuk =set()

    with urllib.request.urlopen("https://files.rcsb.org/download/"+ id +".pdb") as r:
        text = r.read().decode("utf-8")

        maxline = 0
        for line in text.splitlines():
            parts = line.split()

            if line.startswith("ATOM"):


                #abstand aplha beta

                if parts[2] == "CA" and parts[5] == "1":
                    afirst = [float(x) for x in [parts[6],parts[7],parts[8]]]
                if parts[2] == "CB" and parts[5] == "1":
                    bfirst = [float(x) for x in [parts[6], parts[7], parts[8]]]

                if int(parts[5]) > int(maxline):
                    maxline = int(parts[5])


                if parts[2] == "CA" and parts[5] == str(maxline):
                    alast = [float(x) for x in [parts[6], parts[7], parts[8]]]
                if parts[2] == "CB" and parts[5] == str(maxline):
                    blast = [float(x) for x in [parts[6], parts[7], parts[8]]]

                #karton

                if float(parts[6]) < minx:
                    minx = float(parts[6])
                if float(parts[7]) < miny:
                    miny = float(parts[7])
                if float(parts[8]) < minz:
                    minz = float(parts[8])

                if float(parts[6]) > maxx:
                    maxx = float(parts[6])
                if float(parts[7]) > maxy:
                    maxy = float(parts[7])
                if float(parts[8]) > maxz:
                    maxz = float(parts[8])

            if line.startswith("HELIX"):
                allsecstuk.update(range(int(parts[5]), int(parts[8]) + 1))
            if line.startswith("SHEET"):
                allsecstuk.update(range(int(parts[6]), int(parts[9]) + 1))



        distanceCA = np.sqrt(
            np.square(alast[0]-afirst[0])+
            np.square(alast[1]-afirst[1])+
            np.square(alast[2]-afirst[2])
        )
        distanceCB = np.sqrt(
            np.square(blast[0] - bfirst[0]) +
            np.square(blast[1] - bfirst[1]) +
            np.square(blast[2] - bfirst[2]))


        XGroesse = maxx - minx
        YGroesse = maxy - miny
        ZGroesse = maxz - minz

        volumen = XGroesse * YGroesse * ZGroesse

        #% sekundär struktur
        prozent = len(allsecstuk)/ float(maxline)


        print(textwrap.dedent(f"""\
        {id}\tAnteil AS in Sekundaerstruktur\t{prozent:.4f}
        {id}\tAbstand C_alpha\t{distanceCA:.4f}
        {id}\tAbstand C_beta\t{distanceCB:.4f}
        {id}\tX-Groesse\t{XGroesse:.4f}
        {id}\tY-Groesse\t{YGroesse:.4f}
        {id}\tZ-Groesse\t{ZGroesse:.4f}
        {id}\tVolumen\t{volumen:.4f}
        """), end="")






