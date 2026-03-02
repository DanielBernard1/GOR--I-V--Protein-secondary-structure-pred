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
    return "".join(comp[b] for b in reversed(dna)) #zusammenfassung für for b in reversed(dns) --> "".join(comp[b])


with open("MyFile.txt", "w") as f:# File für die nächsten Aufgaben
    for header, seq_2 in seq.items():
        orf_id = 0 #brauchen wir für Bennenung der header im File da diese sonst evtl nicht eindeutig sind und uns das bei den nächsten Aufgaben Probleme macht
        strand = "" # hier 3 zu 5
        sequence = seq_2.upper()
        length = len(sequence)

        codon_end = length-2 # n-3+1 (+1 weil 0 basiert)
        start0 = None #haben wir ATG in diesem FRAME schonmal gesehen, danach ist ATG egal bis wir zu einem Stop Codon gekommen sind und dann Start wieder auf 0 setzen
        start1 = None
        start2 = None

        # wir gehen position für position (j ist die Position)
        for j in range(codon_end):
            codon = sequence[j:j + 3] # aktuelle Pos(Anfang Codon), +3 (Ende Codon)

            if j % 3 == 0: #Frame ab 0 Position
                if start0 is None:
                    if codon == "ATG":
                        start0 = j
                else:
                    if codon == "TAA" or codon == "TAG" or codon == "TGA":
                        end = j + 3 #muss letztes Codon (Stopcodon) noch hinzufügen
                        print(f"{header}{strand}_0") #kann Strand rauslassen, hier aber für eindeutigkeit noch drinnen, stattdesen vielleicht orf_id mit rein nehmen
                        print(sequence[start0:end])
                        f.write(f"{header}{strand}_0_{orf_id}\n") # eigtl richtig laut Vorgabe = {header}_0_{orf_id}
                        f.write(sequence[start0:end]+ "\n")
                        orf_id += 1
                        start0 = None


            if j % 3 == 1: #FRAME startet an Stelle 1
                if start1 is None:
                    if codon == "ATG":
                        start1 = j
                else:
                    if codon == "TAA" or codon == "TAG" or codon == "TGA":
                        end = j + 3
                        print(f"{header}{strand}_1")# 1ter Frame!
                        print(sequence[start1:end])
                        f.write(f"{header}{strand}_1_{orf_id}\n")
                        f.write(sequence[start1:end] + "\n")
                        orf_id += 1
                        start1 = None


            if j % 3 == 2: #FRAME startet an Stelle 2
                if start2 is None:
                    if codon == "ATG":
                        start2 = j
                else:
                    if codon == "TAA" or codon == "TAG" or codon == "TGA":
                        end = j + 3
                        print(f"{header}{strand}_2")# 2ter Frame!
                        print(sequence[start2:end])
                        f.write(f"{header}{strand}_2_{orf_id}\n")
                        f.write(sequence[start2:end]+ "\n")
                        orf_id += 1
                        start2 = None


        # Gleiche nochmal für 5 zu 3

        strand = "_rev" #reversed Strand _rev damit ich ausgabe von oben koppierten kann und trotzdem "_" dabei habe
        rev = revcomp(seq_2.upper()) # hätte man auch direkt oben in der Methode machen können
        length = len(rev) #ist hier noch weil ich alles erst falsch gemacht habe und dachte man muss nur den längsten ORF aus jeder Sequenz ausgeben
        codon_end = length-2
        start0 = None
        start1 = None
        start2 = None


            # wir gehen position für position (j ist die Position)
        for j in range(codon_end):
            codon = rev[j:j + 3] # rev!

            if j % 3 == 0:
                if start0 is None:
                    if codon == "ATG":
                        start0 = j
                else:
                    if codon == "TAA" or codon == "TAG" or codon == "TGA":
                        end = j + 3
                        print(f"{header}{strand}_0")
                        print(rev[start0:end]) #rev!
                        f.write(f"{header}{strand}_0_{orf_id}\n")
                        f.write(rev[start0:end]+ "\n")
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
                        print(rev[start1:end]) #rev!
                        f.write(f"{header}{strand}_1_{orf_id}\n")
                        f.write(rev[start1:end]+ "\n")
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
                        print(rev[start2:end]) #rev!
                        f.write(f"{header}{strand}_2_{orf_id}\n")
                        f.write(rev[start2:end]+ "\n")
                        orf_id += 1
                        start2 = None

