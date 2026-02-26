#!/usr/bin/biopython
import os
import subprocess
import mycgi



form = mycgi.Form()

ac = form.getfirst("fasta", "").strip()



result = subprocess.run(["python3", "../Assignment05/acsearch.py", "--ac", ac],
                        text=True,
                        capture_output=True,
                        )


print("Content-Type: text/html\n")
print()
print("<pre>")
print("<h1> Ergebnis: </h1>")
print("<pre>")
print(result.stdout)