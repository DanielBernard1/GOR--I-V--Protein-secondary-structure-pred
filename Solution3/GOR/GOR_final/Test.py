#!/usr/bin/biopython
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mycgi
print("Content-type: text/html\n")
form = mycgi.Form()
action = form.get("action")
output_section = ""
print(f"""<!DOCTYPE html>
<html><body>
<h1>GOR</h1>
<p>action: {action}</p>
</body></html>""")