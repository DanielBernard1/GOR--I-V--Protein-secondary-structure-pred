import os
import subprocess


def run_visualieze(form):
    pdb_id = form.getvalue("--vis_pdb")

    if not pdb_id:
        return "<pre>ERROR: pdb_id ist None/leer</pre>"

    pdb_id = pdb_id.strip()

    gorout_upload = form.getvalue("--vis_gorout")
    if not gorout_upload:
        return "<pre>ERROR: Kein GOR-Output File hochgeladen</pre>"

    gorout = os.path.join("uploads", "vis_gorout.txt")
    with open(gorout, "wb") as f:
        if isinstance(gorout_upload, str):
            f.write(gorout_upload.encode())
        else:
            f.write(gorout_upload)

    result = subprocess.run([
        "python3", "visualisediff2.py",
        "--pdb", pdb_id,
        "--gorout", gorout,
    ], capture_output=True, text=True)

    if result.returncode != 0:
        return f"<pre>SUBPROCESS ERROR:\n{result.stderr}</pre>"


    with open("uploads/vis_result.html") as f:
        return f.read()