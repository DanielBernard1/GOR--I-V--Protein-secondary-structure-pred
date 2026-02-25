#!/usr/bin/env python3

import os
import subprocess
import mycgi

print("Content-type: text/html\n")

form = mycgi.Form()


fasta = form["fasta"]

os.makedirs("uploads", exist_ok=True)

mRNA_path = "uploads/cgi.fasta"

with open(mRNA_path, "w") as f:
    f.write(fasta.value)


output = subprocess.run(["python3", "mrna2aa.py", "--fasta", mRNA_path], capture_output=True, text = True)


print("""
<!DOCTYPE html>
<html>
  <body>
    <h1>Transformation mRNA to Protein </h1>
    <p> Pls insert a fasta file which should be analysed </p>
    <p> The output of the programm will be shown after you hit the button send </p>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="fasta" required>
      <input type="submit" value="send">
    </form>
    <h2> Output </h2>
    <pre>
    """)
print(output.stdout)

print("""
     </pre>
  </body>
</html>
""")

