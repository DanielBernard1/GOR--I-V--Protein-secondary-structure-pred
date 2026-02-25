#!/usr/bin/python
import os
import mycgi
import subprocess
import shutil

print("Content-type:text/html\n\n")

result = "No Organism Name entered."
form = mycgi.Form()
organisms_input = form.get('organisms')

if not organisms_input:
    print("<h3>No organisms provided.</h3>")
    mycgi.print_footer()
    exit()

organisms = [organism.strip() for organism in organisms_input.split(",") if organism.strip()]

result = subprocess.run(
    ["python3", "genome_length.py", "--organism"] + organisms, 
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
            Download as FASTA:
            <a> href="GenomeLengths.txt" download="GenomeLengths.txt">Download File</a>
            {output}
        </body>
</html>
""")
