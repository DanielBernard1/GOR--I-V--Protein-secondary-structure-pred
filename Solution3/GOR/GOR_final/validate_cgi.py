import os
import subprocess

def run_validate(BASE_DIR, form):

    PREDICTION_PATH = os.path.join( "uploads/prediction.txt")
    REFERENCE_PATH  = os.path.join("uploads/reference.txt")
    VALIDATION_PATH = os.path.join("jars/validateGor.jar")
    DETAILED_PATH   = os.path.join("uploads/detailedGor.txt")

    if "--prediction_file" in form and form["--prediction_file"].filename:
        prediction = form["--prediction_file"].file.read().decode()
    else:
        prediction = form.getvalue("--prediction", "")

    if "--reference_file" in form and form["--reference_file"].filename:
        reference = form["--reference_file"].file.read().decode()
    else:
        reference = form.getvalue("--reference", "")

    with open(PREDICTION_PATH, "w") as f:
        f.write(prediction)
    with open(REFERENCE_PATH, "w") as f:
        f.write(reference)

    result = subprocess.run(
        ["java", "-jar", VALIDATION_PATH, "-p", PREDICTION_PATH, "-r", REFERENCE_PATH, "-d", DETAILED_PATH, "--format", "txt"],
        capture_output=True, text=True)

    return result.stdout