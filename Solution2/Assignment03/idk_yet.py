#!/usr/bin/python3
import mysql.connector
import sys
import argparse as ap
db = mysql.connector.connect(
  host="127.0.0.1",
  port=3307,
  user="bioprakt15",
  password="$1$/NQ9xkkh$BnZDjreVX/1q0MGqWEc3M0",
  database="bioprakt15"
)

parser = ap.ArgumentParser()

parser.add_argument('--id', nargs="+", required=True)
parser.add_argument('--source', required=True)
parser.add_argument('--output', required=False)



args = parser.parse_args()
cursor = db.cursor()
Quellen_name = args.source

in_all_keys = ""
for qid in args.id:
  in_all_keys += f'{qid},'


cursor.execute(f'''
SELECT Q.source_key, S.seq FROM Quelleof Qo JOIN Quelle Q ON Qo.q_id=Q.q_id JOIN Sequenz S ON S.seq_id=Qo.seq_id
WHERE Q.source_name='{Quellen_name}' AND Q.source_key IN ({in_all_keys[:-1]})
''')
Output = cursor.fetchall()
for row in Output:
  print(f">{row[0]}\n{row[1]}")

db.close()