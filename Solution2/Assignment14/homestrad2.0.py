import argparse
import mariadb
import mysql.connector

db = mysql.connector.connect(
  host="mysql2-ext.bio.ifi.lmu.de",
  port=3306,
  user="bioprakt15",
  password="$1$/NQ9xkkh$BnZDjreVX/1q0MGqWEc3M0",
  database="bioprakt15"
)

parser = argparse.ArgumentParser(description="übergebene pdb_id mit alignments abgleichen")
parser.add_argument("--pdb1", type=str, required=True, help="Pdb-ID 1")
parser.add_argument("--pdb2", type=str, required=False, help="Pdb-Id 2 - optional")

args = parser.parse_args()

pdb1 = args.pdb1
pdb2 = args.pdb2

cursor = db.cursor()
if pdb1 and pdb2 is None:
    cursor.execute(f'''
    SELECT * FROM alignment_sequences 
    WHERE alignment_id IN (
        SELECT alignment_id 
        FROM alignment_sequences 
        WHERE pdb_id = '{pdb1}'
    )
    ORDER BY alignment_id, pdb_id;
    ''')
    for row in cursor.fetchall():
        print(row)

else:
    cursor.execute(f'''
    SELECT * FROM alignment_sequences
    WHERE alignment_id IN (
    SELECT alignment_id
    FROM alignment_sequences
    WHERE pdb_id IN ('{pdb1}','{pdb2}')
    GROUP BY alignment_id
    HAVING COUNT(DISTINCT pdb_id) = 2
    );
    ''')
    results = cursor.fetchall()
    if results:
        print("Pairwise alignments found")
        for row in results:
            print(row)


    else:
        print("No pairwise alignments found, search single:")
        ids = [pdb1, pdb2]
        for id in ids:
            cursor.execute(f'''
            SELECT * FROM alignment_sequences 
            WHERE alignment_id IN (
            SELECT alignment_id 
            FROM alignment_sequences 
            WHERE pdb_id = '{id}'
            )
            ORDER BY alignment_id, pdb_id;
            ''')
            results2 = cursor.fetchall()
            for row in results2:
                print(row)


