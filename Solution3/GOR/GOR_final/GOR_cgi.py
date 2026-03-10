import os
import subprocess

def run_predict(BASE_DIR, form):

    GorType = form.getvalue("--Gor_type")
    probabilities = form.getvalue("--probabilities")

    PREDICT = os.path.join(BASE_DIR, "jars/predict.jar")
    MODELS  = os.path.join(BASE_DIR, "GOR_models")

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

    if maf:
        if GorType == "--GOR1":
            model = modelGor1
            if probabilities == "yes":
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--maf", maf, "--format", "txt", "--probabilities"], capture_output=True, text=True, cwd=BASE_DIR)
            else:
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--maf", maf, "--format", "txt"], capture_output=True, text=True, cwd=BASE_DIR)
            output = result.stdout
        elif GorType == "--GOR3":
            model = modelGor3
            if probabilities == "yes":
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--maf", maf, "--format", "txt", "--probabilities"], capture_output=True, text=True, cwd=BASE_DIR)
            else:
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--maf", maf, "--format", "txt"], capture_output=True, text=True, cwd=BASE_DIR)
            output = result.stdout
        elif GorType == "--GOR4":
            model = modelGor4
            if probabilities == "yes":
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--maf", maf, "--format", "txt", "--probabilities"], capture_output=True, text=True, cwd=BASE_DIR)
            else:
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--maf", maf, "--format", "txt"], capture_output=True, text=True, cwd=BASE_DIR)
            output = result.stdout
        else:
            output = "Error: kein GOR Typ ausgewählt"

    elif fasta:
        if GorType == "--GOR1":
            model = modelGor1
            if probabilities == "yes":
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--seq", fasta, "--format", "txt", "--probabilities"], capture_output=True, text=True, cwd=BASE_DIR)
            else:
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--seq", fasta, "--format", "txt"], capture_output=True, text=True, cwd=BASE_DIR)
            output  = result.stdout
        elif GorType == "--GOR3":
            model = modelGor3
            if probabilities == "yes":
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--seq", fasta, "--format", "txt", "--probabilities"], capture_output=True, text=True, cwd=BASE_DIR)
            else:
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--seq", fasta, "--format", "txt"], capture_output=True, text=True, cwd=BASE_DIR)
            output = result.stdout
        elif GorType == "--GOR4":
            model = modelGor4
            if probabilities == "yes":
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--seq", fasta, "--format", "txt", "--probabilities"], capture_output=True, text=True, cwd=BASE_DIR)
            else:
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--seq", fasta, "--format", "txt"], capture_output=True, text=True, cwd=BASE_DIR)
            output = result.stdout
        else:
            output = "Error: kein GOR Typ ausgewählt"
    else:
        output = "Error occurred"

    tmp_path = os.path.join(BASE_DIR, "uploads/temp_seqAndStructure.txt")
    with open(tmp_path, "w") as f:

        f.write(output)

    if fasta and os.path.exists(fasta):
        os.remove(fasta)
    if maf and os.path.exists(maf):
        import shutil
        shutil.rmtree(maf)

    return output