import argparse

import mysql.connector

db = mysql.connector.connect(
  host="127.0.0.1",
  port=3307,
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

#pdb-ids im selben Alignment??
#START: PAARWEISE ALIGNEMNT
if pdb2:
  # haben wir ein gemeinsames Alignment, brauchen nur eins um das zu zeigen
  cursor.execute(f"""
    SELECT DISTINCT a1.alignment_id FROM alignment_sequences a1
    JOIN alignment_sequences a2 ON a1.alignment_id = a2.alignment_id
    WHERE a1.pdb_id = '{pdb1}' AND a2.pdb_id = '{pdb2}'
  """)

  output_common = cursor.fetchone() #brauchen nur einen
#Prüfung
  #wenn wie ein ALignment haben wollen wie alle Zeilen des Alignments ausgeben
  if output_common is not None:
    align = output_common[0]
    print(f"{align}\n")

#Sekundärstruktur
    # wenn wir beide im selben Alignment haben müssen wir ihre sekundärstruktur aus dem ALignment holen
    cursor.execute(f"""
      SELECT secondary_structure FROM alignment_sequences
      WHERE alignment_id = {align}
      AND secondary_structure IS NOT NULL
      LIMIT 1
    """)

    output_ss_common = cursor.fetchone()

    print(f"=== Pairwise view: {pdb1} vs {pdb2} ===") #???????????????????????
    if output_ss_common is not None:
      print("Secondary Structure: " + output_ss_common[0])

#Ausgabe
    #wollen beide zeilen aus Alignment_Sequences ausgeben
    cursor.execute(f"""
      SELECT pdb_id, aligned_sequence FROM alignment_sequences
      WHERE alignment_id = {align}
      AND pdb_id IN ('{pdb1}', '{pdb2}')
      ORDER BY pdb_id
    """)

    output_pair = cursor.fetchall()

    for pid, seq in output_pair: #???????????
      print(f">{pid}\n{seq}")

#Prüfung
  #kein gemeinsames ALignment  -> beide alignments einzeln ausgeben
  else:
    print(f"\n=== Alignments für {pdb1} ===")

#Ausgabe
    #Liste von pdb1 Alignments
    cursor.execute(f"""
      SELECT DISTINCT alignment_id FROM alignment_sequences
      WHERE pdb_id = '{pdb1}'
      ORDER BY alignment_id
    """)

    output_align1_ids = cursor.fetchall()

    if output_align1_ids:
      for (align1_id,) in output_align1_ids:
        print(f"\n ---align1_id {align1_id}---")
        #Secondary Structure
        cursor.execute(f"""
          SELECT secondary_structure FROM alignment_sequences
          WHERE alignment_id = {align1_id}
          AND secondary_structure IS NOT NULL
          LIMIT 1
        """)

        output_align1_ss = cursor.fetchone()
        if output_align1_ss is not None:
          print(output_align1_ss[0])

        cursor.execute(f"""
          SELECT pdb_id, aligned_sequence FROM alignment_sequences
          WHERE alignment_id = {align1_id}
          ORDER BY pdb_id
        """)

        output_align1_msa = cursor.fetchall()

        for pid, seq in output_align1_msa:
          print(f">{pid}\n{seq}")

    # Alignments für pdb2
    print(f"\n=== Alignments für {pdb2} ===")

    cursor.execute(f"""
      SELECT DISTINCT alignment_id FROM alignment_sequences
      WHERE pdb_id = '{pdb2}'
      ORDER BY alignment_id
    """)

    output_align2_ids = cursor.fetchall()

    if output_align2_ids:
      for (align2_id,) in output_align2_ids:
        print(f"\n ---align2_id {align2_id}---")
        # Secondary Structure
        cursor.execute(f"""
          SELECT secondary_structure FROM alignment_sequences
          WHERE alignment_id = {align2_id}
          AND secondary_structure IS NOT NULL
          LIMIT 1
        """)

        output_align2_ss = cursor.fetchone()
        if output_align2_ss is not None:
          print(output_align2_ss[0])

        cursor.execute(f"""
          SELECT pdb_id, aligned_sequence FROM alignment_sequences
          WHERE alignment_id = {align2_id}
          ORDER BY pdb_id
        """)

        output_align2_msa = cursor.fetchall()

        for pid, seq in output_align2_msa:
          print(f">{pid}\n{seq}")

# nur Eingabe von pdb1
else:
  cursor.execute(f"""
    SELECT DISTINCT alignment_id FROM alignment_sequences
    WHERE pdb_id = '{pdb1}'
    ORDER BY alignment_id
  """)

  output_pdb1_ids = cursor.fetchall()

  for (align_id,) in output_pdb1_ids:
    print(align_id)

    #Secondary Structure
    cursor.execute(f"""
      SELECT secondary_structure FROM alignment_sequences
      WHERE alignment_id = {align_id}
      AND secondary_structure IS NOT NULL
      LIMIT 1
    """)

    output_pdb1_ss = cursor.fetchone()
    if output_pdb1_ss is not None:
      print(output_pdb1_ss[0])

    cursor.execute(f"""
      SELECT pdb_id, aligned_sequence FROM alignment_sequences
      WHERE alignment_id = {align_id}
      ORDER BY pdb_id
    """)

    output_pdb1_msa = cursor.fetchall()

    for pid, seq in output_pdb1_msa:
      print(f">{pid}\n{seq}")

cursor.close()
db.close()