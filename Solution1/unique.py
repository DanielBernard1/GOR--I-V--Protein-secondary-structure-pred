filepath = ""
ks = []
kmers = {}

with open(filepath, "r") as f:
    count = 0
    seq = ""
    for line in f:
        if line.startswith(">"):
            current = "gene" + count 
            if seq != "":
                for k in ks:
                    for i in range(seq.len()):
                        if (i+k == seq.len()): break
                        kmers[seq[i: i+k]] = set
            seq = ""
        else:
            seq += line
