#!/usr/bin/env python3
import argparse
import MySQLdb

db = MySQLdb
parser = argparse.ArgumentParser(description="Add Swissprot to Database")
parser.add_argument("--input", type=str, required=True, help="Path to swissprot data")

args = parser.parse_args()
file_path = args.input

with open(file_path, "r") as f:
    sequence = ""
    appendToSequence = False
    data = {"ID" : "", "AC" : "", "DE" : "", "OS" : "", "KW" : [], "SQ" : ""}
    for line in f:
        if line.startswith("SQ"):
            appendToSequence = True
        elif not line.startswith("     ") and appendToSequence:
            print(sequence)
            data["SQ"] = sequence
            appendToSequence = False
        elif line.startswith("AC"):
            data["AC"] = line[5:]
        elif appendToSequence:
            sequence += line.strip()
        elif line.startswith("//"):
            if data["SQ"] != "":
                for kw in data["KW"]:
                    print()
                    #add sequence to whole DB // TODO
                    #add sequence and keywoard to keywoard DB TODO
                print(sequence)
            sequence = ""
            appendToSequence = False
            data = {"ID" : "", "AC" : "", "DE" : "", "OS" : "", "KW" : [], "SQ" : ""}