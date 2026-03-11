#!/usr/bin/biopython
import os
import subprocess


def run_seclib(BASE_DIR, form):
    id = form.getvalue("--id")

    if "--idlist" in form and form["--idlist"].filename:
        idList = form["--idlist"].file.read().decode("utf-8")
    else:
        idList = form.getvalue("--idlist")

    seclib_path = os.path.join(BASE_DIR, "sec_lib.txt")
    output = ""

    if id:
        result = subprocess.run(
            ["python3", "sec_create.py", "--id", id],
            capture_output=True, text=True, cwd=BASE_DIR)
        output = result.stdout + result.stderr

    elif idList:
        tmp_path = os.path.join(BASE_DIR, "tmp_idlist.txt")
        try:
            with open(tmp_path, "w") as f:
                f.write(idList)
            result = subprocess.run(
                ["python3", "sec_create.py", "--idlist", tmp_path],
                capture_output=True, text=True, cwd=BASE_DIR)
            output = result.stdout + result.stderr
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    else:
        output = "Keine IDs bereitgestellt."

    return output, seclib_path