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


curser = db.cursor(buffered=True)

curser.execute("SELECT pdb_id, sequence FROM Homstrad")
rows = curser.fetchall()

for pdb_id, sequence in rows:
    new_sequence = sequence.replace("-", "")

    update_cursor = db.cursor()
    update_cursor.execute(
        "UPDATE Homstrad SET sequence=%s WHERE pdb_id=%s",
        (new_sequence, pdb_id)
    )

db.commit()

curser.close()
db.close()