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
        output, seclib_path = run_seclib(BASE_DIR, form)
        output_section = f"<textarea readonly rows='10' style='width:100%; resize:both;'>{output}</textarea><a href={seclib_path} download style='display:inline-block; margin-top:10px; padding:8px 16px; background:#2c3e50; color:white; border-radius:4px;'>Download</a>"
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"
elif action == "predict":
    try:
        output, pp_path = run_predict(BASE_DIR, form)
        output_section += f"<br><br><h3>Prediction Output</h3>"
        output_section = f"<textarea readonly rows='10' style='width:100%; resize:both;'>{output}</textarea>"
        output_section += f"<a href='uploads/temp_seqAndStructure.txt' download style='padding:8px 16px; background:#2c3e50; color:white; border-radius:4px; text-decoration:none; margin-top:10px; display:inline-block;'>Prediction</a>"
        if pp_path:

            with open(pp_path) as f:
                pp_content = f.read()
            output_section += f"<br><br><h3>Post-Processed Output</h3>"
            output_section += f"<textarea readonly rows='10' style='width:100%; resize:both;'>{pp_content}</textarea>"
            output_section += f"<a href='uploads/temp_seqAndStructure_pp.txt' download style='padding:8px 16px; background:#2c3e50; color:white; border-radius:4px; text-decoration:none;'>Post-Processed</a>"
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"

elif action == "visualise":
    try:
        output_section = run_visualieze(form)
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"


elif action == "validate":
    try:
        output = run_validate(BASE_DIR, form)
        values = [""]
        for line in output.splitlines():
            values.append(line.strip())
        output_section = f"""<br><br>
    <h2>Results</h2>
<div style="overflow-x: auto;">
    <table style="border-collapse: collapse; white-space: nowrap; width: 100%;">
        <thead>
            <tr style="background: #2c3e50; color: white;">
                <th style="padding: 8px 12px;">Fold</th>
                <th style="padding: 8px 12px;">Nr of Prot</th>
                <th style="padding: 8px 12px;">Mean Length</th>
                <th style="padding: 8px 12px;">Sum of Length</th>
                <th style="padding: 8px 12px;">Sum of pred. pos</th>
                <th style="padding: 8px 12px;">Q3 Mean</th>
                <th style="padding: 8px 12px;">Q3 Dev</th>
                <th style="padding: 8px 12px;">SOV Mean</th>
                <th style="padding: 8px 12px;">SOV Dev</th>
                <th style="padding: 8px 12px;">Q3_H Mean</th>
                <th style="padding: 8px 12px;">Q3_H Dev</th>
                <th style="padding: 8px 12px;">Q3_E Mean</th>
                <th style="padding: 8px 12px;">Q3_E Dev</th>
                <th style="padding: 8px 12px;">Q3_C Mean</th>
                <th style="padding: 8px 12px;">Q3_C Dev</th>
                <th style="padding: 8px 12px;">SOV_H Mean</th>
                <th style="padding: 8px 12px;">SOV_H Dev</th>
                <th style="padding: 8px 12px;">SOV_E Mean</th>
                <th style="padding: 8px 12px;">SOV_E Dev</th>
                <th style="padding: 8px 12px;">SOV_C Mean</th>
                <th style="padding: 8px 12px;">SOV_C Dev</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="padding: 8px 12px;">validation</td>
                <td style="padding: 8px 12px;">{values[0]}</td>
                <td style="padding: 8px 12px;">{values[1]}</td>
                <td style="padding: 8px 12px;">{values[2]}</td>
                <td style="padding: 8px 12px;">{values[3]}</td>
                <td style="padding: 8px 12px;">{values[4]}</td>
                <td style="padding: 8px 12px;">{values[5]}</td>
                <td style="padding: 8px 12px;">{values[6]}</td>
                <td style="padding: 8px 12px;">{values[7]}</td>
                <td style="padding: 8px 12px;">{values[8]}</td>
                <td style="padding: 8px 12px;">{values[9]}</td>
                <td style="padding: 8px 12px;">{values[10]}</td>
                <td style="padding: 8px 12px;">{values[11]}</td>
                <td style="padding: 8px 12px;">{values[12]}</td>
                <td style="padding: 8px 12px;">{values[13]}</td>
                <td style="padding: 8px 12px;">{values[14]}</td>
                <td style="padding: 8px 12px;">{values[15]}</td>
                <td style="padding: 8px 12px;">{values[16]}</td>
                <td style="padding: 8px 12px;">{values[17]}</td>
                <td style="padding: 8px 12px;">{values[18]}</td>
                <td style="padding: 8px 12px;">{values[19]}</td>
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
<html>
<head>
    <title>GOR</title>
    <style>
        body {{ font-family: monospace; max-width: 1700px; margin: auto; padding: 2rem; }}
        section {{ border: 1px solid #ccc; padding: 1rem; margin-bottom: 1.5rem; }}
        input, select, textarea {{ width: 100%; margin-bottom: 1rem; padding: 0.5rem; box-sizing: border-box;}}
        button {{ background: #2c3e50; color: white; padding: 0.5rem 1rem; border: none; cursor: pointer; }}
        button:hover {{ background: #c0392b; }}
    </style>
</head>
<body>
<h1>GOR Prediction</h1>

<section>
    <h2>Sec Library</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="hidden" name="action" value="seclib">
        <label>Protein ID</label>
        <input type="text" name="--id" placeholder="z.B. 2MZ9">
        <label>oder ID-Liste (File)</label>
        <input type="file" name="--idlist">
        <button type="submit" >Run</button>
    </form>
    {output_section if action == "seclib" else ""}
</section>

<section>

    <h2>Train</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="hidden" name="action" value="train">
        <label>GOR Methode</label>
        <select name="--method">
            <option value="1">GOR1</option>
            <option value="3">GOR3</option>
            <option value="4">GOR4</option>
        </select>
        <label>Database File</label>
        <input type="file" name="--db">
        <button type="submit" >Run</button>
    </form>
    <br><br>
    {output_section if action == "train" else ""}

    <h2>Predict</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="hidden" name="action" value="predict">
        <label>GOR Typ</label>
        <select name="--Gor_type">
            <option value="--GOR1">GOR1</option>
            <option value="--GOR3">GOR3</option>
            <option value="--GOR4">GOR4</option>
        </select>
        <label>Custom Model (pls use the same filename as provided by the generator or use the format gorXmodel.txt)</label>
        <input type="file" name="--model_file">
        <label>FASTA (File)</label>
        <input type="file" name="--fasta">
        <label>MAF (File)</label>
        <input type="file" name="--maf">
        <label>Probabilities</label>
        <select name="--probabilities">
            <option value="no">No</option>
            <option value="yes">Yes</option>
        </select>
        <br><br>
    
        <label>
            <label><input type="checkbox" name="--postprocess" value="yes" style="width:auto;"> Post-Processing</label>
        </label>
        <br><br>
        <label>Post-Processing Window Size</label>
<input type="number" name="--windowsize" value="7" min="3" max="20" step="2">
<br><br>
    
        <button type="submit" >Run</button>
    </form>
    {output_section if action == "predict" else ""}
</section>

<section>
    <h2>Validate</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="hidden" name="action" value="validate">
        <label>Prediction</label>
        <textarea name="--prediction" rows="4"></textarea>
        <input type="file" name="--prediction_file">
        <label>Reference</label>
        <textarea name="--reference" rows="4"></textarea>
        <input type="file" name="--reference_file">
        <button type="submit" >Run</button>
    </form>
    {output_section if action == "validate" else ""}
</section>

<section>
    <h2>K-Fold</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="hidden" name="action" value="kfold">
        <label>GOR Typ</label>
        <select name="--gorType">
            <option value="gor1">GOR1</option>
            <option value="gor3">GOR3</option>
            <option value="gor4">GOR4</option>
        </select>
        <label>Fold Count</label>
        <input type="number" name="--foldcount" value="5" min="2" max="10">
        <label>Input Database</label>
            <input type="file" name="--input_seclib">
        <button type="submit">Run</button>
    </form>
    {output_section if action == "kfold" else ""}
</section>
<section>
<h2>3D Protein</h2>
       <p class="section-label">3D Visualisation</p>

    <div class="card">
        <h2></h2>
        <p>3D model of protein</p>
        <p>For comparison of GOR-Prediction with observed in 3D (JSmol) attach gor output file</p>
        <script type="text/javascript" src="jsmol/JSmol.min.js"></script>
        <form method="post" enctype="multipart/form-data">
            <input type="hidden" name="action" value="visualise">
            <div class="param-grid">
                <div>
                    <label class="field-label">PDB-ID</label>
                    <input type="text" name="--vis_pdb" placeholder="z.B. 1a2p" required>
                </div>
                <div>
                    <label class="field-label">GOR-Output</label>
                    <input type="file" name="--vis_gorout">
                </div>
            </div>
            <button type="submit">Visualise</button>
        </form>
        {output_section if action == "visualise" else ""}
    </div>
</section>
</body>
</html>""")