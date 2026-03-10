#!/usr/bin/biopython
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Content-type: text/html\n")

try:
    import mycgi
    print("<p>mycgi ok</p>")
except Exception as e:
    print(f"<p>mycgi ERROR: {e}</p>")

try:
    from validate_cgi import run_validate
    print("<p>validate_cgi ok</p>")
except Exception as e:
    print(f"<p>validate_cgi ERROR: {e}</p>")