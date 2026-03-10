import os
import subprocess

def run_predict(BASE_DIR, form):

    GorType = form.getvalue("--Gor_type")

    fasta = form.getvalue("--fasta")

    maf = form.getvalue("--maf")
    probabilities = form.getvalue("--probabilities")

    JARS    = os.path.join(BASE_DIR, "jars")
    PREDICT = os.path.join(JARS, "predict.jar")

    MODELS  = os.path.join(BASE_DIR, "GOR_models")


    modelGor1 = os.path.join(MODELS, "gor1_cb513_model.txt")
    modelGor3 = os.path.join(MODELS, "gor3_cb513_model.txt")

    modelGor4 = os.path.join(MODELS, "gor4_cb513_model.txt")

    os.makedirs(os.path.join(BASE_DIR, "uploads"), exist_ok=True)

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
    elif fasta:
        if GorType == "--GOR1":
            model = modelGor1
            if probabilities == "yes":
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--fasta", fasta, "--format", "txt", "--probabilities"], capture_output=True, text=True)
            else:
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--fasta", fasta, "--format", "txt"], capture_output=True, text=True)
            output = result.stdout
        elif GorType == "--GOR3":
            model = modelGor3
            if probabilities == "yes":
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--fasta", fasta, "--format", "txt", "--probabilities"], capture_output=True, text=True)
            else:
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--fasta", fasta, "--format", "txt"], capture_output=True, text=True)
            output = result.stdout
        elif GorType == "--GOR4":

            model = modelGor4
            if probabilities == "yes":
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--fasta", fasta, "--format", "txt", "--probabilities"], capture_output=True, text=True)
            else:
                result = subprocess.run(["java", "-jar", PREDICT, "--model", model, "--fasta", fasta, "--format", "txt"], capture_output=True, text=True)
            output = result.stdout
    else:

        output = "Error occurred"

    tmp_path = os.path.join(BASE_DIR, "uploads/temp_seqAndStructure.txt")


    with open(tmp_path, "w") as f:
        f.write(output)


    return output