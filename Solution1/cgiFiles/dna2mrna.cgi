#!/usr/bin/biopython
import os
import subprocess
import mycgi

print("Content-type: text/html\n")

form = mycgi.Form()


fasta = form["fasta"]

os.makedirs("uploads", exist_ok=True)

dna_path = "uploads/cgi.fasta"

with open(dna_path, "w") as f:
    f.write(fasta.value)


output = subprocess.run(["python3", "dna2mrna.py", "--fasta", dna_path], capture_output=True, text = True)


print("""
<!DOCTYPE html>
<html>
  <body>
    <h1>Transformation DNA to mRNA</h1>
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

