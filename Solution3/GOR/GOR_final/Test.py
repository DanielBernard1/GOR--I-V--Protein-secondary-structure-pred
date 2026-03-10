#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mycgi
from validate_cgi import run_validate

print("Content-type: text/html\n")

form = mycgi.Form()
action = form.get("action")
output_section = ""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
    <form method="post">
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