#!/usr/bin/biopython
import sys
import os

from visualie_cgi import run_visualieze
from train_CGI import run_train
from validate_cgi import run_validate

print("Content-type: text/html\n")

import mycgi
from Website_sec_create import run_seclib
from GOR_cgi import run_predict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
form = mycgi.Form()
action = form.getvalue("action")
output_section = ""
GOR_OUTPUT = os.path.join("uploads/temp_seqAndStructure.txt")


if action == "seclib":
    try:
        output, seclib_path, fasta_path = run_seclib(BASE_DIR, form)
        output_section = f"<textarea readonly rows='10' style='width:100%; resize:both;'>{output}</textarea>"
        output_section += f"<a href={seclib_path} download style='display:inline-block; margin-top:10px; padding:8px 16px; background:#2c3e50; color:white; border-radius:4px;'>Download Seclib</a>"
        if fasta_path:
            output_section += f" <a href='uploads/sec_lib.fasta' download style='display:inline-block; margin-top:10px; padding:8px 16px; background:#2c3e50; color:white; border-radius:4px;'>Download FASTA</a>"
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"

elif action == "predict":
    try:
        output, pp_path = run_predict(BASE_DIR, form)
        output_section += f"<br><br><h3>Prediction Output</h3>"
        output_section = f"<textarea readonly rows='10' style='width:100%; resize:both;'>{output}</textarea>"
        output_section += f"<a href='uploads/temp_seqAndStructure.txt' download style='padding:8px 16px; background:#2c3e50; color:white; border-radius:4px; text-decoration:none; margin-top:10px; display:inline-block;'>Download Prediction</a>"
        if pp_path:

            with open(pp_path) as f:
                pp_content = f.read()
            output_section += f"<br><br><h3>Post-Processed Output</h3>"
            output_section += f"<textarea readonly rows='10' style='width:100%; resize:both;'>{pp_content}</textarea>"
            output_section += f"<a href='uploads/temp_seqAndStructure_pp.txt' download style='padding:8px 16px; background:#2c3e50; color:white; border-radius:4px; text-decoration:none;'>Download Post-Processed</a>"
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"

elif action == "visualise":
    run_visualieze(form)
    try:
        with open("testprot.html") as f:
            content = f.read()
        output_section = content.split("<body>")[1].split("</body>")[0]
    except Exception as e:
        import traceback
        output_section = f"<pre>ERROR: {e}\n{traceback.format_exc()}</pre>"
elif action == "validate":
    try:
        output = run_validate(BASE_DIR, form)
        values = [""]
        for line in output.splitlines():
            values.append(round(float(line.strip()),2))
        output_section = f"""<br><br>
    <h2>Results</h2>
<div style="overflow-x:auto;">
<table style="border-collapse:collapse; font-family:Arial,sans-serif;">
    <thead>
        <tr style="background:#1f5c3a; color:white;">
            <th style="padding:8px 12px; white-space:nowrap;">Nr of Prot</th>
            <th style="padding:8px 12px; white-space:nowrap;">Mean Length</th>
            <th style="padding:8px 12px; white-space:nowrap;">Sum of Length</th>
            <th style="padding:8px 12px; white-space:nowrap;">Sum of pred. pos</th>
            <th style="padding:8px 12px; white-space:nowrap;">Q3 Mean</th>
            <th style="padding:8px 12px; white-space:nowrap;">Q3 Dev</th>
            <th style="padding:8px 12px; white-space:nowrap;">SOV Mean</th>
            <th style="padding:8px 12px; white-space:nowrap;">SOV Dev</th>
            <th style="padding:8px 12px; white-space:nowrap;">Q3_C Mean</th>
            <th style="padding:8px 12px; white-space:nowrap;">Q3_C Dev</th>
            <th style="padding:8px 12px; white-space:nowrap;">Q3_E Mean</th>
            <th style="padding:8px 12px; white-space:nowrap;">Q3_E Dev</th>
            <th style="padding:8px 12px; white-space:nowrap;">Q3_H Mean</th>
            <th style="padding:8px 12px; white-space:nowrap;">Q3_H Dev</th>
            <th style="padding:8px 12px; white-space:nowrap;">SOV_C Mean</th>
            <th style="padding:8px 12px; white-space:nowrap;">SOV_C Dev</th>
            <th style="padding:8px 12px; white-space:nowrap;">SOV_E Mean</th>
            <th style="padding:8px 12px; white-space:nowrap;">SOV_E Dev</th>
            <th style="padding:8px 12px; white-space:nowrap;">SOV_H Mean</th>
            <th style="padding:8px 12px; white-space:nowrap;">SOV_H Dev</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:8px 12px; text-align:center;">{values[1]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[2]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[3]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[4]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[5]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[6]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[7]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[8]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[9]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[10]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[11]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[12]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[13]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[14]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[15]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[16]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[17]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[18]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[19]}</td>
            <td style="padding:8px 12px; text-align:center;">{values[20]}</td>
        </tr>
    </tbody>
</table>
</div>


<a href="uploads/detailedGor.txt" download style="display:inline-block; margin-top:10px; padding:8px 16px; background:#2c3e50; color:white; text-decoration:none; border-radius:4px;">Download</a>"""
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"
elif action == "train":
    try:
        output , model_path = run_train(BASE_DIR, form)
        output_section = f"<textarea readonly rows='10' style='width:100%; resize:both;'>{output}</textarea><a href={model_path} download style='display:inline-block; margin-top:10px; padding:8px 16px; background:#2c3e50; color:white; border-radius:4px;'>Download</a>"
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"
elif action == "kfold":
    try:
        from Kfold_cgi import kfold
        output_section = kfold(BASE_DIR, form)
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"


print(f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>GOR &mdash; propraGruppe15</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <script type = "text/javascript" src = "jsmol/JSmol.min.js"></script>
    <script type = "text/javascript">
    var Info = {{
        width: 700,
        height: 700,
        j2sPath: "jsmol/j2s"
    }}
    </script>
</head>
<body>

<nav>
    <a class="nav-logo" href="#">
        <svg viewBox="0 0 22 22" fill="none" width="20" height="20">
            <ellipse cx="11" cy="11" rx="4"  ry="10" stroke="#2e7d52" stroke-width="1.8" fill="none"/>
            <ellipse cx="11" cy="11" rx="10" ry="4"  stroke="#4caf80" stroke-width="1.8" fill="none"/>
            <circle  cx="11" cy="11" r="2"           fill="#2e7d52"/>
        </svg>
        propraGruppe15
    </a>
    <ul class="nav-links">
        <li><a href="https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution1/Assignment03/aufgabe3_2_0.html">Home</a></li>
        <li><a href="https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution3/Alignment/Alignment_CGI.py">Alignment</a></li>
        <li><a href="#" class="active">GOR</a></li>
        <li style="margin-left: auto;"><a href="https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution1/Assignment03/help/index.html">Help</a></li>
        <li><a href="https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution1/Assignment03/about/index.html">About</a></li>
    </ul>
</nav>

<div class="hero">
    <h1>GOR Prediction</h1>
    <p>Secondary structure prediction &mdash; propraGruppe15 &middot; LMU/TUM &middot; Gruppe 15</p>
</div>

<div class="page-wrapper">

    <p class="section-label">Library &amp; Training</p>

    <div class="card">
        <h2>Sec Library</h2>
        <p>Create a secondary structure library from PDB protein IDs.</p>
        <form method="post" enctype="multipart/form-data">
            <input type="hidden" name="action" value="seclib">
            <label class="field-label">Protein ID</label>
            <input type="text" name="--id" placeholder="z.B. 2MZ9">
            <label class="field-label">oder ID-Liste (File)</label>
            <input type="file" name="--idlist">
            <label class="field-label">
                <input type="checkbox" name="--generate_fasta" value="yes" style="width:auto;"> Generate FASTA
            </label>
            <br>
            <button type="submit">Run</button>
        </form>
        {output_section if action == "seclib" else ""}
    </div>

   

    <p class="section-label">Prediction</p>
    
     <div class="card">
        <h2>Train</h2>
        <p>Train a GOR model on a secondary structure database.</p>
        <form method="post" enctype="multipart/form-data">
            <input type="hidden" name="action" value="train">
            <label class="field-label">GOR Methode</label>
            <select name="--method">
                <option value="1">GOR1</option>
                <option value="3">GOR3</option>
                <option value="4">GOR4</option>
            </select>
            <label class="field-label">Database File</label>
            <input type="file" name="--db">
            <button type="submit">Run</button>
        </form>
        {output_section if action == "train" else ""}
    </div>

    <div class="card">
        <h2>Predict</h2>
        <p>Predict secondary structure from a FASTA or MAF file.</p>
        <form method="post" enctype="multipart/form-data">
            <input type="hidden" name="action" value="predict">
            <label class="field-label">GOR Typ</label>
            <select name="--Gor_type">
                <option value="--GOR1">GOR1</option>
                <option value="--GOR3">GOR3</option>
                <option value="--GOR4">GOR4</option>
            </select>
            <label class="field-label">Custom Model (pls use the same filename as provided by the generator or use the format gorXmodel.txt)</label>
            <input type="file" name="--model_file">
            <label class="field-label">FASTA (File)</label>
            <input type="file" name="--fasta">
            <label class="field-label">MAF (File)</label>
            <input type="file" name="--maf">
            <label class="field-label">Probabilities</label>
            <select name="--probabilities">
                <option value="no">No</option>
                <option value="yes">Yes</option>
            </select>
            <label class="field-label">
                <input type="checkbox" name="--postprocess" value="yes" style="width:auto;"> Post-Processing
            </label>
            <label class="field-label">Post-Processing Window Size</label>
            <input type="number" name="--windowsize" value="7" min="3" max="20" step="2">
            <button type="submit">Run</button>
        </form>
        {output_section if action == "predict" else ""}
    </div>

    <p class="section-label">Validation</p>

    <div class="card">
        <h2>Validate</h2>
        <p>Compare a prediction against a ground truth to compute Q3/SOV scores.</p>
        <form method="post" enctype="multipart/form-data">
            <input type="hidden" name="action" value="validate">
            <label class="field-label">Prediction</label>
            <textarea name="--prediction" rows="4"></textarea>
            <input type="file" name="--prediction_file">
            <label class="field-label">Ground truth</label>
            <textarea name="--reference" rows="4"></textarea>
            <input type="file" name="--reference_file">
            <button type="submit">Run</button>
        </form>
        {output_section if action == "validate" else ""}
    </div>

    <div class="card">
        <h2>K-Fold</h2>
        <p>Cross-validate a GOR model with k-fold evaluation.</p>
        <form method="post" enctype="multipart/form-data">
            <input type="hidden" name="action" value="kfold">
            <label class="field-label">GOR Typ</label>
            <select name="--gorType">
                <option value="gor1">GOR1</option>
                <option value="gor3">GOR3</option>
                <option value="gor4">GOR4</option>
            </select>
            <label class="field-label">Fold Count</label>
            <input type="number" name="--foldcount" value="5" min="2" max="10">
            <label class="field-label">Input Database</label>
            <input type="file" name="--input_seclib">
            <label class="field-label">
    <input type="checkbox" name="--postprocess" value="yes" style="width:auto;"> Post-Processing
        </label>
        <label class="field-label">Post-Processing Window Size</label>
        <input type="number" name="--windowsize" value="7" min="3" max="20" step="2">
        <br>
            <button type="submit">Run</button>
        </form>
        {output_section if action == "kfold" else ""}
    </div>

    <p class="section-label">Visualisation</p>

    <div class="card">
        <h2>3D Protein</h2>
        <p>
    For comparison of GOR-Prediction with ground truth in 3D (JSmol) attach gor output file.
         </p>
        <form method="post" enctype="multipart/form-data">
            <input type="hidden" name="action" value="visualise">
            <div class="param-grid">
                <div>
                    <label class="field-label">PDB-ID</label>
                    <input type="text" name="--vis_pdb" placeholder="z.B. 1a2p" required>
                </div>
                <div>
                    <label class="field-label">GOR-Output</label>
                    <input type="file" name="--vis_gorout" required>
                </div>
            </div>
            <button type="submit">Visualise</button>
        </form>
        {output_section if action == "visualise" else ""}
        
        
    </div>
</div>

<footer>
    <span>propraGruppe15 &mdash; Bioinformatik-Praktikum &middot; LMU/TUM &middot; Gruppe 15</span>
    <span>Laura Martin &middot; Lucas Nassonov &middot; Daniel Bernadi &middot; Toan David Huynh Ngoc</span>
</footer>

</body>
</html>""")