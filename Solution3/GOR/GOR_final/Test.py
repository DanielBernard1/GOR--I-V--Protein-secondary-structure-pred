#!/usr/bin/biopython
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mycgi
print("Content-type: text/html\n")
print("<h1>mycgi ok</h1>")