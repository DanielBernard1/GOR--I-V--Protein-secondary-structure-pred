#!/usr/bin/biopython
import os
import subprocess
import mycgi

print("Content-type: text/html\n")

form = mycgi.Form()


fasta = form["fasta"]
features = form["features"]

#Datein speichern
os.makedirs("uploads", exist_ok=True)

orf_path = "uploads/cgi.fasta"
feat_path = "uploads/cgi.features"

with open(orf_path, "wb") as f:
    f.write(fasta.value)

with open(feat_path, "wb") as f:
    f.write(features.value)

#
output = subprocess.run(["python3", "../Assignment10/genome2orf.py", "--organism", orf_path, "--features", feat_path], capture_output=True, text = True)


print("""
<!DOCTYPE html>
<html>
  <body>
    <h1>Ausgabe aller ORFs zusammen mit ihrem Lotus-Tag</h1>
    <p> Pls insert a fasta file and a features file, which should be analysed </p>
    <p> The output of the programm will be shown after you hit the button send </p>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="fasta" required>
      <input type="file" name="features" required>
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

