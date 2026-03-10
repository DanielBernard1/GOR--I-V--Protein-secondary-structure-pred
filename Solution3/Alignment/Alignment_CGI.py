#!/usr/bin/biopython
#quelle w3school html-tutorial

#Autor Laura Martin+
import subprocess
import mycgi
import mysql.connector

print ("Content-type: text/html\n")

form = mycgi.Form()

output = None

def get_sequence_from_db(pdb_id):
    db = mysql.connector.connect(
        host="localhost",
        user="bioprakt15",
        password="$1$/NQ9xkkh$BnZDjreVX/1q0MGqWEc3M0",
        database="bioprakt15"
    )
    cursor = db.cursor()
    cursor.execute("SELECT sequence FROM homestead WHERE pdb = %s", (pdb_id,))
    row = cursor.fetchone()
    db.close()
    return row[0] if row else None

submitted = "input_type" in form
if submitted:
    input_type = form["input_type"].value
else:
    input_type = ""

if input_type == "text":
    style_text = "display: block;"
else:
    style_text = "display: none;"

if input_type == "file":
    style_file = "display: block;"
else:
    style_file = "display: none;"

if input_type == "pdb":
    style_pdb = "display: block;"
else:
    style_pdb = "display: none;"


seq1= ""
seq2 = ""
id1 =""
id2 = ""

if input_type == "pdb" and "pdb1" in form and form["pdb1"].value.strip():
    id1 = form["pdb1"].value
    id2 = form["pdb2"].value
    seq1 = get_sequence_from_db(id1)
    seq2 = get_sequence_from_db(id2)
    if seq1 is None or seq2 is None:
        print("<p> ERROR: PDB-ID not found</p>")
        seq1 = ""
        seq2 = ""
        id1 = ""
        id2 = ""

elif input_type == "file" and "seqfile" in form and hasattr(form["seqfile"], "file") and form["seqfile"].filename:
    content = form["seqfile"].file.read().decode("utf-8")

    entries = []
    current_id, current_seq = None, []
    for line in content.splitlines():
        line = line.strip()
        if line.startswith(">"):
            if current_id:
                entries.append((current_id, "".join(current_seq)))
            current_id = line[1:].split()[0]
            current_seq = []
        elif line:
            current_seq.append(line)
    if current_id:
        entries.append((current_id, "".join(current_seq)))

    if len(entries) < 2:
        print("<p> ERROR: Not enough sequences in the file. Or Wrong File</p>")
    id1, seq1 = entries[0]
    id2, seq2 = entries[1]
else:
    if "seq1" in form:
        seq1 = form["seq1"].value
    else:
        seq1 = ""
    if "seq2" in form:
        seq2 = form["seq2"].value
    else:
        seq2 = ""
    if not seq1 or not seq2:
        print("<p style='color:red'>Fehler: Pls insert a seq</p>")

    if "id1" in form:
        id1 = form["id1"].value
    else:
        id1 = ""
    if "id2" in form:
        id2 = form["id2"].value
    else:
        id2 = ""

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

if "go" in form:
    go = form["go"].value
else:
    go = "-12"
if "ge" in form:
    ge = form["ge"].value
else:
    ge = "-1"


#if "check" in form:
#    check = True
#else:
#    check = False

if "show_dp" in form:
    show_dp = True
else:
    show_dp = False

if "use_nw" in form:
    use_nw = form["use_nw"].value
else:
    use_nw = "gotoh"

if use_nw == "nw":
    style_go = "display: none;"
else:
    style_go = "display: block;"
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
        section {{ margin-bottom: 40px; }}
        textarea, input[type=text], select {{ padding: 5px; width: 100%; }}
        pre {{ white-space: pre-wrap; overflow-wrap: break-word; }}
    </style>
    <script>
    function switchInput(type) {{
        document.getElementById('input_text').style.display = 'none';
        document.getElementById('input_file').style.display = 'none';
        document.getElementById('input_pdb').style.display  = 'none';
        document.getElementById('input_' + type).style.display = 'block';
    }}
    
    function switchGap(algo) {{
    if (algo === 'gotoh') {{
        document.getElementById('gap_open').style.display = 'block';
        document.getElementById('gap_extend').style.display = 'block';
    }} else {{
        document.getElementById('gap_open').style.display = 'none';
        document.getElementById('gap_extend').style.display = 'block';
    }}
}}
    window.onload = function() {{
        var algo = document.querySelector('select[name=use_nw]').value;
        switchGap(algo);
    }};
    </script>
</head>
<body>
    <h1>Alignment</h1>
    <h2>New Searchrequest:</h2>
    <form method="post" enctype="multipart/form-data" action="Alignment_CGI.py"> 
        <p>Input-Type:</p>
        <p>Own Sequences:</p>
        <input type="button" value="Enter Sequences manually" onclick="switchInput('text')">
        <p>Upload FastaFile: </p>
        <input type="button" value="Enter Fasta-File" onclick="switchInput('file')">
        <p>Upload PDB-IDs form the Database: </p>
        <input type="button" value="Enter PDB-Ids" onclick="switchInput('pdb')">
        
        <input type="hidden" name="input_type" id="input_type_hidden" value="{input_type}">
        <br><br>
        
        <div id="input_text" style="{style_text}">
            <p>Id1: </p>
            <input type="text" name="id1" value="{id1}">
            <p>Id2: </p>
            <input type="text" name="id2" value="{id2}"><br>
            <p>Sequenz1: </p>
            <textarea name="seq1">{seq1}</textarea>
            <p>Sequenz2: </p>
            <textarea name="seq2">{seq2}</textarea><br>
        </div>
        
        <div id="input_file" style="{style_file}">
            <p>Upload Fasta-File for multiple Alignments:</p>
            <input type="file" name="seqfile" > 
        </div>
        <br><br>
        
        <div id="input_pdb" style="{style_pdb}">
            <p>Upload PDB-IDs out of the Database</p>
            <p>PDB-ID1: </p>
            <input type="text" name="pdb1" placeholder="z.B. 1HBA">
            <p>PDB-ID2: </p>
            <input type="text" name="pdb2" placeholder="z.B. 2HBB">
        </div>
        <br><br>
        
        <p>Matrix:</p>
        <select name="matrix"> #alle Matrizen die auf Server liegen
            <option value="dayhoff.mat"> <p>dayhoff</p> </option>
            <option value="BlakeCohenMatrix.mat"> <p>BlakeCohenMatrix</p> </option>
            <option value="blosum62.mat"> <p>BLOSUM62</p> </option>
            <option value="pam250.mat"> <p>pam250</p> </option>
        </select>
        <br><br>
        
        <p>Mode:</p>
        <select name="mode">
            <option value="global"> <p>global</p> </option>
            <option value="local"> <p>local</p> </option>
            <option value="freeshift"> <p>freeshift</p> </option>
        </select>
        <br><br>
        
        <p>Output-Format:</p>
        <select name="format">
            <option value="html"> <p>html</p> </option>
            <option value="ali"> <p>ali</p> </option>
            <option value="scores"> <p>scores</p> </option>
        </select><br>
            
        <p>Algorithm:</p>
        <select name="use_nw" onchange="switchGap(this.value)">
            <option value="gotoh"> <p>Gotoh</p> </option>
            <option value="nw"> <p>Needleman-Wunsch/ Smith-Waterman</p> </option> 
        </select><br>
        
        <div id="gap_open" style="{style_go}">
            <p>Gap Open:</p>
            <input type="text" name="go" value="{go}">
        </div>
        <p>Gap Extension:</p>
        <input type="text" name="ge" value="{ge}">
        <br><br>
        
        <input type="submit" value="Calculate Alignment">
        
    </form>
    
    <h2>Final Alignment</h2>
    <pre class="result">
    
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

dp_vis = subprocess.run(["python3", "../dp_matrix.py", dp_path], capture_output=True, text=True)
print("<h2>DP-Matrix:</h2><pre>")
print(dp_vis.stdout)

fp_file = dp_path + "fixedpoint_" + id1 + "_" + id2 + ".txt"
fp_png  = dp_path + "fixedpoint_" + id1 + "_" + id2 + ".png"

subprocess.run(["python3", "FixPoint.py", fp_file, fp_png])
print("<h2>Fixed Point Alignment</h2>")
print(f"<img src='https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution3/Alignment/dp/fixedpoint_{id1}_{id2}.png'>")
