#!/usr/bin/env python3
#quelle w3school html-tutorial

#Autor Laura Martin+
import subprocess

import mycgi

print ("Content-type: text/html\n")

form = mycgi.Form()

output = None

seq1 = form["seq1"]
seq2 = form["seq2"]
id1 = form["id1"]
id2 = form["id2"]
matrix = form["matrix"]
mode = form["mode"]
fmt = form["fmt"]
go = form["go"]
ge = form["ge"]
use_nw = form["use_nw"]

ref_align1 = form["ref_align1"]
ref_align2 = form["ref_align2"]
db_id1 = form["db_id1"]
db_id2 = form["db_id2"]
show_dp = form["show_dp"]

#Einlesen:
alignment_jar = "finaljars/alignment.jar"
matrix_path = "matrices/" + matrix
seqlib_file = "seqlib.txt" #wo sind die sequenzen gespeichert
pairs_file = "pairs.txt"  #welche Sequenzpaare werden allaniert


with open(pairs_file, "w") as f:
    f.write(f"{id1} {id2}\n")

with open(seqlib_file, "w") as f:
    f.write(f"{id1}:{seq1}\n")
    f.write(f"{id2}:{seq2}\n")

output = subprocess.run(["java", "-jar", alignment_jar, "--pairs", pairs_file, "--seqlib", seqlib_file,
                         "-m", matrix_path, "--mode", mode, "--go", go, "--ge", ge, "--format", fmt],
                        capture_output=True, text=True)

print(f"""<!DOCTYPE html>
<html>
<body>
    <h1>Alignment</h1>
    <form method="post" enctype="multipart/form-data" action="Alignment_CGI.py"> #haben nicht .py
        <input type="text" name="id1" value="{id1}">
        <input type="text" name="id2" value="{id2}"><br>
        <textarea name="seq1">{seq1}</textarea>
        <textarea name="seq2">{seq2}</textarea><br>
        
        <select name="matrix"> #alle Matrizen die auf Server liegen
            <option value="dayhoff.mat"> <p>dayhoff</p> </option>
            <option value="BlakeCohenMatrix.mat"> <p>BlakeCohenMatrix</p> </option>
            <option value="blosum62.mat"> <p>BLOSUM62</p> </option>
            <option value="pam250.mat"> <p>pam250</p> </option>
        </select>
        
        <select name="mode">
            <option value="global"> <p>global</p> </option>
            <option value="local"> <p>local</p> </option>
            <option value="freeshift"> <p>freeshift</p> </option>
        </select>
        
        <select name="format">
            <option value="ali"> <p>ali</p> </option>
            <option value="scores"> <p>scores</p> </option>
            <option value="html"> <p>html</p> </option>
        </select></br>
        
            <input type="text" name="go" value="{go}">
            <input type="text" name="ge" value="{ge}"><br>
            <input type="submit" value="Alignment berechnen">
            
        <section>
            <input type="checkbox" name="check"> <p>check</p> <br>
            <input type="checkbox" name="show_dp"> <p>DP-Matrix</p> <br>
        </section>
    </form>
    
    <h2>Output</h2>
    <pre>
""")

if output:
    print(output.stdout)

print(f"""
        </pre>
    </body>
</html>
""")
