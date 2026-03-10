#!/usr/bin/biopython
import sys
import os


print("Content-type: text/html\n")

from GOR_cgi import run_predict
from validate_cgi import run_validate
import subprocess
import mycgi
from Website_sec_create import run_seclib

form = mycgi.Form()
action = form.get("action")
output = ""
output_section = ""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DETAILED_PATH = os.path.join(BASE_DIR, "uploads/detailedGor.txt")
GOR_OUTPUT = os.path.join(BASE_DIR, "uploads/temp_seqAndStructure.txt")

def run_kfold():
    gorType = form.get("--gorType")
    inputdb = form.get("--inputdb")
    tmp = os.path.join(BASE_DIR, "uploads/tmp_kfold.txt")
    with open(tmp, "w") as f: f.write(inputdb)
    result = subprocess.run(["python3", "Kfold.py", "--inputdb", tmp, "--gorType", gorType], capture_output=True, text=True)
    os.remove(tmp)
    return result.stdout

if action == "seclib":
    try:
        output, seclib_path = run_seclib(BASE_DIR, form)
        output_section = f"<br><br><h2>Output</h2><textarea readonly rows='10' style='resize:both;'>{output}</textarea><a href='/{seclib_path}' download style='display:inline-block; margin-top:10px; padding:8px 16px; background:#2c3e50; color:white; text-decoration:none; border-radius:4px;'>Download</a>"
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"

elif action == "predict":
    try:
        output = run_predict(BASE_DIR, form)
        if output:
            output_section = (f"""<br><br><h2>Output</h2><textarea readonly rows='10' style='resize:both;'>{output}</textarea>"
                              <a href='/{GOR_OUTPUT}' download style='display:inline-block; margin-top:10px; padding:8px 16px; background:#2c3e50; color:white; text-decoration:none; border-radius:4px;'>Download</a>""")
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"

elif action == "kfold":
    try:
        output = run_kfold()
        output_section = f"<pre>{output}</pre>"
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"

elif action == "validate":
    try:
        output = run_validate(BASE_DIR, form)
        values = [""] + [line.strip() for line in output.splitlines()]
        output_section = f"""<br><br>
    <h2>Results</h2>
<div style="overflow-x: auto;">
    <table style="border-collapse: collapse; white-space: nowrap; width: 100%;">
        <thead>
            <tr style="background: #2c3e50; color: white;">
                <th style="padding: 8px 12px;">Fold</th>
                <th style="padding: 8px 12px;">Proteins</th>
                <th style="padding: 8px 12px;">Mean Length</th>
                <th style="padding: 8px 12px;">Sum Length</th>
                <th style="padding: 8px 12px;">Sum Predicted</th>
                <th style="padding: 8px 12px;">Q3 Mean</th>
                <th style="padding: 8px 12px;">Q3 Dev</th>
                <th style="padding: 8px 12px;">SOV Mean</th>
                <th style="padding: 8px 12px;">SOV Dev</th>
                <th style="padding: 8px 12px;">qObs H</th>
                <th style="padding: 8px 12px;">qObs E</th>
                <th style="padding: 8px 12px;">qObs C</th>
                <th style="padding: 8px 12px;">SOV H</th>
                <th style="padding: 8px 12px;">SOV E</th>
                <th style="padding: 8px 12px;">SOV C</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="padding: 8px 12px;">validation</td>
                {''.join(f'<td style="padding: 8px 12px;">{values[i] if i < len(values) else ""}</td>' for i in range(1, 14))}
            </tr>
        </tbody>
    </table>
</div>
<a href="/{DETAILED_PATH}" download style="display:inline-block; margin-top:10px; padding:8px 16px; background:#2c3e50; color:white; text-decoration:none; border-radius:4px;">Download</a>"""
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"

print(f"""<!DOCTYPE html>
<html>
<head>
    <title>GOR</title>
    <style>
        body {{ font-family: monospace; max-width: 1000px; margin: auto; padding: 2rem; }}
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
        <button type="submit">Run</button>
    </form>
    {output_section if action == "seclib" else ""}
</section>

<section>
    <h2>Predict</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="hidden" name="action" value="predict">
        <label>GOR Typ</label>
        <select name="--Gor_type">
            <option value="--GOR1">GOR1</option>
            <option value="--GOR3">GOR3</option>
            <option value="--GOR4">GOR4</option>
        </select>
        <label>FASTA (File)</label>
        <input type="file" name="--fasta">
        <label>MAF (File) (if this is selected Gor5 will be used)</label>
        <input type="file" name="--maf">
        <label>Probabilities</label>
        <select name="--probabilities">
            <option value="no">No</option>
            <option value="yes">Yes</option>
        </select>
        <button type="submit">Run</button>
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
        <button type="submit">Run</button>
    </form>
    {output_section if action == "validate" else ""}
</section>

<section>
    <h2>K-Fold</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="hidden" name="action" value="kfold">
        <label>GOR Typ</label>
        <select name="--gorType">
            <option value="--GOR1">GOR1</option>
            <option value="--GOR3">GOR3</option>
            <option value="--GOR4">GOR4</option>
        </select>
        <label>Input Database</label>
        <textarea name="--inputdb" rows="4"></textarea>
        <button type="submit">Run</button>
    </form>
    {output_section if action == "kfold" else ""}
</section>

</body>
</html>""")