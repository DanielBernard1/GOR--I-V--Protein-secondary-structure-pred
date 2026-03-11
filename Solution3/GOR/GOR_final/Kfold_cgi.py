#!/usr/bin/biopython
import argparse
import os
import subprocess
import numpy as np
import sys


def kfold(BASE_DIR, form):


    gorType  =form.getvalue("--gorType")
    foldcount = int(form.getvalue("--foldcount") or 5)

    seclib = os.path.join(BASE_DIR, "uploads/kfold_input.txt")
    seclib_with_data = form["--input_seclib"].file.read().decode()
    with open(seclib, "w") as f:
        f.write(seclib_with_data)


    VALIDATION_PATH = os.path.join( "jars/validateGor.jar")
    TRAIN_JAR   = os.path.join("jars/train.jar")
    PREDICT_JAR = os.path.join("jars/predict.jar")

    proteins= []
    with open(seclib) as f:
        lines = f.readlines()
    os.remove(seclib)


    i = 0
    while i < len(lines):
        if lines[i].startswith(">"):
            proteins.append({
                "ID": lines[i].strip(),
                "AS":    lines[i+1].strip(),
                "SS":     lines[i+2].strip()
            })
            i += 3
        else:
            i += 1

    np.random.shuffle(proteins)
    folds = np.array_split(proteins, foldcount)


    splits = []

    for i in range(foldcount):
        train = []
        for j, fold in enumerate(folds):
            if j != i:
                train.extend(fold)

        splits.append({
            "fold": i + 1,
            "train": train,
            "test": list(folds[i])
        })

    allvalues = []
    for split in splits:
        fold = split["fold"]
        train_seclib = os.path.join( f"uploads/fold{fold}_train.txt")
        test_fasta = os.path.join(f"uploads/fold{fold}_test.fasta")
        model_file = os.path.join( f"uploads/fold{fold}_model.seclib")
        predict_output = os.path.join( f"uploads/fold{fold}_predict.txt")
        PREDICTION_PATH = os.path.join( f"uploads/fold{fold}_prediction.txt")
        REFERENCE_PATH = os.path.join(f"uploads/fold{fold}_reference.txt")
        DETAILED_PATH = os.path.join( f"uploads/fold{fold}_detailed.txt")

        with open(train_seclib, "w") as f:
            for p in split["train"]:
                f.write(f"{p['ID']}\n{p['AS']}\n{p['SS']}\n")
        subprocess.run([
            "java", "-jar", TRAIN_JAR,
            "--db", train_seclib,
            "--method", gorType,
            "--model", model_file

        ], capture_output=True, text=True)

        with open(test_fasta, "w") as f:
            for p in split["test"]:
                f.write(f"{p['ID']}\n{p['AS'].replace('AS ', '')}\n")
        output = subprocess.run([
            "java" , "-jar", PREDICT_JAR,
            "--model", model_file,
            "--seq", test_fasta,
            "--format", "txt"
        ], capture_output=True, text=True)


        with open(predict_output, "w") as f:
            f.write( output.stdout)

        with open(REFERENCE_PATH, "w") as f:
            for p in split["test"]:
                f.write(f"{p['ID']}\n{p['AS']}\n{p['SS']}\n")

        with open(PREDICTION_PATH, "w") as f:
            f.write(output.stdout)

        validate_output = subprocess.run(
            ["java", "-jar", VALIDATION_PATH,
             "-p", PREDICTION_PATH,
             "-r", REFERENCE_PATH,
             "-d", DETAILED_PATH,
             "-f", "txt"],
            capture_output=True, text=True)



        foldvalues = []
        for line in validate_output.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            else:
                foldvalues.append(round(float(line),2))


        allvalues.append(foldvalues)


        for path in [train_seclib, test_fasta, model_file, predict_output, PREDICTION_PATH, REFERENCE_PATH, DETAILED_PATH]:
            if os.path.exists(path):
                os.remove(path)

    averages = []
    for col in range(len(allvalues[0])):
        total = 0
        for row in allvalues:
            total += row[col]
        averages.append(total / len(allvalues))

    headers = ["Number of Proteins", "Mean Protein Length", "Sum of Protein Length",
               "Sum of Predicted Positions", "Q3 Mean", "SOV Mean", "SOV Dev",
               "qObs_H Mean", "qObs_E Mean", "qObs_C Mean",
               "SOV_H Mean", "SOV_E Mean", "SOV_C Mean"]


    header= "<th style='padding: 8px 12px;'>Fold</th>\n"
    for h in headers:
        header += f"<th style='padding: 8px 12px;'>{h}</th>\n"

    fold = ""
    for i, fold in enumerate(allvalues):
        fold += "<tr>\n"
        fold += f"<td style='padding: 8px 12px;'>Fold {i + 1}</td>\n"
        for value in fold:
            fold += f"<td style='padding: 8px 12px; text-align:right;'>{value}</td>\n"
        fold += "</tr>\n"

    avg = "<tr style='background: #ecf0f1; font-weight: bold;'>\n"
    avg += "<td style='padding: 8px 12px;'>Average</td>\n"
    for value in averages:
        avg += f"<td style='padding: 8px 12px; text-align:right;'>{value}</td>\n"
    avg += "</tr>\n"

    table_html = f"""
     <div style="overflow-x: auto; margin-top: 1rem;">
         <table style="border-collapse: collapse; width: 100%; font-size: 0.85rem;">
             <thead>
                 <tr style="background: #2c3e50; color: white; text-align: center;">
                     {header}
                 </tr>
             </thead>
             <tbody>
                 {fold}
                 {avg}
             </tbody>
         </table>
     </div>"""

    return table_html







