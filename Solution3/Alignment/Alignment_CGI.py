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
style_pdb  = "display: block;" if input_type == "pdb"  else "display: none;"

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
text_error = ""
if input_type == "text" and submitted and (not seq1 or not seq2):
    text_error = "Fehler: Bitte beide Sequenzen eingeben."



# HTML ZUERST DRUCKEN --> Seite immer sichtbar
# auch wenn Fehker geworfen wird

print(f"""<!DOCTYPE html>
<html>
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
    <nav>
        <a class="nav-logo" href="https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/index.html">
            <svg viewBox="0 0 22 22" fill="none" width="20" height="20">
                <ellipse cx="11" cy="11" rx="4"  ry="10" stroke="#2e7d52" stroke-width="1.8" fill="none"/>
                <ellipse cx="11" cy="11" rx="10" ry="4"  stroke="#4caf80" stroke-width="1.8" fill="none"/>
                <circle  cx="11" cy="11" r="2"           fill="#2e7d52"/>
            </svg>
            propraGruppe15
        </a>
        <ul class="nav-links">
            <!-- Home-Link: zurück zur Hauptseite -->
            <li><a href="https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/index.html">Home</a></li>
            <li><a href="https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution3/GOR/GOR_CGI.py">GOR</a></li>
            <!-- class="active": markiert die aktuelle Seite -->
            <li><a href="Alignment_CGI.py" class="active">Alignment</a></li>
        </ul>
    </nav>
    
    
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
if seq1 and seq2 and not file_error and not text_error and not pdb_error:
    try:
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

print("</body>\n</html>")

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