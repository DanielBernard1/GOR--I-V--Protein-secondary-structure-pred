#!/usr/bin/biopython
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Content-type: text/html\n")

import mycgi

form = mycgi.Form()
action = form.getvalue("action")

print(f"<pre>action={action}</pre>")