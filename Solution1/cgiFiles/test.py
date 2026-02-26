import subprocess

organisms_input = "Paraburkholderia graminis"
organisms = [organism.strip() for organism in organisms_input.split(",") if organism.strip()]

result = subprocess.run(
    ["python3", "../Assignment08/genome_length.py", "--organism"] + organisms, 
    text=True,
    capture_output=True
    ) 
output = result.stdout
print(output)