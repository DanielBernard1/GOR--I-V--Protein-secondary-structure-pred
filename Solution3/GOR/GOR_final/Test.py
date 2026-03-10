#!/usr/bin/biopython
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Content-type: text/html\n")

import mycgi
from Website_sec_create import run_seclib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
form = mycgi.Form()
action = form.getvalue("action")
output_section = ""

if action == "seclib":
    try:
        output, seclib_path = run_seclib(BASE_DIR, form)
        output_section = f"<pre>{output}</pre><a href='sec_lib.txt' download style='display:inline-block; margin-top:10px; padding:8px 16px; background:#2c3e50; color:white; text-decoration:none; border-radius:4px;'>Download</a>"
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
        <label>MAF (File)</label>
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