#!/usr/bin/biopython
# quelle w3school html-tutorial
import re
# Autor Laura Martin+
import subprocess
import mycgi
import mysql.connector
import sys


form = mycgi.Form()

print("Content-type: text/html\n")


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
show_fp = "show_fp" in form

if "ss" in form:
    use_ss = form["ss"].value
else:
    use_ss = "none"

if use_nw == "nw":
    style_go = "display: none;"
else:
    style_go = "display: block;"

file_error = ""
native_error = ""
text_error = ""
pdb_error = ""
java_error = ""

#FASTA-FILE!!!!
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

use_native   = False
if input_type == "native":
    pairs_ok  = "pairs_file"  in form and hasattr(form["pairs_file"],  "file") and form["pairs_file"].filename
    seqlib_ok = "seqlib_file" in form and hasattr(form["seqlib_file"], "file") and form["seqlib_file"].filename
    if not pairs_ok or not seqlib_ok:
        native_error = "ERROR: Upload both Files(pairs.txt and seqlib.txt)."
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
                id1 = first_pair[0]
                id2 = first_pair[1]
        except Exception as e:
            native_error = f"ERROR: Can't read file{e}"

# pdb_error hier initialisieren damit Java-Bedingung unten funktioniert

if input_type == "text" and submitted and (not seq1 or not seq2):
    text_error = "ERROR: Please insert both sequences."

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
        if row:
            seq2 = row[0]
        else:
            seq2 = None
        id1 = pdb1_input
        id2 = pdb2_input
        db.close()
        if not seq1 or not seq2:
            pdb_error = f"ERROR: PDB-ID not found ('{pdb1_input}' or '{pdb2_input}' are not part of the Database)"
            seq1 = ""
            seq2 = ""
    except Exception as e:
        pdb_error = f"ERROR: No connection to the Database {e}"
        seq1 = ""
        seq2 = ""

#Fehler bei manueller Eingabe
if input_type == "text" and submitted and (not seq1 or not seq2):
    text_error = "ERROR: Please insert both sequences."



# Java starten
alignment_jar = "../finaljars/alignment.jar"
matrix_path = "/home/m/martinla/public_html/propragruppe15/Solution3/Alignment/matrices/" + matrix
seqlib_file = "seqlib.txt"
pairs_file = "pairs.txt"

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
        if use_ss:
            cmd.append("--ss")

        output = subprocess.run(cmd, capture_output=True, text=True)
    except Exception as e:
        print(f'<p class="error">ERROR: Java konnte nicht gestartet werden: {e}</p>')



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
    print("Content-Type: text/plain")
    print(f"Content-Disposition: attachment; filename=\"{filename}\"") #??????????????????????????
    print()
    print(output.stdout)
    sys.exit(0)




# HTML ZUERST DRUCKEN

print(f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Alignment — propraGruppe15</title>

    <!-- DESIGN: gleiche Fonts wie index.html -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

    <style>
        /* DESIGN: gleiche CSS-Variablen wie index.html */
        :root {{
            --green:     #2e7d52;
            --green-dk:  #1f5c3a;
            --green-lt:  #4caf80;
            --green-bg:  #edf7f2;
            --green-mid: #c5ddd0;
            --text:      #1c2b1e;
            --text-dim:  #5a7060;
            --border:    #c5ddd0;
            --bg:        #f2f8f4;
            --white:     #ffffff;
        }}
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Inter', sans-serif;
            font-size: 15px;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}

        /* DESIGN: sticky Navbar identisch mit index.html */
        nav {{
            background: var(--white);
            border-bottom: 2px solid var(--green-mid);
            padding: 0 32px;
            display: flex; align-items: center; gap: 32px;
            height: 54px; position: sticky; top: 0; z-index: 10;
            box-shadow: 0 1px 6px rgba(30,80,50,0.07);
        }}
        .nav-logo {{
            font-weight: 600; font-size: 0.95rem; color: var(--green);
            display: flex; align-items: center; gap: 8px;
            white-space: nowrap; text-decoration: none;
        }}
        .nav-links {{ display: flex; gap: 4px; list-style: none; }}
        .nav-links a {{
            text-decoration: none; font-size: 0.85rem; font-weight: 500;
            color: var(--text-dim); padding: 6px 13px; border-radius: 6px; transition: all 0.15s;
        }}
        .nav-links a:hover  {{ background: var(--green-bg); color: var(--green); }}
        .nav-links a.active {{ background: var(--green); color: white; }}

        /* DESIGN: grüner Page-Header mit Algorithmen-Untertitel (alignment-spezifisch) */
        .page-header {{
            background: var(--green);
            padding: 32px 40px 28px; color: white;
        }}
        .page-header h1 {{ font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em; margin-bottom: 4px; }}
        .page-header p  {{ font-size: 0.87rem; opacity: 0.82; font-weight: 300; }}

        /* DESIGN: Sequenz-Dekorationszeile (alignment-spezifisch) */
        .seq-deco {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem; opacity: 0.22; letter-spacing: 0.12em;
            margin-top: 14px; overflow: hidden; white-space: nowrap;
        }}

        /* DESIGN: zentrierter Wrapper wie index.html */
        .page-wrapper {{ max-width: 900px; margin: 0 auto; padding: 24px 24px 80px; }}

        /* DESIGN: section-label mit Trennlinie wie index.html */
        .section-label {{
            font-size: 0.7rem; font-weight: 600; letter-spacing: 0.14em;
            text-transform: uppercase; color: var(--green);
            margin-bottom: 10px; margin-top: 24px;
            display: flex; align-items: center; gap: 8px;
        }}
        .section-label::after {{ content: ''; flex: 1; height: 1px; background: var(--green-mid); }}

        /* DESIGN: weiße Cards mit Schatten wie index.html */
        .card {{
            background: var(--white); border: 1px solid var(--border);
            border-radius: 8px; padding: 22px 24px; margin-bottom: 14px;
            box-shadow: 0 1px 4px rgba(30,80,50,0.07);
        }}

        /* DESIGN: field-label über Eingabefeldern wie index.html */
        .field-label {{
            display: block; font-size: 0.78rem; font-weight: 500;
            color: var(--text-dim); margin-bottom: 5px; margin-top: 14px;
        }}

        /* DESIGN: einheitliche Inputs mit grünem Focus-Ring */
        input[type=text], select {{
            width: 100%; padding: 9px 12px;
            background: var(--white); border: 1.5px solid var(--border);
            border-radius: 6px; color: var(--text);
            font-family: 'Inter', sans-serif; font-size: 0.9rem;
            transition: border-color 0.15s, box-shadow 0.15s;
            outline: none; appearance: none;
        }}
        input[type=text]:focus, select:focus {{
            border-color: var(--green);
            box-shadow: 0 0 0 3px rgba(46,125,82,0.1);
        }}

        /* DESIGN: Monospace + grünlicher Hintergrund für Sequenz-Textareas (alignment-spezifisch) */
        textarea {{
            width: 100%; padding: 9px 12px;
            background: #f6fdf9; border: 1.5px solid var(--border);
            border-radius: 6px; color: var(--text);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem; resize: vertical; min-height: 72px;
            transition: border-color 0.15s, box-shadow 0.15s; outline: none;
        }}
        textarea:focus {{ border-color: var(--green); box-shadow: 0 0 0 3px rgba(46,125,82,0.1); }}

        /* DESIGN: custom Select-Pfeil */
        select {{
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'%3E%3Cpath fill='%235a7060' d='M5 6L0 0h10z'/%3E%3C/svg%3E");
            background-repeat: no-repeat; background-position: right 12px center;
            padding-right: 32px; cursor: pointer;
        }}

        /* DESIGN: Input-Typ Buttons als Outline-Buttons */
        input[type=button] {{
            font-family: 'Inter', sans-serif; font-size: 0.85rem; font-weight: 500;
            padding: 8px 16px; border: 1.5px solid var(--border); border-radius: 6px;
            background: var(--white); color: var(--text-dim);
            cursor: pointer; transition: all 0.15s; margin-right: 8px; margin-bottom: 6px;
        }}
        input[type=button]:hover {{ border-color: var(--green-lt); color: var(--green); background: var(--green-bg); }}

        /* DESIGN: grüner Submit-Button */
        input[type=submit] {{
            margin-top: 20px; padding: 11px 28px;
            background: var(--green); color: white;
            font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.9rem;
            border: none; border-radius: 6px; cursor: pointer; transition: background 0.15s;
        }}
        input[type=submit]:hover {{ background: var(--green-dk); }}

        /* DESIGN: Checkbox grün */
        input[type=checkbox] {{ accent-color: var(--green); width: 15px; height: 15px; cursor: pointer; }}
        .checkbox-row {{ display: flex; align-items: center; gap: 9px; margin-top: 14px; font-size: 0.88rem; color: var(--text-dim); }}

        /* DESIGN: 2-spaltiges Grid für Parameter */
        .param-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0 24px; }}

        /* DESIGN: Fehlerbox */
        .error {{
            color: #c0392b; font-weight: 500; padding: 10px 14px;
            background: #fff5f5; border: 1px solid #f0a0a0;
            border-radius: 6px; margin: 10px 0; font-size: 0.88rem;
        }}

        /* DESIGN: Result-Bar (alignment-spezifisch) — grüner Header über dem Ergebnis */
        .result-bar {{
            background: var(--green); color: white;
            padding: 9px 18px; font-size: 0.75rem; font-weight: 600;
            letter-spacing: 0.08em; text-transform: uppercase;
            border-radius: 8px 8px 0 0;
            display: flex; align-items: center; gap: 10px;
        }}
        .result-dot {{ width: 7px; height: 7px; border-radius: 50%; background: #a8efd0; }}

        /* DESIGN: pre für Ergebnis-Output (alignment-spezifisch)
           KEIN color — Java-HTML nutzt eigene span-Farben für Matches */
        pre.result {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem; line-height: 1.7;
            white-space: pre; overflow-x: auto;
            background: #f7fbf8;
            border: 1.5px solid var(--border); border-top: none;
            border-radius: 0 0 8px 8px; padding: 20px 24px;
        }}

        /* DESIGN: img mit grünem Border für Plots */
        img {{ max-width: 100%; border-radius: 6px; border: 1px solid var(--border); margin-top: 12px; }}

        hr {{ border: none; border-top: 1px solid var(--border); margin: 20px 0; }}

        /* DESIGN: Footer wie index.html */
        footer {{
            background: var(--white); border-top: 1px solid var(--border);
            padding: 14px 40px; font-size: 0.78rem; color: var(--text-dim);
            display: flex; justify-content: space-between; margin-top: 40px;
        }}
    </style>

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

<!-- DESIGN: Navbar mit Zurück-Link zur Hauptseite -->
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
        <!-- Home-Link: zurück zur Hauptseite -->
        <li><a href="https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution1/Assignment03/aufgabe3_2_0.html">Home</a></li>
        <li><a href="https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution3/GOR/Test.py">GOR</a></li>
        <!-- class="active": markiert die aktuelle Seite -->
        <li><a href="Alignment_CGI.py" class="active">Alignment</a></li>
    </ul>
</nav>

<!-- DESIGN: grüner Header mit Algorithmen-Untertitel und Sequenz-Deko -->
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
            <label class="field-label">FASTA-Datei (min. 2 Sequences - first ones get aligned)</label>
            <input type="file" name="seqfile">
        </div>

        <div id="input_pdb" style="{style_pdb}">
            <div class="param-grid">
                <div>
                    <label class="field-label">PDB-ID 1</label>
                    <input type="text" name="pdb1" value="{pdb1_input}" placeholder="z.B. 1hba">
                </div>
                <div>
                    <label class="field-label">PDB-ID 2</label>
                    <input type="text" name="pdb2" value="{pdb2_input}" placeholder="z.B. 2hbb">
                </div>
            </div>
        </div>

        <div id="input_native" style="{style_native}">
            <label class="field-label">pairs.txt</label>
            <input type="file" name="pairs_file" accept=".txt">
            <label class="field-label">seqlib.txt</label>
            <input type="file" name="seqlib_file" accept=".txt">

        </div>

    </div>

    <p class="section-label">Parameters</p>
    <div class="card">
        <div class="param-grid">
            <div>
                <label class="field-label">Matrix</label>
                <select name="matrix">
                    <option value="dayhoff.mat"         {'selected' if matrix == 'dayhoff.mat' else ''}><p>dayhoff</p></option>
                    <option value="BlakeCohenMatrix.mat" {'selected' if matrix == 'BlakeCohenMatrix.mat' else ''}><p>BlakeCohenMatrix</p></option>
                    <option value="blosum62.mat"         {'selected' if matrix == 'blosum62.mat' else ''}><p>BLOSUM62</p></option>
                    <option value="pam250.mat"           {'selected' if matrix == 'pam250.mat' else ''}><p>pam250</p></option>
                </select>
            </div>
            <div>
                <label class="field-label">Mode</label>
                <select name="mode">
                    <option value="global"    {'selected' if mode == 'global' else ''}><p>global</p></option>
                    <option value="local"     {'selected' if mode == 'local' else ''}><p>local</p></option>
                    <option value="freeshift" {'selected' if mode == 'freeshift' else ''}><p>freeshift</p></option>
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
            <label for="show_dp">show DP-Matrix</label>
        </div>
        
        <div class="checkbox-row">
            <input type="checkbox" name="show_Fixpoint" id="show_FP" {'checked' if show_fp else ''}>
            <label for="show_FP">Show FixedPoint-Graphics</label>
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

if java_error:
    print (f"<p class='error'>{java_error}</p>")

if output:

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
        print(
            f'<div class="result-bar"><span class="result-dot"></span>Mode: {mode} &nbsp;&middot;&nbsp; Matrix: {matrix} &nbsp;&middot;&nbsp; {use_nw}</div>')
        print('<pre class="result">')
        print(java_out)
        print('</pre>')

    print('<p class="section-label">Graphics</p>')
    #print("<img src='benchmark.png'>")

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

        dp_file = dp_path + "dp_matrix_" + id1 + "_" + id2 + ".txt"
        dp_png = dp_path + "dp_matrix_" +id1 + "_" + id2 + ".png"
        scoring_matrix_file = dp_path + "scoring_matrix.txt"
        traceback_file = dp_path + "traceback_index.txt"

        dp_vis = subprocess.run(["python3", "../dp_matrix.py", scoring_matrix_file, traceback_file, dp_png], capture_output=True, text=True)

        print("<div><h2>DP-Matrix:</h2>")
        print(f"<img src='https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution3/Alignment/dp/dp_matrix_{id1}_{id2}.png'>")

        print("</div>")

    except Exception as e:
        print(f"<p class='error'>DP-Matrix ERROR: {e}</p>")

if show_fp and seq1 and seq2 and output:
    try:
        fp_file = dp_path + "fixedpoint_" + id1 + "_" + id2 + ".txt"
        fp_png = dp_path + "fixedpoint_" + id1 + "_" + id2 + ".png"
        subprocess.run(["python3", "FixPoint.py", fp_file, fp_png], capture_output=True, text=True)
        print("<h2>Fixed Point Alignment</h2>")
        print(
            f"<img src='https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution3/Alignment/dp/fixedpoint_{id1}_{id2}.png'>")
    except Exception as e:
        print(f"<p class='error'>Fixed Point ERROR: {e}</p>")

print("""
</div>

<footer>
    <span>propraGruppe15 &mdash; Bioinformatik-Praktikum &middot; Gruppe 15</span>
    <span>Alignment</span>
</footer>

</body>
</html>
""")