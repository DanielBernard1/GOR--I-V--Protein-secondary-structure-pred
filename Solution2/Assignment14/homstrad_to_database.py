#!/usr/bin/env python3
import argparse
import mysql.connector
import os

db = mysql.connector.connect(
  host="127.0.0.1",
  port=3307,
  user="bioprakt15",
  password="$1$/NQ9xkkh$BnZDjreVX/1q0MGqWEc3M0",
  database="bioprakt15")

parser = argparse.ArgumentParser(description="Add ORF to Database")
parser.add_argument("--input", type=str, required=True, help="Path to Homstrad data")

curser = db.cursor(buffered=True)

args = parser.parse_args()
root_directory = args.input


#input sequence and pdb header into sequenz from .tem files
def tem_files(file_path):
    with open(file_path, "r") as f:
        header = ""
        sequence = ""
        newSequence = False
        secondary_sequence = False
        for line in f:
            if line.startswith(">"):
                if sequence:
                    if secondary_sequence:
                        curser.execute("UPDATE alignment_sequences SET secondary_structure = %s WHERE pdb_id = %s",
                                (sequence[:len(sequence) - 1], header[:len(header) - 1].strip(";")))
                        secondary_sequence = False
                    else:
                        curser.execute("INSERT IGNORE INTO sequenz VALUES(NULL, %s, 'Protein', %s, '-', 'Homstrad', %s, %s)", 
                                    (header.strip(";"), len(sequence), sequence, header.strip(";")))
                        newSequence = False
                    db.commit()
                header = line[3:].strip()
                sequence = ""
                newSequence = False
                secondary_sequence = False
            elif line.startswith("sequence"):
                newSequence = True
                secondary_sequence = False
            elif line.startswith("secondary structure"):
                secondary_sequence = True
                newSequence = False
            elif newSequence or secondary_sequence:
                sequence += line

        if sequence:
            if secondary_sequence:
                curser.execute("UPDATE alignment_sequences SET secondary_structure = %s WHERE pdb_id = %s",
                                (sequence, header))
                secondary_sequence = False
            else:
                curser.execute("INSERT IGNORE INTO sequenz VALUES(NULL, %s, 'Protein', %s, '-', 'Homstrad', %s, %s)", 
                    (header, len(sequence), sequence, header))

def ali_files(ali_id, file_path):
    with open(file_path, "r") as f:
        family = ""
        # ali_class = ""
        sequence = ""
        addSequence = False
        for line in f:
            if line.startswith("C; family:"):
                family = line[10:].strip()
            # elif line.startswith("C; class:"):
            #     ali_class = line[8:].strip()
            #     continue
            if line.startswith("structureX"):
                addSequence = True
                attributes = [x.strip() for x in line.split(":")]
                #add to alignment sequences
                curser.execute("INSERT IGNORE INTO alignment_sequences VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (ali_id, attributes[1], attributes[6], attributes[7], attributes[2], attributes[4], attributes[3], "-", "-", family))
                db.commit()
            elif addSequence:
                if line.endswith("*\n"):
                    sequence += line.rstrip("*\n")
                    curser.execute("UPDATE alignment_sequences SET aligned_sequence = %s WHERE pdb_id = %s",
                                (sequence, attributes[1]))
                    db.commit()
                    addSequence = False
                else:
                    sequence += line.strip()       


ali_counter = 0
for subdir, _, files in os.walk(root_directory):
    for file in files:
        if file.endswith(".last.backup"):
            continue
        file_path = os.path.join(subdir, file)
        if file.endswith(".tem"):
            print(f"TEM file: {file_path}")
            tem_files(file_path)
        elif file.endswith(".ali"):
            print(f"ALI file: {file_path}")
            ali_files(ali_counter, file_path)
            ali_counter += 1