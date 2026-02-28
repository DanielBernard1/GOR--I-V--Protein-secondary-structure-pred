#!/usr/bin/biopython
import os
import subprocess
import mycgi

print("Content-type: text/html\n")

form = mycgi.Form()


pdb1 = form["pdb1"].value
pdb2 = form["pdb2"].value
#

#
try:
    if pdb2:
        output = subprocess.run(["python3", "../Assignment14/homestrad2.0.py", "--pdb1", pdb1, "--pdb2", pdb2], capture_output=True, text = True)
    else:
        output = subprocess.run(["python3", "../Assignment14/homestrad2.0.py", "--pdb1", pdb1], capture_output=True, text=True)
except Exception as e:
    print(e)
print("""
<!DOCTYPE html>
<html>
  <body>
    <h1>Ausgabe Proteine</h1>
    <p> </p>
    <p> The output of the programm will be shown after you hit the button send </p>
    <form method="post" enctype="multipart/form-data">
      <input type="text" name="pdb1" required>
      <input type="text" name="pdb2">
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

