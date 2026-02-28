#!/usr/bin/env python3
import argparse
import mysql.connector

db = mysql.connector.connect(
  host="127.0.0.1",
  port=3307,
  user="bioprakt15",
  password="$1$/NQ9xkkh$BnZDjreVX/1q0MGqWEc3M0",
  database="bioprakt15")

parser = argparse.ArgumentParser(description="Add ORF to Database")
parser.add_argument("--input", type=str, required=True, help="Path to ORF data")

curser = db.cursor(buffered=True)

args = parser.parse_args()
file_path = args.input

with open(file_path, "r") as f:
    header = "" 
    sequence = ""
    first = True
    counter = 0
    for line in f:
        if line.startswith(">"):
            if first:
                header = line[1:].strip()
                sequence = ""
                first = False
                continue

            curser.execute("INSERT IGNORE INTO sequenz VALUES (NULL, %s, 'ORF', %s, '-', 'Datensatz', %s, %s);", (header, len(sequence), sequence, header))
            header = line[1:].strip()
            sequence = ""
            counter += 1
            if counter % 100 == 0:
                db.commit()

        else: 
            sequence += line.strip()
        
    curser.execute("INSERT IGNORE INTO sequenz VALUES (NULL, %s, 'ORF', %s, '-', 'Datensatz', %s, %s);", (header, len(sequence), sequence, header))
    db.commit()
curser.close()
db.close()