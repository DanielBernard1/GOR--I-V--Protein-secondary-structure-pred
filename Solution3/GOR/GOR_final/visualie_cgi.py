import os
import subprocess


def run_visualieze(form):
    pdb_id = form.getvalue("--vis_pdb").strip()


    gorout = os.path.join("uploads", "temp_seqAndStructure.txt")

    gorout_upload = form.getvalue("--vis_gorout")
    if gorout_upload:
        gorout = os.path.join("uploads", "vis_gorout.txt")
        with open(gorout, "wb") as f:
            if isinstance(gorout_upload, str):
                f.write(gorout_upload.encode())
            else:
                f.write(gorout_upload)


    html_file = os.path.join("uploads", f"{pdb_id.upper()}.html")

    result = subprocess.run([
        "python3", "visualisediff2.py",
        "--pdb", pdb_id,
        "--gorout", gorout,
        "--output", html_file
    ], text=True)


    if result.returncode != 0:
        return f"<pre>SUBPROCESS ERROR:\n{result.stderr}</pre>"

    return result.stdout