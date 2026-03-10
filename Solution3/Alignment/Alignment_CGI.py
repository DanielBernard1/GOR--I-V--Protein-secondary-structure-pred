#!/usr/bin/biopython
#quelle w3school html-tutorial

#Autor Laura Martin+
import subprocess
import mycgi
import mysql.connector

print("Content-type: text/html\n")

form = mycgi.Form()

# Werte einlesen


submitted  = "input_type" in form
input_type = form["input_type"].value if submitted else ""

# Welches Input-Div soll sichtbar sein (wird in HTML eingesetzt)
style_text = "display: block;" if input_type == "text" else "display: none;"
style_file = "display: block;" if input_type == "file" else "display: none;"
style_pdb    = "display: block;" if input_type == "pdb"    else "display: none;"
style_native = "display: block;" if input_type == "native" else "display: none;"

# Sequenz-Felder (nur bei text-Input direkt aus Form)
seq1 = form["seq1"].value if "seq1" in form else ""
seq2 = form["seq2"].value if "seq2" in form else ""
id1  = form["id1"].value  if "id1"  in form else ""
id2  = form["id2"].value  if "id2"  in form else ""

# PDB-Eingaben zwischenspeichern — DB-Abfrage kommt erst NACH dem HTML
pdb1_input = form["pdb1"].value.strip() if "pdb1" in form else ""
pdb2_input = form["pdb2"].value.strip() if "pdb2" in form else ""

# Parameter
matrix = form["matrix"].value if "matrix" in form else "dayhoff.mat"
mode   = form["mode"].value   if "mode"   in form else "global"
fmt    = form["format"].value if "format" in form else "html"
go     = form["go"].value     if "go"     in form else "-12"
ge     = form["ge"].value     if "ge"     in form else "-1"
use_nw = form["use_nw"].value if "use_nw" in form else "gotoh"
show_dp = "show_dp" in form

style_go = "display: none;" if use_nw == "nw" else "display: block;"

# Für FASTA-File: Datei direkt hier parsen (kein DB-Call, kein Crash)
file_error = ""
if input_type == "file" and "seqfile" in form and hasattr(form["seqfile"], "file") and form["seqfile"].filename:
    try:
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
            file_error = "ERROR: Not enough sequences in the file."
        else:
            id1, seq1 = entries[0]
            id2, seq2 = entries[1]
    except Exception as e:
        file_error = f"ERROR reading file: {e}"

# Text-Input Fehler (nur wenn submitted)
# Native pairs.txt + seqlib.txt Upload
native_error = ""
use_native   = False
if input_type == "native":
    pairs_ok  = "pairs_file"  in form and hasattr(form["pairs_file"],  "file") and form["pairs_file"].filename
    seqlib_ok = "seqlib_file" in form and hasattr(form["seqlib_file"], "file") and form["seqlib_file"].filename
    if not pairs_ok or not seqlib_ok:
        native_error = "ERROR: Bitte beide Dateien hochladen (pairs.txt und seqlib.txt)."
    else:
        try:
            pairs_content  = form["pairs_file"].file.read().decode("utf-8")
            seqlib_content = form["seqlib_file"].file.read().decode("utf-8")
            with open("pairs.txt", "w") as f:
                f.write(pairs_content)
            with open("seqlib.txt", "w") as f:
                f.write(seqlib_content)
            use_native = True
            first_pair = pairs_content.strip().splitlines()[0].split()
            if len(first_pair) >= 2:
                id1, id2 = first_pair[0], first_pair[1]
        except Exception as e:
            native_error = f"ERROR beim Einlesen der Dateien: {e}"

text_error = ""
if input_type == "text" and submitted and (not seq1 or not seq2):
    text_error = "Fehler: Bitte beide Sequenzen eingeben."



# HTML ZUERST DRUCKEN --> Seite immer sichtbar
# auch wenn Fehker geworfen wird

print(f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial; max-width: 900px; margin: auto; padding: 20px; }}
        h1 {{ color: #2c5f8a; border-bottom: 2px solid #2c5f8a; }}
        section {{ margin-bottom: 40px; }}
        textarea, input[type=text], select {{ padding: 5px; width: 100%; }}
        pre {{ white-space: pre-wrap; overflow-wrap: break-word; }}
        .error {{ color: red; font-weight: bold; padding: 8px; background: #fff0f0; border: 1px solid #f0a0a0; border-radius: 4px; }}
    </style>
    <script>
    function switchInput(type) {{
        document.getElementById('input_text').style.display = 'none';
        document.getElementById('input_file').style.display = 'none';
        document.getElementById('input_pdb').style.display    = 'none';
        document.getElementById('input_native').style.display = 'none';
        document.getElementById('input_' + type).style.display = 'block';
        // Setzt den hidden field damit Python weiß welcher Input-Typ gewählt wurde
        document.getElementById('input_type_hidden').value = type;
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
            <input type="file" name="seqfile">
        </div>
        <br><br>

        <div id="input_pdb" style="{style_pdb}">
            <p>Upload PDB-IDs out of the Database</p>
            <p>PDB-ID1: </p>
            <input type="text" name="pdb1" value="{pdb1_input}" placeholder="z.B. 1hba">
            <p>PDB-ID2: </p>
            <input type="text" name="pdb2" value="{pdb2_input}" placeholder="z.B. 2hbb">
        </div>
        <br><br>

        <p>Matrix:</p>
        <select name="matrix">
            <option value="dayhoff.mat"         {'selected' if matrix == 'dayhoff.mat'         else ''}>dayhoff</option>
            <option value="BlakeCohenMatrix.mat" {'selected' if matrix == 'BlakeCohenMatrix.mat' else ''}>BlakeCohenMatrix</option>
            <option value="blosum62.mat"         {'selected' if matrix == 'blosum62.mat'         else ''}>BLOSUM62</option>
            <option value="pam250.mat"           {'selected' if matrix == 'pam250.mat'           else ''}>pam250</option>
        </select>
        <br><br>

        <p>Mode:</p>
        <select name="mode">
            <option value="global"    {'selected' if mode == 'global'    else ''}>global</option>
            <option value="local"     {'selected' if mode == 'local'     else ''}>local</option>
            <option value="freeshift" {'selected' if mode == 'freeshift' else ''}>freeshift</option>
        </select>
        <br><br>

        <p>Output-Format:</p>
        <select name="format">
            <option value="html"   {'selected' if fmt == 'html'   else ''}>html</option>
            <option value="ali"    {'selected' if fmt == 'ali'    else ''}>ali</option>
            <option value="scores" {'selected' if fmt == 'scores' else ''}>scores</option>
        </select><br>

        <p>Algorithm:</p>
        <select name="use_nw" onchange="switchGap(this.value)">
            <option value="gotoh" {'selected' if use_nw == 'gotoh' else ''}>Gotoh</option>
            <option value="nw"    {'selected' if use_nw == 'nw'    else ''}>Needleman-Wunsch / Smith-Waterman</option>
        </select><br>

        <div id="gap_open" style="{style_go}">
            <p>Gap Open:</p>
            <input type="text" name="go" value="{go}">
        </div>
        <div id="gap_extend">
            <p>Gap Extension:</p>
            <input type="text" name="ge" value="{ge}">
        </div>
        <br><br>

        <input type="submit" value="Calculate Alignment">
    </form>

    <h2>Final Alignment</h2>
""")

# Fehler aus File-Parsing anzeigen
if file_error:
    print(f'<p class="error">{file_error}</p>')
if native_error:
    print(f'<p class="error">{native_error}</p>')
if text_error:
    print(f'<p class="error">{text_error}</p>')


# AB HIER: DB-Abfrage und Java

# PDB-Sequenzen aus DB holen
pdb_error = ""
if input_type == "pdb" and pdb1_input:
    try:
        db = mysql.connector.connect(
            host="mysql2-ext.bio.ifi.lmu.de",
            user="bioprakt15",
            password="$1$/NQ9xkkh$BnZDjreVX/1q0MGqWEc3M0",
            database="bioprakt15"
        )
        cursor = db.cursor()
        cursor.execute("SELECT sequence FROM homestrad WHERE pdb = %s", (pdb1_input.lower(),))
        row = cursor.fetchone()
        seq1 = row[0] if row else None

        cursor.execute("SELECT sequence FROM homestrad WHERE pdb = %s", (pdb2_input.lower(),))
        row = cursor.fetchone()
        seq2 = row[0] if row else None

        id1 = pdb1_input
        id2 = pdb2_input
        db.close()

        if not seq1 or not seq2:
            pdb_error = f"ERROR: PDB-ID nicht gefunden ('{pdb1_input}' oder '{pdb2_input}' nicht in der Datenbank)"
            seq1 = seq2 = ""
    except Exception as e:
        pdb_error = f"ERROR: Datenbankverbindung fehlgeschlagen: {e}"
        seq1 = seq2 = ""

if pdb_error:
    print(f'<p class="error">{pdb_error}</p>')

# Java nur starten wenn Sequenzen vorhanden und kein Fehler
alignment_jar = "../finaljars/alignment.jar"
matrix_path   = "/home/m/martinla/public_html/propragruppe15/Solution3/Alignment/matrices/" + matrix
seqlib_file   = "seqlib.txt"
pairs_file    = "pairs.txt"

output = None
if (use_native or (seq1 and seq2)) and not file_error and not text_error and not pdb_error and not native_error:
    try:
        if not use_native:
            with open(pairs_file, "w") as f:
                f.write(f"{id1} {id2}\n")
            with open(seqlib_file, "w") as f:
                f.write(f"{id1}:{seq1}\n")
                f.write(f"{id2}:{seq2}\n")

        cmd = ["java", "-jar", alignment_jar,
               "--pairs", pairs_file, "--seqlib", seqlib_file,
               "-m", matrix_path, "--mode", mode,
               "--go", go, "--ge", ge, "--format", fmt]
        if use_nw == "nw":
            cmd.append("--nw")

        output = subprocess.run(cmd, capture_output=True, text=True)
    except Exception as e:
        print(f'<p class="error">ERROR: Java konnte nicht gestartet werden: {e}</p>')

if output:
    print("<pre>")
    print(mode)
    print("")
    print(output.stdout)
    print(matrix)
    print("</pre>")
    print("<h2>Benchmark</h2>")
    print("<img src='benchmark.png'>")



# DP-Matrix und Fixpoint
dp_path = "/home/m/martinla/public_html/propragruppe15/Solution3/Alignment/dp/"

if show_dp and (use_native or (seq1 and seq2)) and output:
    try:
        cmd_dp = ["java", "-jar", alignment_jar,
                  "--pairs", pairs_file, "--seqlib", seqlib_file,
                  "-m", matrix_path, "--mode", mode,
                  "--go", go, "--ge", ge, "--format", fmt,
                  "--dpmatrices", dp_path]
        if use_nw == "nw":
            cmd_dp.append("--nw")
        subprocess.run(cmd_dp, capture_output=True, text=True)

        dp_vis = subprocess.run(["python3", "../dp_matrix.py", dp_path], capture_output=True, text=True)
        print("<h2>DP-Matrix:</h2><pre>")
        print(dp_vis.stdout)
        print("</pre>")

        fp_file = dp_path + "fixedpoint_" + id1 + "_" + id2 + ".txt"
        fp_png  = dp_path + "fixedpoint_" + id1 + "_" + id2 + ".png"
        subprocess.run(["python3", "FixPoint.py", fp_file, fp_png])
        print("<h2>Fixed Point Alignment</h2>")
        print(f"<img src='https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution3/Alignment/dp/fixedpoint_{id1}_{id2}.png'>")
    except Exception as e:
        print(f"<p class='error'>DP-Matrix Fehler: {e}</p>")

print("</body>\n</html>")