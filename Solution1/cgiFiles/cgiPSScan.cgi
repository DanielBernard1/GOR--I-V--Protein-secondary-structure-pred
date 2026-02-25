#!/usr/bin/biopython
import subprocess
import mycgi

form = mycgi.Form()

pattern = form.getfirst("pattern", "").strip()
prosite_id = form.getfirst("prosite_id", "").strip()


form_file = form["file"]  

if pattern:
    result = subprocess.run(
        ["python3", "Aufgabe7.py", "--fasta", "-", "--pattern", pattern],
        stdin=form_file.file,
        text=True,
        capture_output=True
    )

if prosite_id:
    result = subprocess.run(
        ["python3", "Aufgabe7.py", "--fasta", "-", "--web", prosite_id],
        stdin=form_file.file,
        text=True,
        capture_output=True
    )

print("Content-Type: text/html\n")
print("<h1>Ergebnis:</h1>")
print("<pre>")
print(result.stdout)
print("</pre>")