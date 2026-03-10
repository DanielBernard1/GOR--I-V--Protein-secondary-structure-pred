#!/usr/bin/biopython
import subprocess
import mycgi

form = mycgi.Form()

pattern = form.getfirst("pattern", "").strip()
prosite_id = form.getfirst("prosite_id", "").strip()

form_file = form["file"]
file_content = form_file.file.read().decode("utf-8")

if pattern:
    result = subprocess.run(
        ["python3", "../Assignment07/psscan.py", "--fasta", "-", "--pattern", pattern],
        input=file_content,
        text=True,
        capture_output=True
    )
elif prosite_id:
    result = subprocess.run(
        ["python3", "Aufgabe7.py", "--fasta", "-", "--web", prosite_id],
        input=file_content,
        text=True,
        capture_output=True
    )

print("Content-Type: text/html\n")
print("<h1>Ergebnis:</h1>")
print("<pre>")
print(result.stdout)
print("</pre>")