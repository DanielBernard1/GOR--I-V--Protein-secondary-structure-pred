#!/usr/bin/env python3
import argparse
from random import *

#Input: Länge, gc Gehalt (in Prozent), optional: Sequenzname
#Output:
    # Sequenzname
    # erzeugt eine Sequenz mit bestimmten gc gehalt und länge

parser = argparse.ArgumentParser(description="Generates a random sequence with a given gc content")
parser.add_argument("--length", type=int, required=True, help="Length of the sequence")
parser.add_argument("--gc", type=float, required=True, help="GC content of the sequence")
parser.add_argument("--name", type=str, default=None, help="Name of the sequence")

args = parser.parse_args()

length = args.length
gc = args.gc
name = args.name

random_sequence = ""

for i in range(length):
    if int(random_sequence.count("G")) + int(random_sequence.count("C")) < gc:
        random_sequence += choice(["G", "C"])
    else:
        random_sequence += choice(["A", "T"])

random_sequence = "".join(random_sequence)

print(f">{name}")
print(random_sequence)
