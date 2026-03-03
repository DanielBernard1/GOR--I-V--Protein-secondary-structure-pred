import mysql.connector
db = mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="bioprakt15",
        password="$1$/NQ9xkkh$BnZDjreVX/1q0MGqWEc3M0",
        database="bioprakt15"
    )
cursor = db.cursor()



cursor.execute(f'''
SELECT pdb_id
FROM alignments
''')
Output = cursor.fetchall()

with open("all_pdbids_from_db.txt", 'w') as f:
    for row in Output:
        f.write(f"{row[0]}\n")


cursor.close()
db.close()