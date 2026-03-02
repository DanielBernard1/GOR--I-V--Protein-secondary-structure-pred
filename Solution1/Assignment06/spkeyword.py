#!/usr/bin/env python3
import argparse



#Ausgabe AC-keys zugehörig zu jeweiligen keywords lexikographisch sortiert
#Eingabe (mehrere) Keywords


parser = argparse.ArgumentParser(description="Prints all AC-Keys of a given keyword")
parser.add_argument("--keyword", nargs="+", required=True, help="Keyword(s) to search for")
parser.add_argument("--swissprot", type=str, required=True, help="Path to the file containing the keywords")

args = parser.parse_args()
file_path = args.swissprot
inputs = args.keyword                        #Liste aller Keywords nach denen gesucht werden soll

output = set()                               #Set damit keine doppelten Ids angegeben werden

ids = []
hit = False

with open(file_path, "r") as f:

    for line in f:
        if line.startswith("AC"):
            id = line[5:].strip()               # skip 0 bis 4 --> wir müssen kw nicht mit ausgeben und haben darauf folgend 3 Leerzeichen
            for ac in id.split(";"):
                ac = ac.strip()
                if ac:                          #filtern leere Teile raus
                    ids.append(ac)
        elif line.startswith("KW"):
            neu = line[5:].strip().rstrip(".")  #"." und ";" kommen nur am ende vor dort ("rstrip()")
            keys = neu.split(";")
            for key in keys:
                k = key.strip().rstrip(";").rstrip(".")
                if k in inputs:
                    hit = True
        elif line.startswith("//"):             #arbeiten Entryweise --> ("//") zeigt Ende des Entrys an
            if hit:                             #haben wir mindestens 1nen Hit
                output.update(ids)
            ids = []                            #beide Resetten für nächsten Eintrag
            hit = False


for a in sorted(output):                        #lexikographisch sortiert
    print (a)


