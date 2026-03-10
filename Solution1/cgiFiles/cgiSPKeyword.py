#!/usr/bin/biopython
import os
import mycgi
import subprocess
import shutil

print("Content-type:text/html\n\n")

result = "No Organism Name entered."
form = mycgi.Form()
keywords_input = form.getfirst('keywords', '')
swiss_prot_input = form["swissprot_file"]

keywords = [keyword.strip() for keyword in keywords_input.split(",") if keyword.strip()]

uploaded_file_path = os.path.join("/tmp", swiss_prot_input.filename)
    
with open(uploaded_file_path, 'wb') as fout:
    shutil.copyfileobj(swiss_prot_input.file, fout)

result = subprocess.run(
    ["python3", "../Assignment06/spkeyword.py", "--keyword"] + keywords + ["--swissprot", uploaded_file_path], 
    text=True,
    capture_output=True
    ) 
output = result.stdout
output = output.replace("\n", "<br>")

print(f"""
<html>
    <head><title>SP Keywords</title></head>
        <body>
            <h1>Entries from keywords: </h1>
            {output}
        </body>
</html>
""")
