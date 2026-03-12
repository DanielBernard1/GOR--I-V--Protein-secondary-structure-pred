import os
import subprocess


def run_visualieze(form):
    pdb_id = form.getvalue("--vis_pdb")

    if not pdb_id:
        return "<pre>no pid</pre>"

    pdb_id = pdb_id.strip()

    gorout_upload = form.getvalue("--vis_gorout")
    if not gorout_upload:
        return "<pre>ERROR: no gorout</pre>"

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
        "--output", "."
    ], capture_output=True, text=True)

    if result.returncode != 0:
        return f"<pre>{result.stderr}</pre>"


    outfile = f"{pdb_id}.html"
    try:
        with open(outfile) as f:
            content = f.read()

        body = content.split("<body>")[1].split("</body>")[0]
        return body
    except Exception as e:
        return f"<pre>ERROR in {outfile}: {e}</pre>"