#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Content-type: text/html\n")

import mycgi
from validate_cgi import run_validate

form = mycgi.Form()
action = form.get("action")
print(f"<h1>action: {action}</h1>")