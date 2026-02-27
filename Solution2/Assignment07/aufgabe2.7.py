#!/usr/bin/python3
import re
# from FASTAreader import FASTAreader
import argparse as ap
import sys
import urllib.request

parser = ap.ArgumentParser()
src1 = parser.add_mutually_exclusive_group(required=True)
src1.add_argument('--fasta')
src1.add_argument('--db')
src = parser.add_mutually_exclusive_group(required=True)
src.add_argument('--pattern')
src.add_argument('--web')
#
args = parser.parse_args()
filepath = args.fasta



if(args.fasta):
    class FASTAreader:
        def read_fasta_function(self, filepath):
            self.motifs = {}
            self.indexes = []

            current_key = None
            for line in filepath:
                s = line.strip()
                if not s:
                    continue

                if s.startswith(">"):
                    current_key = s
                    self.motifs[current_key] = []
                    self.indexes.append(s)
                elif current_key is not None:
                    self.motifs[current_key].append(s)


            for k in self.motifs:
                self.motifs[k] = "".join(self.motifs[k])

            return self.motifs
    reader = FASTAreader()
    with open(filepath, "r") as f:
        fasta_as_dictafasta = reader.read_fasta_function(f)

input = ""

if args.web is not None:
    ac2 = args.web
    url = "https://prosite.expasy.org/" + ac2 + ".txt"
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")

    for line in data.splitlines(True):

        if line[:2] == "PA":
            pattern = line[5:-2]
            input = pattern
            break
        else:
            continue
else:
    input = args.pattern

output_list = []

for i in input:
    if i == "{":
        output_list.append("[^")
    elif i == "}":
        output_list.append("]")
    elif i == "x":
        output_list.append(".")
    elif i == "(":
        output_list.append("{")
    elif i == ")":
        output_list.append("}")
    elif i == "<":
        output_list.append("^")
    elif i == ">":
        output_list.append("$")
    elif i == "?":
        output_list.append(".")
    elif i == "*":
        output_list.append(".*")
    elif i == "-":
        continue
    else:
        output_list.append(i)
output_list = "".join(output_list)
input = re.compile(output_list)


if args.db:
    db = mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="bioprakt15",
        password="$1$/NQ9xkkh$BnZDjreVX/1q0MGqWEc3M0",
        database="bioprakt15"
    )
    cursor = db.cursor()

    cursor.execute(f'''
    SELECT seq_id, REGEXP_SUBSTR(seq, '{input}') AS matched

    FROM Sequenz;

    ''')
    Output = cursor.fetchall()
    for r in Output:
        print(f'{r[0]}\t{r[1]}')

    exit()


# print(output_list)




lookahead_pattern = re.compile(f'(?=({input.pattern}))')

for key, value in fasta_as_dict.items():
    if input.search(value):
        for m in re.finditer(lookahead_pattern, value):
            print(f"{key}\t{m.start()}\t{m.group(1)}")

