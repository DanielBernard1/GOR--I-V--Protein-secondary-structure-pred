#!/usr/bin/biopython
#quelle w3school html-tutorial

#Autor Laura Martin+
import subprocess
import mycgi
import mysql.connector
import os

form = mycgi.Form()

# ── Formular-Werte einlesen ──────────────────────────────────
submitted  = "input_type" in form
input_type = form["input_type"].value if submitted else ""

style_text    = "display: block;" if input_type == "text"    else "display: none;"
style_file    = "display: block;" if input_type == "file"    else "display: none;"
style_pdb     = "display: block;" if input_type == "pdb"     else "display: none;"
style_native  = "display: block;" if input_type == "native"  else "display: none;"

seq1 = form["seq1"].value if "seq1" in form else ""
seq2 = form["seq2"].value if "seq2" in form else ""
id1  = form["id1"].value  if "id1"  in form else ""
id2  = form["id2"].value  if "id2"  in form else ""

pdb1_input = form["pdb1"].value.strip() if "pdb1" in form else ""
pdb2_input = form["pdb2"].value.strip() if "pdb2" in form else ""

matrix  = form["matrix"].value if "matrix" in form else "dayhoff.mat"
mode    = form["mode"].value   if "mode"   in form else "global"
fmt     = form["format"].value if "format" in form else "html"
go      = form["go"].value     if "go"     in form else "-12"
ge      = form["ge"].value     if "ge"     in form else "-1"
use_nw  = form["use_nw"].value if "use_nw" in form else "gotoh"
show_dp = "show_dp" in form

# download_output: wenn true, wird das Ergebnis als Datei ausgegeben statt HTML
download_output = "download_output" in form

style_go = "display: none;" if use_nw == "nw" else "display: block;"

alignment_jar = "../finaljars/alignment.jar"
matrix_path   = "/home/m/martinla/public_html/propragruppe15/Solution3/Alignment/matrices/" + matrix
seqlib_file   = "seqlib.txt"
pairs_file    = "pairs.txt"
dp_path       = "/home/m/martinla/public_html/propragruppe15/Solution3/Alignment/dp/"

# ── Input verarbeiten ────────────────────────────────────────
file_error   = ""
native_error = ""
use_native   = False  # True wenn pairs+seqlib direkt hochgeladen wurden

# FASTA-File parsen
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
            file_error = "ERROR: Not enough sequences in the file (minimum 2 required)."
        else:
            id1, seq1 = entries[0]
            id2, seq2 = entries[1]
    except Exception as e:
        file_error = f"ERROR reading FASTA file: {e}"

# Native pairs.txt + seqlib.txt direkt hochladen
elif input_type == "native":
    pairs_ok  = "pairs_file"  in form and hasattr(form["pairs_file"],  "file") and form["pairs_file"].filename
    seqlib_ok = "seqlib_file" in form and hasattr(form["seqlib_file"], "file") and form["seqlib_file"].filename
    if not pairs_ok or not seqlib_ok:
        native_error = "ERROR: Bitte beide Dateien hochladen (pairs.txt und seqlib.txt)."
    else:
        try:
            # Direkt die hochgeladenen Dateien auf den Server schreiben
            pairs_content  = form["pairs_file"].file.read().decode("utf-8")
            seqlib_content = form["seqlib_file"].file.read().decode("utf-8")
            with open(pairs_file, "w") as f:
                f.write(pairs_content)
            with open(seqlib_file, "w") as f:
                f.write(seqlib_content)
            use_native = True
            # id1/id2 aus pairs.txt lesen für spätere Dateinamen
            first_pair = pairs_content.strip().splitlines()[0].split()
            if len(first_pair) >= 2:
                id1, id2 = first_pair[0], first_pair[1]
        except Exception as e:
            native_error = f"ERROR reading native files: {e}"

text_error = ""
if input_type == "text" and submitted and (not seq1 or not seq2):
    text_error = "Fehler: Bitte beide Sequenzen eingeben."

# ── Wenn download_output: Content-type als Datei, nicht HTML ─
# Muss VOR jedem print() passieren
if download_output and submitted and fmt in ("ali", "scores") and not file_error and not native_error and not text_error:
    # Zuerst Sequenzen schreiben falls nicht native
    if not use_native and seq1 and seq2:
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

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Als Datei ausgeben
    filename = f"alignment_{id1}_{id2}.{fmt}"
    print(f"Content-Type: text/plain")
    print(f"Content-Disposition: attachment; filename=\"{filename}\"")
    print()
    print(result.stdout)
    # Script hier beenden — kein HTML mehr
    import sys
    sys.exit(0)

# ── Ab hier: normaler HTML-Output ───────────────────────────
print("Content-type: text/html\n")

print(f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial; max-width: 900px; margin: auto; padding: 20px; }}
        h1 {{ color: #2c5f8a; border-bottom: 2px solid #2c5f8a; }}
        section {{ margin-bottom: 40px; }}
        textarea, input[type=text], select {{ padding: 5px; width: 100%; }}
        pre {{ white-space: pre-wrap; overflow-wrap: break-word; }}
        .error {{ color: red; font-weight: bold; padding: 8px; background: #fff0f0; border: 1px solid #f0a0a0; border-radius: 4px; margin: 8px 0; }}
        .info  {{ color: #555; font-size: 0.85em; margin: 4px 0 10px 0; }}
        .native-example {{ font-family: monospace; font-size: 0.82em; background: #f4f4f4; border: 1px solid #ddd; padding: 10px; border-radius: 4px; margin-top: 8px; }}
    </style>
    <script>
    function switchInput(type) {{
        document.getElementById('input_text').style.display   = 'none';
        document.getElementById('input_file').style.display   = 'none';
        document.getElementById('input_pdb').style.display    = 'none';
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

    // Download-Checkbox nur bei ali/scores anzeigen (html macht als Download keinen Sinn)
    function updateDownloadOption() {{
        var fmt = document.querySelector('select[name=format]').value;
        var row = document.getElementById('download_row');
        if (fmt === 'ali' || fmt === 'scores') {{
            row.style.display = 'block';
        }} else {{
            row.style.display = 'none';
            document.getElementById('download_output').checked = false;
        }}
    }}

    window.onload = function() {{
        switchGap(document.querySelector('select[name=use_nw]').value);
        updateDownloadOption();
    }};
    </script>
</head>
<body>
    <h1>Alignment</h1>
    <h2>New Searchrequest:</h2>
    <form method="post" enctype="multipart/form-data" action="Alignment_CGI.py">

        <p>Input-Type:</p>
        <input type="button" value="Enter Sequences manually" onclick="switchInput('text')">
        <input type="button" value="FASTA File"               onclick="switchInput('file')">
        <input type="button" value="pairs + seqlib"           onclick="switchInput('native')">
        <input type="button" value="PDB-IDs (Datenbank)"      onclick="switchInput('pdb')">

        <input type="hidden" name="input_type" id="input_type_hidden" value="{input_type}">
        <br><br>

        <!-- Manuelle Sequenzeingabe -->
        <div id="input_text" style="{style_text}">
            <p>Id1: </p>
            <input type="text" name="id1" value="{id1}">
            <p>Id2: </p>
            <input type="text" name="id2" value="{id2}">
            <p>Sequenz 1: </p>
            <textarea name="seq1">{seq1}</textarea>
            <p>Sequenz 2: </p>
            <textarea name="seq2">{seq2}</textarea>
        </div>

        <!-- FASTA-Datei -->
        <div id="input_file" style="{style_file}">
            <p>FASTA-Datei hochladen (min. 2 Sequenzen):</p>
            <p class="info">Format: &gt;ID auf jeder Sequenz-Zeile. Die ersten zwei Sequenzen werden aligned.</p>
            <input type="file" name="seqfile" accept=".fasta,.fa,.txt">
        </div>

        <!-- Native pairs.txt + seqlib.txt -->
        <div id="input_native" style="{style_native}">
            <p>pairs.txt und seqlib.txt direkt hochladen:</p>
            <p class="info">Damit können mehrere Paare auf einmal aligned werden.</p>
            <!-- Beispielformat anzeigen -->
            <div class="native-example">
                <b>pairs.txt:</b><br>
                seq1 seq2<br>
                seq3 seq4<br><br>
                <b>seqlib.txt:</b><br>
                seq1:ACDEFGHIKLM...<br>
                seq2:MVLSPADKTNV...<br>
                seq3:ACDEFGHIKLM...<br>
                seq4:MVLSPADKTNV...
            </div>
            <p>pairs.txt:</p>
            <input type="file" name="pairs_file" accept=".txt">
            <p>seqlib.txt:</p>
            <input type="file" name="seqlib_file" accept=".txt">
        </div>

        <!-- PDB-IDs aus Datenbank -->
        <div id="input_pdb" style="{style_pdb}">
            <p>PDB-ID 1:</p>
            <input type="text" name="pdb1" value="{pdb1_input}" placeholder="z.B. 1hba">
            <p>PDB-ID 2:</p>
            <input type="text" name="pdb2" value="{pdb2_input}" placeholder="z.B. 2hbb">
        </div>
        <br>

        <p>Matrix:</p>
        <select name="matrix">
            <option value="dayhoff.mat"          {'selected' if matrix == 'dayhoff.mat'          else ''}>dayhoff</option>
            <option value="BlakeCohenMatrix.mat"  {'selected' if matrix == 'BlakeCohenMatrix.mat'  else ''}>BlakeCohenMatrix</option>
            <option value="blosum62.mat"          {'selected' if matrix == 'blosum62.mat'          else ''}>BLOSUM62</option>
            <option value="pam250.mat"            {'selected' if matrix == 'pam250.mat'            else ''}>pam250</option>
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
        <select name="format" onchange="updateDownloadOption()">
            <option value="html"   {'selected' if fmt == 'html'   else ''}>html</option>
            <option value="ali"    {'selected' if fmt == 'ali'    else ''}>ali</option>
            <option value="scores" {'selected' if fmt == 'scores' else ''}>scores</option>
        </select>
        <br>

        <!-- Download-Option: nur sichtbar wenn ali oder scores gewählt -->
        <div id="download_row" style="margin-top:8px; {'display:block' if fmt in ('ali','scores') else 'display:none'}">
            <input type="checkbox" name="download_output" id="download_output" {'checked' if download_output else ''}>
            <label for="download_output">Ergebnis als Datei herunterladen</label>
        </div>
        <br>

        <p>Algorithm:</p>
        <select name="use_nw" onchange="switchGap(this.value)">
            <option value="gotoh" {'selected' if use_nw == 'gotoh' else ''}>Gotoh</option>
            <option value="nw"    {'selected' if use_nw == 'nw'    else ''}>Needleman-Wunsch / Smith-Waterman</option>
        </select>
        <br>

        <div id="gap_open" style="{style_go}">
            <p>Gap Open:</p>
            <input type="text" name="go" value="{go}">
        </div>
        <div id="gap_extend">
            <p>Gap Extension:</p>
            <input type="text" name="ge" value="{ge}">
        </div>
        <br>

        <input type="checkbox" name="show_dp" id="show_dp" {'checked' if show_dp else ''}>
        <label for="show_dp">DP-Matrix &amp; Fixed Point anzeigen</label>
        <br><br>

        <input type="submit" value="Calculate Alignment">
    </form>

    <h2>Final Alignment</h2>
""")

# Fehlermeldungen ausgeben
if file_error:   print(f'<p class="error">{file_error}</p>')
if text_error:   print(f'<p class="error">{text_error}</p>')
if native_error: print(f'<p class="error">{native_error}</p>')

# ── DB-Abfrage für PDB (nach HTML) ──────────────────────────
pdb_error = ""
if input_type == "pdb" and pdb1_input:
    try:
        db = mysql.connector.connect(
            host="mysql2-ext.bio.ifi.lmu.de",
            port=3306,
            user="bioprakt15",
            password="$1$/NQ9xkkh$BnZDjreVX/1q0MGqWEc3M0",
            database="bioprakt15"
        )
        cursor = db.cursor()
        cursor.execute("SELECT sequence FROM homestead WHERE pdb = %s", (pdb1_input.lower(),))
        row = cursor.fetchone()
        seq1 = row[0] if row else None
        cursor.execute("SELECT sequence FROM homestead WHERE pdb = %s", (pdb2_input.lower(),))
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

# ── Java starten ─────────────────────────────────────────────
output = None
can_run = not any([file_error, text_error, native_error, pdb_error])

if can_run and submitted:
    # Für text/file/pdb: pairs+seqlib schreiben. Native: schon geschrieben.
    if not use_native:
        if seq1 and seq2:
            try:
                with open(pairs_file, "w") as f:
                    f.write(f"{id1} {id2}\n")
                with open(seqlib_file, "w") as f:
                    f.write(f"{id1}:{seq1}\n")
                    f.write(f"{id2}:{seq2}\n")
            except Exception as e:
                print(f'<p class="error">ERROR: Konnte Eingabedateien nicht schreiben: {e}</p>')
                can_run = False
        else:
            can_run = False

    if can_run:
        try:
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
    print(output.stdout)
    print("</pre>")
    print("<h2>Benchmark</h2>")
    print("<img src='benchmark.png'>")

print("</body>\n</html>")

# ── DP-Matrix & Fixed Point (optional) ──────────────────────
if show_dp and output and can_run:
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