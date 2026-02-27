#!/usr/bin/env python3
import argparse


class FASTAreader:
    def read_fasta_function(self, filepath):
        self.motifs = {}
        self.indexes = []

        current_key = None
        for line in filepath:
            s = line.strip()
            if not s:
                continue

            if s.startswith(">"):
                current_key = s
                self.motifs[current_key] = []
                self.indexes.append(s)
            elif current_key is not None:
                self.motifs[current_key].append(s)


        for k in self.motifs:
            self.motifs[k] = "".join(self.motifs[k])

        return self.motifs

#argument parsing
parser = argparse.ArgumentParser(description="Convert CRISPR sequences")
parser.add_argument("--fasta", type=str, required=True, help="Path to FASTA file")

args = parser.parse_args()
file_path = args.fasta

reader = FASTAreader()

with open(file_path, "r") as f:
    seq = reader.read_fasta_function(f)


#Beginn bei ATG
#Ende bei Stopcodon
#dabei wird nur das jeweils längste betrachtet
#3-5-Strang??

#Methode für reverse
def revcomp(dna: str) -> str: #: legt Variabel fest, -> Output der Methode
    comp = {"A": "T", "T": "A", "C": "G", "G": "C"}
    return "".join(comp[b] for b in reversed(dna))


for header, seq_2 in seq.items():
    orf_id = 0
    for strand, sequence in seq.items():
        length = len(sequence)

        codon_end = length-2 # n-3+1
        start0 = None
        start1 = None
        start2 = None

        # wir gehen position für position (j ist die Position)
        for j in range(codon_end):
            codon = sequence[j:j + 3]

            if j % 3 == 0:
                if start0 is None:
                    if codon == "ATG":
                        start0 = j
                else:
                    if codon == "TAA" or codon == "TAG" or codon == "TGA":
                        end = j + 3
                        print(f"{header}{strand}_0")
                        print(sequence[start0:end])
                        orf_id += 1
                        start0 = None


            if j % 3 == 1:
                if start1 is None:
                    if codon == "ATG":
                        start1 = j
                else:
                    if codon == "TAA" or codon == "TAG" or codon == "TGA":
                        end = j + 3
                        print(f"{header}{strand}_1")
                        print(sequence[start1:end])
                        orf_id += 1
                        start1 = None


            if j % 3 == 2:
                if start2 is None:
                    if codon == "ATG":
                        start2 = j
                else:
                    if codon == "TAA" or codon == "TAG" or codon == "TGA":
                        end = j + 3
                        print(f"{header}{strand}_2")
                        print(sequence[start2:end])
                        orf_id += 1
                        start2 = None


#Gleiche nochmal für 5 zu 3
        for strand, sequence in seq.items():
            rc = revcomp(sequence)
            length = len(sequence)

            codon_end = length - 2  # n-3+1
            start0 = None
            start1 = None
            start2 = None

            # wir gehen position für position (j ist die Position)
            for j in range(codon_end):
                codon = sequence[j:j + 3]

                if j % 3 == 0:
                    if start0 is None:
                        if codon == "ATG":
                            start0 = j
                    else:
                        if codon == "TAA" or codon == "TAG" or codon == "TGA":
                            end = j + 3
                            print(f"{header}{strand}_0")
                            print(sequence[start0:end])
                            orf_id += 1
                            start0 = None


                if j % 3 == 1:
                    if start1 is None:
                        if codon == "ATG":
                            start1 = j
                    else:
                        if codon == "TAA" or codon == "TAG" or codon == "TGA":
                            end = j + 3
                            print(f"{header}{strand}_1")
                            print(sequence[start1:end])
                            orf_id += 1
                            start1 = None

                if j % 3 == 2:
                    if start2 is None:
                        if codon == "ATG":
                            start2 = j
                    else:
                        if codon == "TAA" or codon == "TAG" or codon == "TGA":
                            end = j + 3
                            print(f"{header}{strand}_2")
                            print(sequence[start2:end])
                            orf_id += 1
                            start2 = None

