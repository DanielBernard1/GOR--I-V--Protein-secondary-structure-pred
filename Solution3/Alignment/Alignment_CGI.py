#!/usr/bin/biopython
# quelle w3school html-tutorial

# Autor Laura Martin+
import subprocess
import mycgi
import mysql.connector

form = mycgi.Form()

# Werte einlesen
if "input_type" in form:
    submitted = True
    input_type = form["input_type"].value
else:
    submitted = False
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
if input_type == "native":
    style_native = "display: block;"
else:
    style_native = "display: none;"

if "seq1" in form:
    seq1 = form["seq1"].value
else:
    seq1 = ""

if "seq2" in form:
    seq2 = form["seq2"].value
else:
    seq2 = ""

if "id1" in form:
    id1 = form["id1"].value
else:
    id1 = ""

if "id2" in form:
    id2 = form["id2"].value
else:
    id2 = ""

if "pdb1" in form:
    pdb1_input = form["pdb1"].value.strip()
else:
    pdb1_input = ""
if "pdb2" in form:
    pdb2_input = form["pdb2"].value.strip()
else:
    pdb2_input = ""

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

if "use_nw" in form:
    use_nw = form["use_nw"].value
else:
    use_nw = "gotoh"
show_dp = "show_dp" in form

if "ss" in form:
    use_ss = form["ss"].value
else:
    use_ss = "none"

if use_nw == "nw":
    style_go = "display: none;"
else:
    style_go = "display: block;"

try:
    int(go)
except ValueError:
    go = "-12"

try:
    int(ge)
except ValueError:
    ge = "-1"

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

# Native pairs.txt + seqlib.txt Upload
native_error = ""
use_native = False
if input_type == "native":
    pairs_ok = "pairs_file" in form and hasattr(form["pairs_file"], "file") and form["pairs_file"].filename
    seqlib_ok = "seqlib_file" in form and hasattr(form["seqlib_file"], "file") and form["seqlib_file"].filename
    if not pairs_ok or not seqlib_ok:
        native_error = "ERROR: Bitte beide Dateien hochladen (pairs.txt und seqlib.txt)."
    else:
        try:
            pairs_content = form["pairs_file"].file.read().decode("utf-8")
            seqlib_content = form["seqlib_file"].file.read().decode("utf-8")
            with open("pairs.txt", "w") as f:
                f.write(pairs_content)
            with open("seqlib.txt", "w") as f:
                f.write(seqlib_content)
            use_native = True
            first_pair = pairs_content.strip().splitlines()[0].split()
            if len(first_pair) >= 2:
                id1 = first_pair[0]
                id2 = first_pair[1]
        except Exception as e:
            native_error = f"ERROR beim Einlesen der Dateien: {e}"

# pdb_error hier initialisieren damit Java-Bedingung unten funktioniert
pdb_error = ""

text_error = ""
if input_type == "text" and submitted and (not seq1 or not seq2):
    text_error = "Fehler: Bitte beide Sequenzen eingeben."

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
        cursor.execute("SELECT sequence FROM Homstrad WHERE pdb_id = %s", (pdb1_input.lower(),))
        row = cursor.fetchone()
        seq1 = row[0] if row else None
        cursor.execute("SELECT sequence FROM Homstrad WHERE pdb_id = %s", (pdb2_input.lower(),))
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

# Java starten — VOR dem HTML damit Download möglich ist
import sys

# Java starten
alignment_jar = "../finaljars/alignment.jar"
matrix_path = "/home/m/martinla/public_html/propragruppe15/Solution3/Alignment/matrices/" + matrix
seqlib_file = "seqlib.txt"
pairs_file = "pairs.txt"

output = None
java_error = ""

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

print("Content-type: text/html\n")

if "download_output" in form:
    download_output = True
else:
    download_output = False

if output and not java_error and (input_type == "native" or download_output):
    if fmt == "ali":
        ext = "ali"
    elif fmt == "scores":
        ext = "scores"
    else:
        ext = "txt"
    filename = f"alignment_{id1}_vs_{id2}.{ext}"
    # print("Content-Type: text/plain")
    # print(f"Content-Disposition: attachment; filename=\"{filename}\"")
    # print()
    print(output.stdout)
    sys.exit(0)

# Vorberechnete Werte für HTML-Template
if download_output:
    download_output_checked = "checked"
else:
    download_output_checked = ""
# HTML ZUERST DRUCKEN

print(f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Alignment — propraGruppe15</title>


    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../../Solution1/Assignemnt03/style.css">
      
    <script>
    function switchInput(type) {{
        document.getElementById('input_text').style.display = 'none';
        document.getElementById('input_file').style.display = 'none';
        document.getElementById('input_pdb').style.display  = 'none';
        document.getElementById('input_native').style.display = 'none';
        document.getElementById('input_' + type).style.display = 'block';
        document.getElementById('input_type_hidden').value = type;
    }}
    function switchGap(algo) {{
        if (algo === 'gotoh') {{
            document.getElementById('gap_open').style.display   = 'block';
            document.getElementById('gap_extend').style.display = 'block';
        }} else {{
            document.getElementById('gap_open').style.display   = 'none';
            document.getElementById('gap_extend').style.display = 'block';
        }}
    }}
    window.onload = function() {{
        switchGap(document.querySelector('select[name=use_nw]').value);
    }};
    </script>
</head>
<body>

<nav>
    <a class="nav-logo" href="https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution1/Assignment03/aufgabe3_2_0.html">
        <svg viewBox="0 0 22 22" fill="none" width="20" height="20">
            <ellipse cx="11" cy="11" rx="4"  ry="10" stroke="#2e7d52" stroke-width="1.8" fill="none"/>
            <ellipse cx="11" cy="11" rx="10" ry="4"  stroke="#4caf80" stroke-width="1.8" fill="none"/>
            <circle  cx="11" cy="11" r="2"           fill="#2e7d52"/>
        </svg>
        propraGruppe15
    </a>
    <ul class="nav-links">
        <li><a href="https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution1/Assignment03/aufgabe3_2_0.html">Home</a></li>
        <li><a href="https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution3/GOR/Test.py">GOR</a></li>
        <li style="margin-left: auto;"><a href="../../../Solution1/Assignment03/help/index.html">Help</a></li>
        <li><a href="../../Solution1/Assignment03/about/index.html">About</a></li>
        <!-- class="active": markiert die aktuelle Seite -->
        <li><a href="Alignment_CGI.py" class="active">Alignment</a></li>
    </ul>
</nav>

<div class="page-header">
    <h1>Alignment</h1>
    <p>Gotoh &nbsp;&middot;&nbsp; Needleman-Wunsch &nbsp;&middot;&nbsp; Smith-Waterman</p>
    <div class="seq-deco">MVLSPADKTNVKAAWGKV--GAHAGEYGAEALERMFLSFPTTKTYFPHFD &middot;&middot;&middot; MVHLTPEEKSAVTALWGKVNVDEVGG &middot;&middot;&middot; ACDEFGHIKLMNPQRSTVWY</div>
</div>

<div class="page-wrapper">

    <p class="section-label">New Searchrequest</p>
    <div class="card">
    <form method="post" enctype="multipart/form-data" action="Alignment_CGI.py">

        <p style="font-size:0.85rem; color:var(--text-dim); margin-bottom:10px;">Input-Type:</p>

        <p style="font-size:0.8rem; color:var(--text-dim);">Own Sequences:</p>
        <input type="button" value="Enter Sequences manually" onclick="switchInput('text')">

        <p style="font-size:0.8rem; color:var(--text-dim);">Upload pairs and seqlib File</p>
        <input type="button" value="pairs + seqlib" onclick="switchInput('native')">

        <p style="font-size:0.8rem; color:var(--text-dim); margin-top:8px;">Upload FastaFile:</p>
        <input type="button" value="Enter Fasta-File" onclick="switchInput('file')">

        <p style="font-size:0.8rem; color:var(--text-dim); margin-top:8px;">Upload PDB-IDs from the Database:</p>
        <input type="button" value="Enter PDB-Ids" onclick="switchInput('pdb')">

        <input type="hidden" name="input_type" id="input_type_hidden" value="{input_type}">
        <br>

        <div id="input_text" style="{style_text}">
            <div class="param-grid">
                <div>
                    <label class="field-label">Id 1</label>
                    <input type="text" name="id1" value="{id1}">
                </div>
                <div>
                    <label class="field-label">Id 2</label>
                    <input type="text" name="id2" value="{id2}">
                </div>
            </div>
            <label class="field-label">Sequenz 1</label>
            <textarea name="seq1">{seq1}</textarea>
            <label class="field-label">Sequenz 2</label>
            <textarea name="seq2">{seq2}</textarea>
        </div>

        <div id="input_file" style="{style_file}">
            <label class="field-label">FASTA-Datei (min. 2 Sequenzen — erste zwei werden aligned)</label>
            <input type="file" name="seqfile">
        </div>

        <div id="input_pdb" style="{style_pdb}">
            <div class="param-grid">
                <div>
                    <label class="field-label">PDB-ID 1</label>
                    <input type="text" name="pdb1" value="{pdb1_input}" placeholder="z.B. 13pk">
                </div>
                <div>
                    <label class="field-label">PDB-ID 2</label>
                    <input type="text" name="pdb2" value="{pdb2_input}" placeholder="z.B. 155c">
                </div>
            </div>
        </div>

        <div id="input_native" style="{style_native}">
            <label class="field-label">pairs.txt</label>
            <input type="file" name="pairs_file" accept=".txt">
            <label class="field-label">seqlib.txt</label>
            <input type="file" name="seqlib_file" accept=".txt">
        </div>

    </div><!-- end card -->

    <p class="section-label">Parameters</p>
    <div class="card">
        <div class="param-grid">
            <div>
                <label class="field-label">Matrix</label>
                <select name="matrix">
                    <option value="dayhoff.mat"         {'selected' if matrix == 'dayhoff.mat' else ''}>dayhoff</option>
                    <option value="BlakeCohenMatrix.mat" {'selected' if matrix == 'BlakeCohenMatrix.mat' else ''}>BlakeCohenMatrix</option>
                    <option value="blosum62.mat"         {'selected' if matrix == 'blosum62.mat' else ''}>BLOSUM62</option>
                    <option value="pam250.mat"           {'selected' if matrix == 'pam250.mat' else ''}>pam250</option>
                </select>
            </div>
            <div>
                <label class="field-label">Mode</label>
                <select name="mode">
                    <option value="global"    {'selected' if mode == 'global' else ''}>global</option>
                    <option value="local"     {'selected' if mode == 'local' else ''}>local</option>
                    <option value="freeshift" {'selected' if mode == 'freeshift' else ''}>freeshift</option>
                </select>
            </div>
            <div>
                <label class="field-label">Output-Format</label>
                <select name="format">
                    <option value="html"   {'selected' if fmt == 'html' else ''}>html</option>
                    <option value="ali"    {'selected' if fmt == 'ali' else ''}>ali</option>
                    <option value="scores" {'selected' if fmt == 'scores' else ''}>scores</option>
                </select>
            </div>
            <div>
                <label class="field-label">Algorithm</label>
                <select name="use_nw" onchange="switchGap(this.value)">
                    <option value="gotoh" {'selected' if use_nw == 'gotoh' else ''}>Gotoh</option>
                    <option value="nw"    {'selected' if use_nw == 'nw' else ''}>Needleman-Wunsch / Smith-Waterman</option>
                </select>
            </div>
            <div id="gap_open" style="{style_go}">
                <label class="field-label">Gap Open</label>
                <input type="text" name="go" value="{go}">
            </div>
            <div id="gap_extend">
                <label class="field-label">Gap Extension</label>
                <input type="text" name="ge" value="{ge}">
            </div>
        </div>

        <div class="checkbox-row">
            <input type="checkbox" name="show_dp" id="show_dp" {'checked' if show_dp else ''}>
            <label for="show_dp">DP-Matrix &amp; Fixed Point anzeigen</label>
        </div>
    </div><!-- end card -->

        <input type="submit" value="Calculate Alignment">
    </form>

    <hr>
    <p class="section-label">Result</p>
""")

if file_error:
    print(f'<p class="error">{file_error}</p>')
if text_error:
    print(f'<p class="error">{text_error}</p>')

if output:
    print("<pre>")
if java_error:
    print(f"<p class='error'>{java_error}</p>")
if output:
    import re

    java_out = output.stdout
    # Java gibt bei format=html eine komplette HTML-Seite aus — nur Body-Inhalt nehmen
    # sonst wird unsere Seite blau/kaputt durch Java-eigenes CSS
    if "<html" in java_out.lower():
        body_match = re.search(r'<body[^>]*>(.*?)</body>', java_out, re.DOTALL | re.IGNORECASE)
        java_out = body_match.group(1).strip() if body_match else java_out
        # DESIGN: result-bar + div (nicht pre) damit Java-Spans sichtbar bleiben
        print(
            f'<div class="result-bar"><span class="result-dot"></span>Mode: {mode} &nbsp;&middot;&nbsp; Matrix: {matrix} &nbsp;&middot;&nbsp; {use_nw}</div>')
        print('<div class="result">')
        print(java_out)
        print('</div>')
    else:
        # Kein HTML-Output (ali/scores): in <pre> anzeigen
        print(
            f'<div class="result-bar"><span class="result-dot"></span>Mode: {mode} &nbsp;&middot;&nbsp; Matrix: {matrix} &nbsp;&middot;&nbsp; {use_nw}</div>')
        print('<pre class="result">')
        print(java_out)
        print('</pre>')
    print('<p class="section-label">Graphics</p>')

# DP-Matrix und Fixpoint
dp_path = "/home/m/martinla/public_html/propragruppe15/Solution3/Alignment/dp/"

if show_dp and seq1 and seq2 and output:
    try:
        cmd_dp = ["java", "-jar", alignment_jar,
                  "--pairs", pairs_file, "--seqlib", seqlib_file,
                  "-m", matrix_path, "--mode", mode,
                  "--go", go, "--ge", ge, "--format", fmt,
                  "--dpmatrices", dp_path]
        if use_nw == "nw":
            cmd_dp.append("--nw")
        if use_ss == "ss":
            cmd_dp.append("--ss")
        subprocess.run(cmd_dp, capture_output=True, text=True)

        dp_png = dp_path + "dp_matrix_" + id1 + "_" + id2 + ".png"
        dp_vis = subprocess.run(["python3", "../dp_matrix.py", dp_png], capture_output=True, text=True)
        print("<h2>DP-Matrix:</h2>")
        print(
            f"<img src='https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution3/Alignment/dp/dp_matrix_{id1}_{id2}.png'>")
        # print("</div>")

        fp_file = dp_path + "fixedpoint_" + id1 + "_" + id2 + ".txt"
        fp_png = dp_path + "fixedpoint_" + id1 + "_" + id2 + ".png"
        subprocess.run(["python3", "FixPoint.py", fp_file, fp_png])
        print("<h2>Fixed Point Alignment</h2>")
        print(
            f"<img src='https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution3/Alignment/dp/fixedpoint_{id1}_{id2}.png'>")
    except Exception as e:
        print(f"<p class='error'>DP-Matrix Fehler: {e}</p>")

print("""
</div>


<footer>
    <span>propraGruppe15 &mdash; Bioinformatik-Praktikum &middot; Gruppe 15</span>
    <span>Alignment</span>
</footer>

</body>
</html>
""")