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

pdb1 = args.pdb1.strip().upper().split("_")[0]
pdb2 = args.pdb2.strip().upper().split("_")[0] if args.pdb2 else ""

cursor = db.cursor()

#pdb-ids im selben Alignment??
if pdb2:

  # 1 SELECT: hol ALLE Zeilen (full MSA) für ALLE gemeinsamen alignment_ids
  # secondary_structure kommt direkt mit (du brauchst keinen extra SS-Select mehr)
  cursor.execute(f"""
    SELECT s.alignment_id, s.pdb_id, s.aligned_sequence, s.secondary_structure FROM alignment_sequences s
    WHERE s.alignment_id IN (
      SELECT DISTINCT a1.alignment_id
      FROM alignment_sequences a1
      JOIN alignment_sequences a2 ON a1.alignment_id = a2.alignment_id
      WHERE a1.pdb_id = '{pdb1}' AND a2.pdb_id = '{pdb2}'
    )
    ORDER BY s.alignment_id, s.pdb_id
  """)

  output_common_full = cursor.fetchall() #brauchen nur einen

  # Wenn leer => kein gemeinsames Alignment
  if output_common_full:

    # Wir geben pro alignment_id aus:
    # - SS einmal (aus erster Zeile, wo secondary_structure nicht NULL ist)
    # - Pairwise view (nur pdb1/pdb2)
    # - Full MSA (alle Zeilen)
    current_align = None
    current_ss = None
    rows_for_align = []

    for align_id, pid, seq, ss in output_common_full:
      if current_align is None:
        current_align = align_id

      # Wechsel zu neuem alignment_id => vorherigen Block ausgeben
      if align_id != current_align:
        print(f"{current_align}\n")

        print(f"=== Pairwise view: {pdb1} vs {pdb2} ===") #???????????????????????
        if current_ss is not None:
          print("Secondary Structure: " + current_ss)

        for pid2, seq2 in rows_for_align:
          if pid2 == pdb1 or pid2 == pdb2:
            print(f">{pid2}\n{seq2}")

        # Full MSA
        for pid2, seq2 in rows_for_align:
          print(f">{pid2}\n{seq2}")

        # Reset für neuen Block
        current_align = align_id
        current_ss = None
        rows_for_align = []

      # SS merken (erste nicht-NULL reicht)
      if current_ss is None and ss is not None:
        current_ss = ss

      # Zeilen sammeln
      rows_for_align.append((pid, seq))

    # letzten Block ausgeben
    print(f"{current_align}\n")

    print(f"=== Pairwise view: {pdb1} vs {pdb2} ===") #???????????????????????
    if current_ss is not None:
      print("Secondary Structure: " + current_ss)

    for pid2, seq2 in rows_for_align:
      if pid2 == pdb1 or pid2 == pdb2:
        print(f">{pid2}\n{seq2}")

    # Full MSA
    for pid2, seq2 in rows_for_align:
      print(f">{pid2}\n{seq2}")

  #kein gemeinsames ALignment  -> beide alignments einzeln ausgeben
  else:
    print(f"\n=== Alignments für {pdb1} ===")

    # 1 SELECT für alle Alignments von pdb1 (inkl. SS + full MSA)
    cursor.execute(f"""
      SELECT s.alignment_id, s.pdb_id, s.aligned_sequence, s.secondary_structure
      FROM alignment_sequences s
      WHERE s.alignment_id IN (
        SELECT DISTINCT alignment_id
        FROM alignment_sequences
        WHERE pdb_id = '{pdb1}'
      )
      ORDER BY s.alignment_id, s.pdb_id
    """)
    output_align1_full = cursor.fetchall()

    current_align1 = None
    current_ss1 = None
    rows_for_align1 = []

    for align_id, pid, seq, ss in output_align1_full:
      if current_align1 is None:
        current_align1 = align_id

      if align_id != current_align1:
        print(f"\n ---align1_id {current_align1}---")
        #Secondary Structure
        if current_ss1 is not None:
          print(current_ss1)

        for pid2, seq2 in rows_for_align1:
          print(f">{pid2}\n{seq2}")

        current_align1 = align_id
        current_ss1 = None
        rows_for_align1 = []

      if current_ss1 is None and ss is not None:
        current_ss1 = ss
      rows_for_align1.append((pid, seq))

    if current_align1 is not None:
      print(f"\n ---align1_id {current_align1}---")
      #Secondary Structure
      if current_ss1 is not None:
        print(current_ss1)

      for pid2, seq2 in rows_for_align1:
        print(f">{pid2}\n{seq2}")

    # Alignments für pdb2
    print(f"\n=== Alignments für {pdb2} ===")

    # 1 SELECT für alle Alignments von pdb2 (inkl. SS + full MSA)
    cursor.execute(f"""
      SELECT s.alignment_id, s.pdb_id, s.aligned_sequence, s.secondary_structure
      FROM alignment_sequences s
      WHERE s.alignment_id IN (
        SELECT DISTINCT alignment_id
        FROM alignment_sequences
        WHERE pdb_id = '{pdb2}'
      )
      ORDER BY s.alignment_id, s.pdb_id
    """)
    output_align2_full = cursor.fetchall()

    current_align2 = None
    current_ss2 = None
    rows_for_align2 = []

    for align_id, pid, seq, ss in output_align2_full:
      if current_align2 is None:
        current_align2 = align_id

      if align_id != current_align2:
        print(f"\n ---align2_id {current_align2}---")
        # Secondary Structure
        if current_ss2 is not None:
          print(current_ss2)

        for pid2, seq2 in rows_for_align2:
          print(f">{pid2}\n{seq2}")

        current_align2 = align_id
        current_ss2 = None
        rows_for_align2 = []

      if current_ss2 is None and ss is not None:
        current_ss2 = ss
      rows_for_align2.append((pid, seq))

    if current_align2 is not None:
      print(f"\n ---align2_id {current_align2}---")
      # Secondary Structure
      if current_ss2 is not None:
        print(current_ss2)

      for pid2, seq2 in rows_for_align2:
        print(f">{pid2}\n{seq2}")

# nur Eingabe von pdb1
else:
  # 1 SELECT total: alle Alignments (full MSA) zu pdb1
  cursor.execute(f"""
    SELECT s.alignment_id, s.pdb_id, s.aligned_sequence, s.secondary_structure
    FROM alignment_sequences s
    WHERE s.alignment_id IN (
      SELECT DISTINCT alignment_id
      FROM alignment_sequences
      WHERE pdb_id = '{pdb1}'
    )
    ORDER BY s.alignment_id, s.pdb_id
  """)

  output_pdb1_full = cursor.fetchall()

  current_align = None
  current_ss = None
  rows_for_align = []

  for align_id, pid, seq, ss in output_pdb1_full:
    if current_align is None:
      current_align = align_id

    if align_id != current_align:
      print(current_align)

      #Secondary Structure
      if current_ss is not None:
        print(current_ss)

      for pid2, seq2 in rows_for_align:
        print(f">{pid2}\n{seq2}")

      current_align = align_id
      current_ss = None
      rows_for_align = []

    if current_ss is None and ss is not None:
      current_ss = ss
    rows_for_align.append((pid, seq))

  if current_align is not None:
    print(current_align)

    #Secondary Structure
    if current_ss is not None:
      print(current_ss)

    for pid2, seq2 in rows_for_align:
      print(f">{pid2}\n{seq2}")

cursor.close()
db.close()