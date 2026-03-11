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

    html_filename = f"uploads/{pdb_id.upper()}.html"
    html_file = os.path.join("uploads", html_filename)

    result = subprocess.run([
        "python3", "visualisediff2.py",
        "--pdb", pdb_id,
        "--gorout", gorout,
        "--output", html_file
    ], capture_output=True, text=True)


    if result.returncode != 0:
        return f"<pre>SUBPROCESS ERROR:\n{result.stderr}</pre>"

    with open(html_file) as f:
        content = f.read()
    return content
