#!/usr/bin/biopython
import os
import mycgi
import subprocess
import shutil

print("Content-type:text/html\n\n")

result = "No Organism Name entered."
form = mycgi.Form()
keywords_input = form.get('keywords')
swiss_prot_input = form.get('swissprot_file')

keywords = [keyword.strip() for keyword in keywords_input.split(",") if keyword.strip()]

result = subprocess.run(
    ["python3", "../Assignment06/spkeyword.py", "--keyword"] + keywords + ["--swissprot", swiss_prot_input], 
    text=True,
    capture_output=True
    ) 
output = result.stdout
output = output.replace("\n", "<br>")



print(f"""
<html>
    <head><title>Genome Lengths</title></head>
        <body>
            <h1>Entries from keywords: </h1>
            {output}
        </body>
</html>
""")
