import os
import subprocess
import sys


def run_visualieze(form):
        pdb_id = form.getvalue("--vis_pdb").strip()

        gorout_upload = form.getvalue("--vis_gorout")
        if gorout_upload:
            gorout = os.path.join( "uploads", "vis_gorout.txt")
            with open(gorout, "wb") as f:
                f.write(gorout_upload)
        #else:
         #   gorout = os.path.join( "uploads", "temp_seqAndStructure.txt")
        html_file = f"uploads/{pdb_id.upper()}.html"

        subprocess.run([
            "python", "visualisediff2.py",
            "--pdb", pdb_id,
            "--gorout", gorout,
            "--output", html_file
        ], check=True)

        with open(html_file) as f:
            content = f.read()
        return content