#!/usr/bin/biopython
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Content-type: text/html\n")

import mycgi
from validate_cgi import run_validate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
form = mycgi.Form()
action = form.get("action")

output_section = ""

if action == "validate":
    try:
        output = run_validate(BASE_DIR, form)
        output_section = f"<pre>{output}</pre>"
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"

print(f"""<!DOCTYPE html>
<html><body>
<h1>GOR</h1>
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
</body></html>""")