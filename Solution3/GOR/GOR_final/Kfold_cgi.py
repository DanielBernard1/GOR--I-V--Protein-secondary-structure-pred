#!/usr/bin/biopython
import argparse
import os
import subprocess
import numpy as np


def kfold(BASE_DIR, form):

    seclib = form.get("--inputSeq_lib")
    gorType  =form.get("--gorType")


    foldcount = 5

    VALIDATION_PATH = os.path.join(BASE_DIR, "jars/validateGor.jar")
    TRAIN_JAR   = os.path.join(BASE_DIR, "jars/trainGor.jar")
    PREDICT_JAR = os.path.join(BASE_DIR, "jars/predict.jar")

    proteins= []
    with open(seclib) as f:
        lines = f.readlines()


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
        train_seclib = os.path.join(BASE_DIR, f"uploads/fold{fold}_train.txt")
        test_fasta = os.path.join(BASE_DIR, f"uploads/fold{fold}_test.fasta")
        model_file = os.path.join(BASE_DIR, f"uploads/fold{fold}_model.seclib")

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

        predict_output = os.path.join(BASE_DIR, f"uploads/fold{fold}_predict.txt")
        with open(predict_output, "w") as f:
            f.write( output.stdout)

        PREDICTION_PATH = os.path.join(BASE_DIR, "uploads/prediction.txt")
        REFERENCE_PATH = os.path.join(BASE_DIR, "uploads/reference.txt")
        DETAILED_PATH = os.path.join(BASE_DIR, "uploads/detailedGor.txt")

        validate_output = subprocess.run(
            ["java", "-jar", VALIDATION_PATH, "-p", PREDICTION_PATH, "-r", REFERENCE_PATH, "-d", DETAILED_PATH, "--format",
             "txt"], capture_output=True, text=True)


        foldvalues = []
        for line in validate_output.stdout.splitlines():
            foldvalues.append(float(line))
        allvalues.append(foldvalues)

        for path in [train_seclib, test_fasta, model_file, predict_output, PREDICTION_PATH, REFERENCE_PATH, DETAILED_PATH]:
            if os.path.exists(path):
                os.remove(path)

headers = ["Number of Proteins", "Mean Protein Length", "Sum of Protein Length",
           "Sum of Predicted Positions", "Q3 mean", "Q2 Dev", "SOV Mean", "SOV Dev",
           "qObs_H Mean", "qObs_E Mean", "qObs_C Mean", "SOV_H Mean", "SOV_E Mean", "SOV_C Mean"]
averages = []
for column in range(len(headers)):





    header_html = "<tr>\n    <th>Fold</th>\n"
    for h in headers:
        header_html += f"    <th>{h}</th>\n"
    header_html += "</tr>"
fold_rows_html = ""
for i, fold in enumerate(allvalues):
    fold_rows_html += f"<tr>\n    <td>Fold {i + 1}</td>\n"
    for value in fold:
        fold_rows_html += f"    <td>{value}</td>\n"
    fold_rows_html += "</tr>\n"








