import os
import subprocess

def run_train(BASE_DIR, form):



    TRAIN_PATH = os.path.join("jars/train.jar")
    method = form.getvalue("--method")
    db = form["--db"].file.read().decode()
    db_file = os.path.join("uploads/db_model.txt")

    if method == "1":
        method= "gor1"
    elif method == "3":
        method= "gor2"
    elif method == "4":
        method= "gor3"

    modeloutput = os.path.join(f"uploads/model{method}.txt")

    with open(db_file, "w") as f:
        f.write(db)


    result = subprocess.run(
        ["java", "-jar", TRAIN_PATH, "--db", db_file, "--method", method, "--model", modeloutput],
        capture_output=True, text=True)

    if db_file and os.path.exists(db_file):
        os.remove(db_file)

    return result.stdout