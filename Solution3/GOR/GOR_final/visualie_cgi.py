#!/usr/bin/biopython
import os
import subprocess


def run_visualieze(form):
    pdb_id = form.getvalue("--vis_pdb")

    # Debug: zeig was ankommt
    if not pdb_id:
        return "<pre>ERROR: pdb_id ist None/leer</pre>"

    pdb_id = pdb_id.strip()
    gorout = os.path.join("uploads", "temp_seqAndStructure.txt")

    # Debug: existiert die gorout datei?
    if not os.path.exists(gorout):
        return f"<pre>ERROR: gorout nicht gefunden: {gorout}</pre>"

    result = subprocess.run([
        "python3", "visualisediff2.py",
        "--pdb", pdb_id,
        "--gorout", gorout,
    ], capture_output=True, text=True)

    if result.returncode != 0:
        return f"<pre>SUBPROCESS ERROR:\n{result.stderr}</pre>"

    return result.stdout


