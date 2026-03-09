#!/usr/bin/biopython
#quelle w3school html-tutorial

#Autor Laura Martin+
import subprocess
import mycgi

print ("Content-type: text/html\n")

form = mycgi.Form()

output = None


seq1 = form["seq1"].value
seq2 = form["seq2"].value

id1 = form["id1"].value
id2 = form["id2"].value

if "matrix" in form:
    matrix = form["matrix"].value
else:
    matrix = "dayhoff.mat"

if "mode" in form:
    mode = form["mode"].value
else:
    mode = "global"

if "format" in form:
    fmt = form["format"].value
else:
    fmt = "html"

go = form["go"].value
ge = form["ge"].value




if "check" in form:
    check = True
else:
    check = False

if "show_dp" in form:
    show_dp = True
else:
    show_dp = False

if "use_nw" in form:
    use_nw = form["use_nw"].value
else:
    use_nw = "gotoh"


#Einlesen:
alignment_jar = "../finaljars/alignment.jar"
matrix_path = "/home/m/martinla/public_html/propragruppe15/Solution3/Alignment/matrices/" + matrix
seqlib_file = "seqlib.txt" #wo sind die sequenzen gespeichert
pairs_file = "pairs.txt"  #welche Sequenzpaare werden allaniert


with open(pairs_file, "w") as f:
    f.write(f"{id1} {id2}\n")

with open(seqlib_file, "w") as f:
    f.write(f"{id1}:{seq1}\n")
    f.write(f"{id2}:{seq2}\n")

#with open("") as f:
#    print("<h3>DP-Matrix:</h3><pre>")
#    print(f.read())
#    print("</pre>")



input = ["java", "-jar", alignment_jar, "--pairs", pairs_file, "--seqlib", seqlib_file,
                         "-m", matrix_path, "--mode", mode, "--go", go, "--ge", ge, "--format", fmt]
if use_nw =="nw":
    input.append("--nw")

output = subprocess.run(input, capture_output=True, text=True)



print(f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial; max-width: 900px; margin: auto; padding: 20px; }}
        h1 {{ color: #2c5f8a; border-bottom: 2px solid #2c5f8a; }}
        button, input[type=submit] {{background: #2c5f8a; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; }}
        section {{ margin-bottom: 40px; }}
        textarea, input[type=text], select {{ padding: 5px; width: 100%; }}
    </style>
</head>
<body>
    <h1>Alignment</h1>
    <h2>New Searchrequest:</h2>
    <form method="post" enctype="multipart/form-data" action="Alignment_CGI.py"> 
        <p>Id1: </p>
        <input type="text" name="id1" value="{id1}">
        <p>Id2: </p>
        <input type="text" name="id2" value="{id2}"><br>
        <p>Sequenz1: </p>
        <textarea name="seq1">{seq1}</textarea>
        <p>Sequenz2: </p>
        <textarea name="seq2">{seq2}</textarea><br>
        
        <select name="matrix"> #alle Matrizen die auf Server liegen
            <option value="dayhoff.mat"> <p>dayhoff</p> </option>
            <option value="BlakeCohenMatrix.mat"> <p>BlakeCohenMatrix</p> </option>
            <option value="blosum62.mat"> <p>BLOSUM62</p> </option>
            <option value="pam250.mat"> <p>pam250</p> </option>
        </select>
        <br><br>
        <select name="mode">
            <option value="global"> <p>global</p> </option>
            <option value="local"> <p>local</p> </option>
            <option value="freeshift"> <p>freeshift</p> </option>
        </select>
        <br><br>
        <select name="format">
            <option value="ali"> <p>ali</p> </option>
            <option value="scores"> <p>scores</p> </option>
            <option value="html"> <p>html</p> </option>
        </select><br>
            
        <section>
            <input type="checkbox" name="check"> <p>check</p> <br>
            <input type="checkbox" name="show_dp"> <p>DP-Matrix</p> <br>
        </section>
        
        <select name="use_nw">
            <option value="gotoh"> <p>Gotoh</p> </option>
            <option value="nw"> <p>Needleman-Wunsch/ Smith-Waterman</p> </option> 
        </select><br>
        
        <input type="text" name="go" value="{go}"><br>
        <input type="text" name="ge" value="{ge}"><br>
        <input type="submit" value="Calculate Alignment">
        
    </form>
    
    <h2>Final Alignment</h2>
    <pre>
""")

if output:
    print(mode)
    print("")
    print(output.stdout)
    print(matrix)
    print("")
    print("")
    print("<h2>Benchmark</h2>")
    print("<img src='benchmark.png'>")

print(f"""
        </pre>
    </body>
</html>
""")

dp_path = "/home/m/martinla/public_html/propragruppe15/Solution3/Alignment/dp/"

input = ["java", "-jar", alignment_jar, "--pairs", pairs_file, "--seqlib", seqlib_file,
         "-m", matrix_path, "--mode", mode, "--go", go, "--ge", ge, "--format", fmt,
         "--dpmatrices", dp_path]
if use_nw == "nw":
    input.append("--nw")

output = subprocess.run(input, capture_output=True, text=True)
#dp_vis = subprocess.run(["python3", "../dp_matrix.py", dp_path], capture_output=True, text=True)
#print("<h2>DP-Matrix:</h2><pre>")
#print(dp_vis.stdout)

fp_file = dp_path + "fixedpoint_" + id1 + "_" + id2 + ".txt"
fp_png  = "fixedpoint_" + id1 + "_" + id2 + ".png"

subprocess.run(["python3", "FixPoint.py", fp_file, fp_png])
print("<h2>Fixed Point Alignment</h2>")
print(f"<img src='fixedpoint_{id1}_{id2}.png'>")
