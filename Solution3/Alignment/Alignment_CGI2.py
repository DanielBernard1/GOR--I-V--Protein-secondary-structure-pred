#!/usr/bin/biopython
# quelle w3school html-tutorial

# Autor Laura Martin+
import subprocess
import mycgi
import mysql.connector

print("Content-type: text/html\n")

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

seq1 = ""
seq2 = ""
id1 = ""
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
    seq1 = form["seq1"].value
    seq2 = form["seq2"].value
    if not seq1 or not seq2:
        print("<p style='color:red'>Fehler: Pls insert a seq</p>")
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

# if "check" in form:
#    check = True
# else:
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
# Einlesen:
alignment_jar = "../finaljars/alignment.jar"
matrix_path = "/home/m/martinla/public_html/propragruppe15/Solution3/Alignment/matrices/" + matrix
seqlib_file = "seqlib.txt"  # wo sind die sequenzen gespeichert
pairs_file = "pairs.txt"  # welche Sequenzpaare werden allaniert

with open(pairs_file, "w") as f:
    f.write(f"{id1} {id2}\n")

with open(seqlib_file, "w") as f:
    f.write(f"{id1}:{seq1}\n")
    f.write(f"{id2}:{seq2}\n")

# with open("") as f:
#    print("<h3>DP-Matrix:</h3><pre>")
#    print(f.read())
#    print("</pre>")


input = ["java", "-jar", alignment_jar, "--pairs", pairs_file, "--seqlib", seqlib_file,
         "-m", matrix_path, "--mode", mode, "--go", go, "--ge", ge, "--format", fmt]
if use_nw == "nw":
    input.append("--nw")

output = subprocess.run(input, capture_output=True, text=True)

print(f"""<!DOCTYPE html>
<html>
<head>

    <!-- DESIGN 1: Google Fonts
         Neu: Inter fuer UI-Text, JetBrains Mono fuer Sequenzen.
         Gleiche Fonts wie auf index.html. Vorher: Arial fuer alles. -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

    <style>

        /* DESIGN 2: CSS-Variablen
           Neu: zentrale Farbpalette identisch mit index.html (gruen statt blau).
           Ermoeglicht konsistentes Theming auf allen Seiten. */
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

        /* DESIGN 3: body
           Neu: Inter-Font, gruener Seitenhintergrund, kein padding direkt auf body.
           Vorher: font-family: Arial; max-width: 900px; margin: auto; padding: 20px; */
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Inter', sans-serif;
            font-size: 15px;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}

        /* DESIGN 4: Navbar
           Neu: sticky Navbar wie auf index.html mit Logo und Links.
           Vorher: keine Navbar vorhanden. */
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

        /* DESIGN 5: Page-Header — alignment-spezifisch
           Neu: solider gruener Header-Block mit Titel und Untertitel.
           Vorher: nur <h1> mit blauer Unterlinie (color: #2c5f8a; border-bottom: 2px solid #2c5f8a).
           Alignment-spezifisch: der Untertitel nennt die drei Algorithmen. */
        .page-header {{
            background: var(--green);
            padding: 32px 40px 28px; color: white;
        }}
        .page-header h1 {{
            font-size: 1.5rem; font-weight: 600;
            letter-spacing: -0.02em; margin-bottom: 4px;
        }}
        .page-header p {{
            font-size: 0.87rem; opacity: 0.82; font-weight: 300;
        }}

        /* DESIGN 6: Sequenz-Dekorationszeile — alignment-spezifisch
           Neu: eine echte Aminosaeure-Sequenz als blasse Deko-Zeile im Header.
           Das gibt dem Alignment-Tool einen visuellen Wiedererkennungswert
           und erscheint so nur auf dieser Seite, nicht auf index.html. */
        .seq-deco {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem; opacity: 0.22; letter-spacing: 0.12em;
            margin-top: 14px; overflow: hidden; white-space: nowrap;
        }}

        /* DESIGN 7: page-wrapper
           Neu: zentrierter Container mit max-width, wie auf index.html.
           Vorher: padding direkt auf body. */
        .page-wrapper {{ max-width: 900px; margin: 0 auto; padding: 24px 24px 80px; }}

        /* DESIGN 8: section-label
           Neu: kleine gruene Kapitaelchen mit Trennlinie, identisch mit index.html.
           Vorher: <h2> ohne besonderes Styling. */
        .section-label {{
            font-size: 0.7rem; font-weight: 600; letter-spacing: 0.14em;
            text-transform: uppercase; color: var(--green);
            margin-bottom: 10px; margin-top: 24px;
            display: flex; align-items: center; gap: 8px;
        }}
        .section-label::after {{
            content: ''; flex: 1; height: 1px; background: var(--green-mid);
        }}

        /* DESIGN 9: card
           Neu: weisse Karte mit Schatten und Border, identisch mit index.html.
           Vorher: kein card-Konzept, Inhalte direkt im body. */
        .card {{
            background: var(--white); border: 1px solid var(--border);
            border-radius: 8px; padding: 22px 24px; margin-bottom: 14px;
            box-shadow: 0 1px 4px rgba(30,80,50,0.07);
        }}

        /* DESIGN 10: field-label
           Neu: kleine graue Labels ueber jedem Eingabefeld, wie auf index.html.
           Vorher: <p>Id1:</p> als einfacher Absatz. */
        .field-label {{
            display: block; font-size: 0.78rem; font-weight: 500;
            color: var(--text-dim); margin-bottom: 5px; margin-top: 14px;
        }}

        /* DESIGN 11: input[type=text] und select
           Neu: einheitliche Felder mit gruenem Focus-Ring und Border.
           Vorher: padding: 5px; width: 100%; ohne weitere Styles. */
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

        /* DESIGN 12: textarea — alignment-spezifisch
           Neu: JetBrains Mono statt Arial, leicht gruenlicher Hintergrund.
           Alignment-spezifisch: Sequenzeingaben sind biologischer Code,
           Monospace macht Laengen und Luecken direkt sichtbar.
           Vorher: textarea {{ padding: 5px; width: 100%; }} */
        textarea {{
            width: 100%; padding: 9px 12px;
            background: #f6fdf9;
            border: 1.5px solid var(--border); border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem; color: var(--text);
            resize: vertical; min-height: 72px;
            transition: border-color 0.15s, box-shadow 0.15s;
            outline: none;
        }}
        textarea:focus {{
            border-color: var(--green);
            box-shadow: 0 0 0 3px rgba(46,125,82,0.1);
        }}

        /* DESIGN 13: select Pfeil
           Neu: custom SVG-Pfeil in Grau statt Browser-Standard. */
        select {{
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'%3E%3Cpath fill='%235a7060' d='M5 6L0 0h10z'/%3E%3C/svg%3E");
            background-repeat: no-repeat; background-position: right 12px center;
            padding-right: 32px; cursor: pointer;
        }}

        /* DESIGN 14: Buttons (Input-Type-Auswahl)
           Neu: gruene Outline-Buttons statt blauem Vollton.
           Vorher: button {{ background: #2c5f8a; color: white; ... }} */
        input[type=button] {{
            font-family: 'Inter', sans-serif; font-size: 0.85rem; font-weight: 500;
            padding: 8px 16px; border: 1.5px solid var(--border); border-radius: 6px;
            background: var(--white); color: var(--text-dim);
            cursor: pointer; transition: all 0.15s;
            margin-right: 8px; margin-bottom: 6px;
        }}
        input[type=button]:hover {{
            border-color: var(--green-lt); color: var(--green); background: var(--green-bg);
        }}

        /* DESIGN 15: Submit-Button
           Neu: gruen statt blau (#2c5f8a), Inter-Font, abgerundeter.
           Vorher: background: #2c5f8a; color: white; padding: 8px 16px;
                   border: none; border-radius: 4px; */
        input[type=submit] {{
            margin-top: 20px; padding: 11px 28px;
            background: var(--green); color: white;
            font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.9rem;
            border: none; border-radius: 6px; cursor: pointer; transition: background 0.15s;
        }}
        input[type=submit]:hover {{ background: var(--green-dk); }}

        /* DESIGN 16: Result-Bar — alignment-spezifisch
           Neu: gruener Header-Balken ueber dem Ergebnis-Block mit Modus und Matrix-Info.
           Alignment-spezifisch: nirgendwo sonst auf der Seite gibt es einen Ergebnis-Block.
           Vorher: nur <h2>Final Alignment</h2> darueber. */
        .result-bar {{
            background: var(--green); color: white;
            padding: 9px 18px; font-size: 0.75rem; font-weight: 600;
            letter-spacing: 0.08em; text-transform: uppercase;
            border-radius: 8px 8px 0 0;
            display: flex; align-items: center; gap: 10px;
        }}
        /* Alignment-spezifisch: kleiner gruener Punkt als visuelles Signal fuer aktives Ergebnis */
        .result-dot {{
            width: 7px; height: 7px; border-radius: 50%; background: #a8efd0;
        }}

        /* DESIGN 17: pre.result — alignment-spezifisch
           Neu: JetBrains Mono, heller gruenlicher Hintergrund, passender Border.
           KEIN color gesetzt: Java gibt HTML-Output mit eigenen span-Farben aus
           (gruen = Match, orange = Substitution) — die wuerden sonst ueberschrieben.
           Vorher: pre {{ white-space: pre-wrap; overflow-wrap: break-word; }} */
        pre.result {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem; line-height: 1.7;
            white-space: pre; overflow-x: auto;
            background: #f7fbf8;
            border: 1.5px solid var(--border); border-top: none;
            border-radius: 0 0 8px 8px;
            padding: 20px 24px;
            /* KEIN color-Property: Java-HTML-Output nutzt eigene span-Farben
               fuer Matches und Substitutionen — diese muessen sichtbar bleiben */
        }}

        /* DESIGN 18: img
           Neu: abgerundete Ecken + gruener Border fuer Plots (Benchmark, DP-Matrix).
           Vorher: keine img-Styles. */
        img {{
            max-width: 100%; border-radius: 6px;
            border: 1px solid var(--border); margin-top: 12px;
        }}

        /* DESIGN 19: hr
           Neu: dezente Trennlinie in Border-Farbe statt Browser-Standard. */
        hr {{ border: none; border-top: 1px solid var(--border); margin: 20px 0; }}

        /* DESIGN 20: Footer
           Neu: Footer wie auf index.html mit Gruppeninfo.
           Vorher: kein Footer vorhanden. */
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

    <!-- DESIGN 4: Navbar — identisch mit index.html -->
    <nav>
        <a class="nav-logo" href="../index.html">
            <svg viewBox="0 0 22 22" fill="none" width="20" height="20">
                <ellipse cx="11" cy="11" rx="4"  ry="10" stroke="#2e7d52" stroke-width="1.8" fill="none"/>
                <ellipse cx="11" cy="11" rx="10" ry="4"  stroke="#4caf80" stroke-width="1.8" fill="none"/>
                <circle  cx="11" cy="11" r="2"           fill="#2e7d52"/>
            </svg>
            propraGruppe15
        </a>
        <ul class="nav-links">
            <li><a href="../index.html">Home</a></li>
            <li><a href="https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution3/GOR/GOR_CGI.py">GOR</a></li>
            <li><a href="Alignment_CGI2.py" class="active">Alignment</a></li>
        </ul>
    </nav>

    <!-- DESIGN 5+6: Page-Header mit Algorithmen-Untertitel und Sequenz-Deko -->
    <div class="page-header">
        <h1>Alignment</h1>
        <!-- DESIGN 5: Untertitel mit Algorithmen-Namen — alignment-spezifisch -->
        <p>Gotoh &nbsp;&middot;&nbsp; Needleman-Wunsch &nbsp;&middot;&nbsp; Smith-Waterman</p>
        <!-- DESIGN 6: echte Aminosaeure-Sequenz als Deko — nur auf dieser Seite -->
        <div class="seq-deco">MVLSPADKTNVKAAWGKV--GAHAGEYGAEALERMFLSFPTTKTYFPHFD &middot;&middot;&middot; MVHLTPEEKSAVTALWGKVNVDEVGG &middot;&middot;&middot; ACDEFGHIKLMNPQRSTVWY</div>
    </div>

    <!-- DESIGN 7: page-wrapper -->
    <div class="page-wrapper">

    <!-- DESIGN 8+9: section-label + card -->
    <p class="section-label">New Searchrequest</p>
    <div class="card">
    <form method="post" enctype="multipart/form-data" action="Alignment_CGI.py"> 
        <p>Input-Type:</p>
        <p>Own Sequences:</p>
        <!-- DESIGN 14: input[type=button] mit neuem Outline-Stil -->
        <input type="button" value="Enter Sequences manually" onclick="switchInput('text')">
        <p>Upload FastaFile: </p>
        <input type="button" value="Enter Fasta-File" onclick="switchInput('file')">
        <p>Upload PDB-IDs form the Database: </p>
        <input type="button" value="Enter PDB-Ids" onclick="switchInput('pdb')">

        <input type="hidden" name="input_type" id="input_type_hidden" value="{input_type}">
        <br><br>

        <div id="input_text" style="{style_text}">
            <!-- DESIGN 10: field-label statt <p> -->
            <label class="field-label">Id1</label>
            <!-- DESIGN 11: input[type=text] mit gruenem Focus-Ring -->
            <input type="text" name="id1" value="{id1}">
            <label class="field-label">Id2</label>
            <input type="text" name="id2" value="{id2}"><br>
            <!-- DESIGN 12: textarea mit Monospace-Font und gruenem Hintergrund -->
            <label class="field-label">Sequenz 1</label>
            <textarea name="seq1">{seq1}</textarea>
            <label class="field-label">Sequenz 2</label>
            <textarea name="seq2">{seq2}</textarea><br>
        </div>

        <div id="input_file" style="{style_file}">
            <label class="field-label">Upload Fasta-File for multiple Alignments</label>
            <input type="file" name="seqfile" > 
        </div>
        <br><br>

        <div id="input_pdb" style="{style_pdb}">
            <label class="field-label">PDB-ID 1</label>
            <input type="text" name="pdb1" placeholder="z.B. 1HBA">
            <label class="field-label">PDB-ID 2</label>
            <input type="text" name="pdb2" placeholder="z.B. 2HBB">
        </div>
        <br><br>

        <!-- DESIGN 10+11: field-label + select fuer alle Parameter -->
        <label class="field-label">Matrix</label>
        <select name="matrix">
            <option value="dayhoff.mat"> <p>dayhoff</p> </option>
            <option value="BlakeCohenMatrix.mat"> <p>BlakeCohenMatrix</p> </option>
            <option value="blosum62.mat"> <p>BLOSUM62</p> </option>
            <option value="pam250.mat"> <p>pam250</p> </option>
        </select>
        <br><br>

        <label class="field-label">Mode</label>
        <select name="mode">
            <option value="global"> <p>global</p> </option>
            <option value="local"> <p>local</p> </option>
            <option value="freeshift"> <p>freeshift</p> </option>
        </select>
        <br><br>

        <label class="field-label">Output-Format</label>
        <select name="format">
            <option value="html"> <p>html</p> </option>
            <option value="ali"> <p>ali</p> </option>
            <option value="scores"> <p>scores</p> </option>
        </select><br>

        <label class="field-label">Algorithm</label>
        <select name="use_nw" onchange="switchGap(this.value)">
            <option value="gotoh"> <p>Gotoh</p> </option>
            <option value="nw"> <p>Needleman-Wunsch/ Smith-Waterman</p> </option> 
        </select><br>

        <div id="gap_open" style="{style_go}">
            <label class="field-label">Gap Open</label>
            <input type="text" name="go" value="{go}">
        </div>

        <div id="gap_extend">
            <label class="field-label">Gap Extension</label>
            <input type="text" name="ge" value="{ge}">
        </div>
        <br><br>

        <!-- DESIGN 15: gruenem Submit-Button -->
        <input type="submit" value="Calculate Alignment">

    </form>
    </div>

    <hr>

    <!-- DESIGN 8: section-label -->
    <p class="section-label">Final Alignment</p>

    <!-- DESIGN 16: result-bar mit Modus und Matrix-Info (alignment-spezifisch) -->
""")

if output:
    print(mode)
    print("")
    # DESIGN 16+17: result-bar + pre.result statt nacktem <pre>
    print(
        f'<div class="result-bar"><span class="result-dot"></span>Mode: {mode} &nbsp;&middot;&nbsp; Matrix: {matrix}</div>')
    print('<pre class="result">')
    print(output.stdout)
    print(matrix)
    print("")
    print("")
    print('</pre>')
    print("<p class='section-label'>Benchmark</p>")
    # DESIGN 18: img bekommt abgerundete Ecken und Border per CSS
    print("<img src='benchmark.png'>")

print(f"""
    </div>

    <!-- DESIGN 20: Footer -->
    <footer>
        <span>propraGruppe15 &mdash; Bioinformatik-Praktikum &middot; Gruppe 15</span>
        <span>Alignment</span>
    </footer>

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
fp_png = dp_path + "fixedpoint_" + id1 + "_" + id2 + ".png"

subprocess.run(["python3", "FixPoint.py", fp_file, fp_png])
print("<h2>Fixed Point Alignment</h2>")
print(
    f"<img src='https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution3/Alignment/dp/fixedpoint_{id1}_{id2}.png'>")