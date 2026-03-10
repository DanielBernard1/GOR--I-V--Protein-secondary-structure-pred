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


seq1 = ""
seq2 = ""
id1  = ""
id2  = ""

if input_type == "pdb" and "pdb1" in form and form["pdb1"].value.strip():
    id1 = form["pdb1"].value
    id2 = form["pdb2"].value
    seq1 = get_sequence_from_db(id1)
    seq2 = get_sequence_from_db(id2)
    if seq1 is None or seq2 is None:
        print("<p class='error-msg'>ERROR: PDB-ID not found</p>")
        seq1 = ""
        seq2 = ""
        id1  = ""
        id2  = ""

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
        print("<p class='error-msg'>ERROR: Not enough sequences in the file. Or Wrong File</p>")
    id1, seq1 = entries[0]
    id2, seq2 = entries[1]
else:
    seq1 = form["seq1"].value if "seq1" in form else ""
    seq2 = form["seq2"].value if "seq2" in form else ""
    if submitted and (not seq1 or not seq2):
        print("<p class='error-msg'>Fehler: Pls insert a seq</p>")
    id1 = form["id1"].value if "id1" in form else ""
    id2 = form["id2"].value if "id2" in form else ""

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

go = form["go"].value if "go" in form and form["go"].value else "-11"
ge = form["ge"].value if "ge" in form and form["ge"].value else "-1"

if "show_dp" in form:
    show_dp = True
else:
    show_dp = False

if "use_nw" in form:
    use_nw = form["use_nw"].value
else:
    use_nw = "gotoh"

style_go = "display:none;" if use_nw == "nw" else "display:block;"

alignment_jar = "../finaljars/alignment.jar"
matrix_path   = "/home/m/martinla/public_html/propragruppe15/Solution3/Alignment/matrices/" + matrix
seqlib_file   = "seqlib.txt"
pairs_file    = "pairs.txt"

if seq1 and seq2:
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


print(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Sequence Alignment</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --green:      #2e7d52;
            --green-dk:   #1f5c3a;
            --green-lt:   #4caf80;
            --green-bg:   #edf7f2;
            --green-mid:  #c5ddd0;
            --text:       #1c2b1e;
            --text-dim:   #5a7060;
            --border:     #c5ddd0;
            --bg:         #f2f8f4;
            --white:      #ffffff;
        }}
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Inter', sans-serif;
            font-size: 15px;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}
        nav {{
            background: var(--white);
            border-bottom: 2px solid var(--green-mid);
            padding: 0 32px;
            display: flex;
            align-items: center;
            gap: 32px;
            height: 54px;
            position: sticky;
            top: 0;
            z-index: 10;
            box-shadow: 0 1px 6px rgba(30,80,50,0.07);
        }}
        .nav-logo {{
            font-weight: 600; font-size: 0.95rem;
            color: var(--green); letter-spacing: 0.01em;
            display: flex; align-items: center; gap: 8px; white-space: nowrap;
        }}
        .nav-links {{ display: flex; gap: 4px; list-style: none; }}
        .nav-links a {{
            text-decoration: none; font-size: 0.85rem; font-weight: 500;
            color: var(--text-dim); padding: 6px 13px; border-radius: 6px; transition: all 0.15s;
        }}
        .nav-links a:hover {{ background: var(--green-bg); color: var(--green); }}
        .nav-links a.active {{ background: var(--green); color: white; }}
        .page-header {{
            background: linear-gradient(135deg, #1a4d2e 0%, #2e7d52 60%, #3a9668 100%);
            padding: 34px 40px 30px; color: white;
        }}
        .page-header h1 {{ font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em; margin-bottom: 5px; }}
        .page-header p {{ font-size: 0.87rem; opacity: 0.8; font-weight: 300; }}
        .header-deco {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem; opacity: 0.22; letter-spacing: 0.15em;
            margin-top: 14px; overflow: hidden; white-space: nowrap;
        }}
        .page-wrapper {{ max-width: 900px; margin: 0 auto; padding: 26px 24px 80px; }}
        .section-label {{
            font-size: 0.7rem; font-weight: 600; letter-spacing: 0.14em;
            text-transform: uppercase; color: var(--green);
            margin-bottom: 10px; margin-top: 24px;
            display: flex; align-items: center; gap: 8px;
        }}
        .section-label::after {{
            content: ''; flex: 1; height: 1px; background: var(--green-mid);
        }}
        .card {{
            background: var(--white); border: 1px solid var(--border);
            border-radius: 8px; padding: 22px 24px; margin-bottom: 14px;
            box-shadow: 0 1px 4px rgba(30,80,50,0.07);
        }}
        .method-buttons {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 6px; }}
        .method-btn {{
            font-family: 'Inter', sans-serif; font-size: 0.85rem; font-weight: 500;
            padding: 8px 16px; border: 1.5px solid var(--border); border-radius: 6px;
            background: var(--white); color: var(--text-dim); cursor: pointer; transition: all 0.15s;
        }}
        .method-btn:hover {{ border-color: var(--green-lt); color: var(--green); background: var(--green-bg); }}
        .method-btn.active {{ border-color: var(--green); background: var(--green); color: white; }}
        .field-label {{
            display: block; font-size: 0.78rem; font-weight: 500;
            color: var(--text-dim); margin-bottom: 5px; margin-top: 14px;
        }}
        input[type=text], textarea, select {{
            width: 100%; padding: 9px 12px;
            background: var(--white); border: 1.5px solid var(--border);
            border-radius: 6px; color: var(--text);
            font-family: 'Inter', sans-serif; font-size: 0.9rem;
            transition: border-color 0.15s, box-shadow 0.15s;
            outline: none; appearance: none;
        }}
        input[type=text]:focus, textarea:focus, select:focus {{
            border-color: var(--green);
            box-shadow: 0 0 0 3px rgba(46,125,82,0.12);
        }}
        textarea {{
            font-family: 'JetBrains Mono', monospace; font-size: 0.8rem;
            resize: vertical; min-height: 72px; background: #fafcfb;
        }}
        select {{
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'%3E%3Cpath fill='%235a7060' d='M5 6L0 0h10z'/%3E%3C/svg%3E");
            background-repeat: no-repeat; background-position: right 12px center;
            padding-right: 32px; cursor: pointer;
        }}
        input[type=file] {{ color: var(--text-dim); font-size: 0.88rem; padding: 8px 0; }}
        .param-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0 24px; }}
        .checkbox-row {{
            display: flex; align-items: center; gap: 9px;
            margin-top: 16px; color: var(--text-dim); font-size: 0.88rem;
        }}
        input[type=checkbox] {{ accent-color: var(--green); width: 15px; height: 15px; cursor: pointer; }}
        input[type=submit] {{
            margin-top: 20px; padding: 11px 28px;
            background: var(--green); color: white;
            font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.9rem;
            border: none; border-radius: 6px; cursor: pointer; transition: background 0.15s;
        }}
        input[type=submit]:hover {{ background: var(--green-dk); }}
        .result-bar {{
            background: var(--green); color: white; padding: 10px 20px;
            font-size: 0.76rem; font-weight: 600; letter-spacing: 0.08em;
            text-transform: uppercase; border-radius: 8px 8px 0 0;
            display: flex; align-items: center; gap: 10px;
        }}
        .result-dot {{
            width: 7px; height: 7px; border-radius: 50%;
            background: #a8efd0; box-shadow: 0 0 6px #a8efd0;
        }}
        /* pre.result ist NUR fuer ali/scores — Java-HTML bekommt keinen wrapper */
        pre.result {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem; line-height: 1.7;
            white-space: pre; overflow-x: auto;
            background: #f7fbf8;
            border: 1.5px solid var(--border); border-top: none;
            border-radius: 0 0 8px 8px;
            padding: 20px 24px;
            /* kein 'color' hier damit Java-HTML span-Farben nicht ueberschrieben werden */
        }}
        .error-msg {{
            background: #fff5f5; border: 1px solid #f0a0a0;
            border-radius: 6px; padding: 10px 14px;
            color: #c0392b; font-size: 0.88rem; margin: 10px 0;
        }}
        img {{ max-width: 100%; border-radius: 6px; border: 1px solid var(--border); margin-top: 12px; }}
        hr {{ border: none; border-top: 1px solid var(--border); margin: 24px 0; }}
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
        document.getElementById('input_type_hidden').value = type;
        document.querySelectorAll('.method-btn').forEach(b => b.classList.remove('active'));
        event.target.classList.add('active');
    }}
    function switchGap(algo) {{
        document.getElementById('gap_open').style.display = algo === 'gotoh' ? 'block' : 'none';
    }}
    window.onload = function() {{
        switchGap(document.querySelector('select[name=use_nw]').value);
    }};
    </script>
</head>
<body onload="switchGap(document.querySelector('select[name=use_nw]').value)">

<nav>
    <div class="nav-logo">
        <svg width="20" height="20" viewBox="0 0 22 22" fill="none">
            <ellipse cx="11" cy="11" rx="4" ry="10" stroke="#2e7d52" stroke-width="1.8" fill="none"/>
            <ellipse cx="11" cy="11" rx="10" ry="4" stroke="#4caf80" stroke-width="1.8" fill="none"/>
            <circle cx="11" cy="11" r="2" fill="#2e7d52"/>
        </svg>
        BioAnalysis Suite
    </div>
    <ul class="nav-links">
        <li><a href="#">Home</a></li>
        <li><a href="#">Sequence</a></li>
        <li><a href="#">SwissProt</a></li>
        <li><a href="#">Structure</a></li>
        <li><a href="#">GOR</a></li>
        <li><a href="#" class="active">Alignment</a></li>
        <li><a href="#">Help</a></li>
    </ul>
</nav>

<div class="page-header">
    <h1>Pairwise Sequence Alignment</h1>
    <p>Gotoh · Needleman-Wunsch · Smith-Waterman &nbsp;|&nbsp; Global · Local · Freeshift</p>
    <div class="header-deco">MVLSPADKTNVKAAWGKV--GAHAGEYGAEALERMFLSFPTTKTYFPHF · · · MVHLTPEEKSAVTALWGKVNVDEVGG</div>
</div>

<div class="page-wrapper">
    <form method="post" enctype="multipart/form-data" action="Alignment_CGI.py">
        <input type="hidden" name="input_type" id="input_type_hidden" value="{input_type}">

        <p class="section-label">Input</p>
        <div class="card">
            <div class="method-buttons">
                <input type="button" class="method-btn {'active' if input_type == 'text' else ''}" value="Enter Sequences" onclick="switchInput('text')">
                <input type="button" class="method-btn {'active' if input_type == 'file' else ''}" value="FASTA File"       onclick="switchInput('file')">
                <input type="button" class="method-btn {'active' if input_type == 'pdb'  else ''}" value="Database (PDB)"   onclick="switchInput('pdb')">
            </div>

            <div id="input_text" style="{style_text}">
                <div class="param-grid">
                    <div>
                        <label class="field-label">ID 1</label>
                        <input type="text" name="id1" value="{id1}">
                    </div>
                    <div>
                        <label class="field-label">ID 2</label>
                        <input type="text" name="id2" value="{id2}">
                    </div>
                </div>
                <label class="field-label">Sequence 1</label>
                <textarea name="seq1" rows="3">{seq1}</textarea>
                <label class="field-label">Sequence 2</label>
                <textarea name="seq2" rows="3">{seq2}</textarea>
            </div>

            <div id="input_file" style="{style_file}">
                <label class="field-label">FASTA File (min. 2 sequences)</label>
                <input type="file" name="seqfile" accept=".fasta,.fa,.txt">
            </div>

            <div id="input_pdb" style="{style_pdb}">
                <div class="param-grid">
                    <div>
                        <label class="field-label">PDB-ID 1</label>
                        <input type="text" name="pdb1" placeholder="e.g. 1HBA">
                    </div>
                    <div>
                        <label class="field-label">PDB-ID 2</label>
                        <input type="text" name="pdb2" placeholder="e.g. 2HBB">
                    </div>
                </div>
            </div>
        </div>

        <p class="section-label">Parameters</p>
        <div class="card">
            <div class="param-grid">
                <div>
                    <label class="field-label">Substitution Matrix</label>
                    <select name="matrix">
                        <option value="dayhoff.mat"          {'selected' if matrix == 'dayhoff.mat'          else ''}>Dayhoff</option>
                        <option value="blosum62.mat"          {'selected' if matrix == 'blosum62.mat'          else ''}>BLOSUM62</option>
                        <option value="pam250.mat"            {'selected' if matrix == 'pam250.mat'            else ''}>PAM250</option>
                        <option value="BlakeCohenMatrix.mat"  {'selected' if matrix == 'BlakeCohenMatrix.mat'  else ''}>BlakeCohenMatrix</option>
                    </select>
                </div>
                <div>
                    <label class="field-label">Alignment Mode</label>
                    <select name="mode">
                        <option value="global"    {'selected' if mode == 'global'    else ''}>Global</option>
                        <option value="local"     {'selected' if mode == 'local'     else ''}>Local</option>
                        <option value="freeshift" {'selected' if mode == 'freeshift' else ''}>Freeshift</option>
                    </select>
                </div>
                <div>
                    <label class="field-label">Output Format</label>
                    <select name="format">
                        <option value="html"   {'selected' if fmt == 'html'   else ''}>HTML</option>
                        <option value="ali"    {'selected' if fmt == 'ali'    else ''}>ALI</option>
                        <option value="scores" {'selected' if fmt == 'scores' else ''}>Scores</option>
                    </select>
                </div>
                <div>
                    <label class="field-label">Algorithm</label>
                    <select name="use_nw" onchange="switchGap(this.value)">
                        <option value="gotoh" {'selected' if use_nw == 'gotoh' else ''}>Gotoh</option>
                        <option value="nw"    {'selected' if use_nw == 'nw'    else ''}>Needleman-Wunsch / Smith-Waterman</option>
                    </select>
                </div>
                <div id="gap_open" style="{style_go}">
                    <label class="field-label">Gap Open</label>
                    <input type="text" name="go" value="{go}">
                </div>
                <div>
                    <label class="field-label">Gap Extension</label>
                    <input type="text" name="ge" value="{ge}">
                </div>
            </div>
            <div class="checkbox-row">
                <input type="checkbox" name="show_dp" id="show_dp" {'checked' if show_dp else ''}>
                <label for="show_dp">Show DP Matrix &amp; Fixed Point Alignment</label>
            </div>
        </div>

        <input type="submit" value="Calculate Alignment">
    </form>

    <hr>
    <p class="section-label">Result</p>
""")

if output:
    if fmt == "html":
        # Java gibt ein komplettes HTML-Dokument aus — direkt ausgeben, kein wrapper
        print(output.stdout)
    else:
        print(f'<div class="result-bar"><span class="result-dot"></span>Mode: {mode} &nbsp;·&nbsp; Matrix: {matrix} &nbsp;·&nbsp; {use_nw}</div>')
        print('<pre class="result">')
        print(output.stdout)
        print('</pre>')

print("""
</div>

<footer>
    <span>BioAnalysis Suite &mdash; Bioinformatics Practical &middot; Group 15</span>
    <span>Sequence Alignment</span>
</footer>

</body>
</html>
""")

dp_path = "/home/m/martinla/public_html/propragruppe15/Solution3/Alignment/dp/"

if show_dp and seq1 and seq2:
    cmd_dp = ["java", "-jar", alignment_jar,
              "--pairs", pairs_file, "--seqlib", seqlib_file,
              "-m", matrix_path, "--mode", mode,
              "--go", go, "--ge", ge, "--format", fmt,
              "--dpmatrices", dp_path]
    if use_nw == "nw":
        cmd_dp.append("--nw")
    subprocess.run(cmd_dp, capture_output=True, text=True)

    dp_vis = subprocess.run(["python3", "../dp_matrix.py", dp_path], capture_output=True, text=True)
    print('<p class="section-label">DP Matrix</p>')
    print(f'<pre class="result">{dp_vis.stdout}</pre>')

    fp_file = dp_path + "fixedpoint_" + id1 + "_" + id2 + ".txt"
    fp_png  = dp_path + "fixedpoint_" + id1 + "_" + id2 + ".png"
    subprocess.run(["python3", "FixPoint.py", fp_file, fp_png])
    print('<p class="section-label">Fixed Point Alignment</p>')
    print(f"<img src='https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution3/Alignment/dp/fixedpoint_{id1}_{id2}.png'>")