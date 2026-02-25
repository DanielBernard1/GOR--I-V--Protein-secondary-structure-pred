#!/usr/bin/biopython
import os
import mycgi
import subprocess
import shutil

print("Content-type:text/html\n\n")

result = "No Organism Name entered."
form = mycgi.Form()
organisms_input = form.get('organisms')

organisms = [organism.strip() for organism in organisms_input.split(",") if organism.strip()]

cgi_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(cgi_dir, "GenomeLengths.txt")
script_path = os.path.join(os.path.dirname(cgi_dir), "Assignment08", "genome_length.py")

result = subprocess.run(
    ["python3", "../Assignment08/genome_length.py", "--organism"] + organisms, 
    text=True,
    capture_output=True
    ) 
output = result.stdout
output = output.replace("\n", "<br>")



print(f"""
<html>
    <head><title>Genome Lengths</title></head>
        <body>
            <h1>Genome Lengths for: </h1>
            {output}
        </body>
</html>
""")

#Download as FASTA:
#<a href="../Assignment08/GenomeLengths.txt" download>Download File</a>