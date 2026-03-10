import os
import subprocess

def run_predict(BASE_DIR, form):

    GorType = form.getvalue("--Gor_type")
    probabilities = form.getvalue("--probabilities")

    JARS    = os.path.join("jars")
    PREDICT = os.path.join(JARS, "predict.jar")
    MODELS  = "GOR_models"

    modelGor1 = os.path.join(MODELS, "gor1_cb513_model.txt")
    modelGor3 = os.path.join(MODELS, "gor3_cb513_model.txt")
    modelGor4 = os.path.join(MODELS, "gor4_cb513_model.txt")

    os.makedirs(os.path.join(BASE_DIR, "uploads"), exist_ok=True)

    fasta = None
    maf = None

    if "--fasta" in form and form["--fasta"].filename:
        fasta = os.path.join(BASE_DIR, "uploads/input.fasta")
        with open(fasta, "wb") as f:
            f.write(form["--fasta"].file.read())

    if "--maf" in form and form["--maf"].filename:
        maf = os.path.join(BASE_DIR, "uploads/maf_input")
        os.makedirs(maf, exist_ok=True)
        filename = form["--maf"].filename
        with open(os.path.join(maf, filename), "wb") as f:
            f.write(form["--maf"].file.read())

    return f"DEBUG: maf={maf}, fasta={fasta}, GorType={GorType}"