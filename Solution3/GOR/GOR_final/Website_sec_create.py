import os
import subprocess

def run_seclib(BASE_DIR, form):
    id = form.get("--id")
    idList = form.get("--idlist")

    seclib_path = os.path.join(BASE_DIR, "sec_lib.txt")
    output = ""

    if id:
        result = subprocess.run(
            ["python3", "sec_create.py", "--id", id],
            capture_output=True, text=True)
        output = result.stdout

    elif idList:
        tmp_path = os.path.join(BASE_DIR, "tmp_idlist.txt")
        try:
            with open(tmp_path, "w") as f:
                f.write(idList)
            result = subprocess.run(
                ["python3", "sec_create.py", "--idList", tmp_path],
                capture_output=True, text=True)
            output = result.stdout
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    else:
        output = "Keine IDs bereitgestellt."

    return output, seclib_path