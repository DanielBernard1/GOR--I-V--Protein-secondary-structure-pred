import os
import subprocess
import shutil
import copy
from collections import Counter

def postprocess(input, output, windowsize=None):
    window = int(windowsize) if windowsize else 5

    proteins = []

    with open(input) as g:
        half = window // 2

        for line in g:
            if line.startswith(">"):
                header = line.strip()
                seq = g.readline()
                predicted = (g.readline()[2:].strip())
                proteins.append((header, list(seq), list(predicted)))

    proteinsmoothed = copy.deepcopy(proteins)
    for a, p in enumerate(proteins):
        for i, char in enumerate(p[2]):
            if i - half < 0 or i + half >= len(p[2]):
                continue
            seen = []
            for j in range(i - half, i + half + 1):
                seen.append(p[2][j])
            häufigster = Counter(seen).most_common(1)[0][0]
            proteinsmoothed[a][2][i] = häufigster

    with open(output, "w", newline="\n") as f:
        for row in proteinsmoothed:
            f.write(row[0] + "\n" + ''.join(row[1]) + "SS " + ''.join(row[2]) + "\n")

def run_predict(BASE_DIR, form):

    GorType = form.getvalue("--Gor_type")
    probabilities = form.getvalue("--probabilities")

    PREDICT = os.path.join( "jars/predict.jar")
    MODELS  = os.path.join( "GOR_models")

    modelGor1 = os.path.join(MODELS, "gor1_cb513_model.txt")
    modelGor3 = os.path.join(MODELS, "gor3_cb513_model.txt")
    modelGor4 = os.path.join(MODELS, "gor4_cb513_model.txt")

    os.makedirs(os.path.join("uploads"), exist_ok=True)

    fasta = None
    maf = None
    custom_model = None

    if "--model_file" in form and form["--model_file"].filename:
        custom_model = os.path.join("uploads/custom_model.txt")
        with open(custom_model, "wb") as f:
            f.write(form["--model_file"].file.read())
        filename = form["--model_file"].filename
        if "gor1" in filename:

            modelGor1 = custom_model
            if GorType != "--GOR1":
                os.remove(custom_model)
                return "wrong combination of GOR and model", None

        elif "gor3" in filename:
            modelGor3 = custom_model
            if GorType != "--GOR3":
                os.remove(custom_model)
                return "wrong combination of GOR and model", None
        elif "gor4" in filename:
            modelGor4 = custom_model
            if GorType != "--GOR4":
                os.remove(custom_model)
                return "wrong combination of GOR and model", None



    if "--fasta" in form and form["--fasta"].filename:
        fasta = os.path.join( "uploads/input.fasta")
        with open(fasta, "wb") as f:
            f.write(form["--fasta"].file.read())

    if "--maf" in form and form["--maf"].filename:
        maf = os.path.join("uploads/maf_input")
        os.makedirs(maf, exist_ok=True)
        filename = form["--maf"].filename
        with open(os.path.join(maf, filename), "wb") as f:
            f.write(form["--maf"].file.read())

    if maf:
        if GorType == "--GOR1":
            model = modelGor1
            if probabilities == "yes":
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--maf", maf, "--format", "txt", "--probabilities"], capture_output=True, text=True)
            else:
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--maf", maf, "--format", "txt"], capture_output=True, text=True)
            output = result.stdout
        elif GorType == "--GOR3":
            model = modelGor3
            if probabilities == "yes":
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--maf", maf, "--format", "txt", "--probabilities"], capture_output=True, text=True)
            else:
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--maf", maf, "--format", "txt"], capture_output=True, text=True)
            output = result.stdout
        elif GorType == "--GOR4":
            model = modelGor4
            if probabilities == "yes":
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--maf", maf, "--format", "txt", "--probabilities"], capture_output=True, text=True)
            else:
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--maf", maf, "--format", "txt"], capture_output=True, text=True)
            output = result.stdout
        else:
            output = "Error: kein GOR Typ ausgewählt"

    elif fasta:
        if GorType == "--GOR1":
            model = modelGor1
            if probabilities == "yes":
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--seq", fasta, "--format", "txt", "--probabilities"], capture_output=True, text=True)
            else:
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--seq", fasta, "--format", "txt"], capture_output=True, text=True)
            output  = result.stdout
        elif GorType == "--GOR3":
            model = modelGor3
            if probabilities == "yes":
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--seq", fasta, "--format", "txt", "--probabilities"], capture_output=True, text=True)
            else:
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--seq", fasta, "--format", "txt"], capture_output=True, text=True)
            output = result.stdout
        elif GorType == "--GOR4":
            model = modelGor4
            if probabilities == "yes":
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--seq", fasta, "--format", "txt", "--probabilities"], capture_output=True, text=True)
            else:
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--seq", fasta, "--format", "txt"], capture_output=True, text=True)
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
        shutil.rmtree(maf)
    if custom_model and os.path.exists(custom_model):
        os.remove(custom_model)

    if form.getvalue("--postprocess") == "yes":
        pp_output_path = os.path.join(BASE_DIR, "uploads/temp_seqAndStructure_pp.txt")
        try:
            postprocess(tmp_path, pp_output_path)
        except Exception as e:
            pp_output_path = str(e)
    else:
        pp_output_path = None

    return output, pp_output_path
