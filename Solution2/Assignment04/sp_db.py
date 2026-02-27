#!/usr/bin/env python3
import argparse
import mysql.connector

db = mysql.connector.connect(
  host="127.0.0.1",
  port=3307,
  user="bioprakt15",
  password="$1$/NQ9xkkh$BnZDjreVX/1q0MGqWEc3M0",
  database="bioprakt15")

parser = argparse.ArgumentParser(description="Add Swissprot to Database")
parser.add_argument("--input", type=str, required=True, help="Path to swissprot data")

curser = db.cursor(buffered=True)

args = parser.parse_args()
file_path = args.input

with open(file_path, "r") as f:
    sequence = ""
    appendToSequence = False
    data = {"ID" : "", "AC" : "", "DE" : "", "OS" : "", "KW" : [], "SQ" : ""}
    for i, line in enumerate(f):
        if line.startswith("SQ"):
            appendToSequence = True
        elif line.startswith("AC"):
            data["AC"] = line[5:].strip()
        elif line.startswith("ID"):
            data["ID"] = line[5:].strip()
        elif line.startswith("OS"):
            data["OS"] = line[5:].strip()
        elif line.startswith("DE"):
            data["DE"] = line[5:].strip()
        elif line.startswith("KW"):
            kws = line[5:].rstrip(".").split(";")
            data["KW"].extend(kw.strip() for kw in kws)
        elif line.startswith("//"):
            data["SQ"] = sequence
            appendToSequence = False
            if data["SQ"] != "":
                #add sequence to whole DB // TODO
                curser.execute("INSERT IGNORE INTO Sequenz(seq_header, typ, laenge, organism, quelle, seq, source_key) VALUES(%s, %s, %s, %s, %s, %s, %s)", 
                               (data["AC"], "Protein", len(data["SQ"].replace(" ", "")), data["OS"], "Swissprot", data["SQ"], data["AC"]))
                #add to swissprot table
                query = "INSERT IGNORE INTO Swissprot(ac, id, de, os) VALUES (%s, %s, %s, %s)"
                vals = (data["AC"], data['ID'], data["DE"], data["OS"])
                curser.execute(query, vals)
                #add to keywords
                for kw in data["KW"]:
                    curser.execute("INSERT IGNORE INTO keywords(keyword) VALUES (%s)",
                    (kw,)
                    )
                    curser.execute("SELECT keyword_id FROM keywords WHERE keyword = %s",
                    (kw,)
                    )
                    keyword_id = curser.fetchone()[0]
                    curser.execute("SELECT seq_number FROM Sequenz WHERE seq_header = %s AND quelle = %s", 
                    (data["AC"], "Swissprot"))
                    seq_number = curser.fetchone()[0]
                    curser.execute("INSERT IGNORE INTO ac_keywords(seq_number, ac, keyword_id) VALUES (%s, %s, %s)",
                    (seq_number, data["AC"], keyword_id))
                print(data["AC"])
            sequence = ""
            appendToSequence = False
            data = {"ID" : "", "AC" : "", "DE" : "", "OS" : "", "KW" : [], "SQ" : ""}
        elif appendToSequence:
            sequence += line.replace(" ", "").strip()

        if i % 100 == 0:
            db.commit()
    db.commit()