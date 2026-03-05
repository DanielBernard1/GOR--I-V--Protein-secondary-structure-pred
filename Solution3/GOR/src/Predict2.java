import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class Predict2 extends GorPredictor {
    static Integer [][][][] matrixes;
    static File matrixInput;
    static File fasta;
    static Double[][] correctedValues;
    static Double[][][][] correctedMatrixes;
    public Predict2(File matrixInput, File fasta) {
        this.matrixInput = matrixInput;
        correctedValues = new Double[20][3];
        this.fasta = fasta;
    }

    public static void matrixReader () {

        matrixes  = new Integer[20][3][20][WINDOW_SIZE];
        int counter = 0;
        int counterLoop =0;
        int counterAS = 0;
        boolean isInitialized = false;

        try (Scanner myReader = new Scanner(matrixInput)){

            Integer[][] currentMatrix = new Integer[20][WINDOW_SIZE];

            while (myReader.hasNextLine()) {
                String line = myReader.nextLine();
                if (line.isEmpty()) continue;
                if (line.charAt(0) == '/') continue;
                if (line.matches("^=([A-Z]),([A-Z])=$")){
                    if (!isInitialized){
                        isInitialized = true;
                        continue;

                    }


                    if (counter ==0 ){
                        matrixes[counterLoop][0]=currentMatrix;
                        counter++;
                        currentMatrix = new Integer[20][WINDOW_SIZE];
                    }else if (counter ==1 ){
                        matrixes[counterLoop][1]=currentMatrix;
                        counter++;
                        currentMatrix = new Integer[20][WINDOW_SIZE];
                    }else if (counter ==2 ){
                        matrixes[counterLoop][2]=currentMatrix;
                        counter =0;
                        counterLoop++;
                        currentMatrix = new Integer[20][WINDOW_SIZE];
                    }
                    continue;
                }
                if (AS_TO_INDEX.get(line.charAt(0))== null) continue;
                String[] weights = line.split("\\t");

                for (int i = 1; i < weights.length; i++) {
                    currentMatrix[counterAS][i-1] = Integer.parseInt(weights[i]);
                }
                counterAS++;
                if (counterAS == 20){counterAS = 0;}


            }
            matrixes[counterLoop][2]=currentMatrix;
        }catch (Exception e) {
            System.err.println("An error occurred when reading the matrix file");
            e.printStackTrace();
        }
        setCorrectedValues();
        correctMatrix();



    }
    public static void setCorrectedValues(){
        for (int i = 0; i < 20; i++) {
            double eps = 0.001;
            double countH = 0;
            double countE = 0;
            double countC = 0;

            for (int j = 0; j < 20; j++) {
                for (int pos = 0; pos < WINDOW_SIZE; pos++) {
                    countH += matrixes[i][0][j][pos];
                    countE += matrixes[i][1][j][pos];
                    countC += matrixes[i][2][j][pos];
                }
            }
            double total = countH + countE + countC;
            correctedValues[i][0] = Math.log((total - countH + eps) / (countH + eps));
            correctedValues[i][1] = Math.log((total - countE + eps) / (countE + eps));
            correctedValues[i][2] = Math.log((total - countC + eps) / (countC + eps));

        }
    }
    public static void correctMatrix() {
        correctedMatrixes = new Double[20][3][20][WINDOW_SIZE];
        double epsilon = 0.001;

        for (int i = 0; i < 20; i ++) {
            for (int j = 0; j < 20; j++) {
                for (int pos = 0; pos < WINDOW_SIZE; pos++) {
                    double h = matrixes[i][0][j][pos] +epsilon;
                    double e = matrixes[i][1][j][pos] +epsilon;
                    double c = matrixes[i][2][j][pos] +epsilon;

                    correctedMatrixes[i][0][j][pos] = Math.log(h / (e + c)) + correctedValues[i][0];
                    correctedMatrixes[i][1][j][pos] = Math.log(e / (h + c)) + correctedValues[i][1];
                    correctedMatrixes[i][2][j][pos] = Math.log(c / (h + e)) + correctedValues[i][2];
                }
            }
        }

    }


    public static ProteinData predictionGor2prob(String sequence, String header, boolean probs){
        StringBuilder seq = new StringBuilder();
        String overlapProof = "________" + sequence + "________";
        seq.append(overlapProof);
        StringBuilder struct = new StringBuilder();
        StringBuilder builderH = new StringBuilder();
        StringBuilder builderE = new StringBuilder();
        StringBuilder builderC = new StringBuilder();

        for (int i = STEPS; i < seq.length()-STEPS; i++) {
            String window = seq.substring(i - STEPS, i + STEPS + 1);
            char center = seq.charAt(i);
            if (AS_TO_INDEX.get(center) == null){
                struct.append("C");
                builderH.append("0");
                builderE.append("0");
                builderC.append("9");
                continue;
            }
            int indexOfCenterAs =  getAsToIndex(center);

            double valueC = calculateWindow(correctedMatrixes[indexOfCenterAs][0] ,window);
            double valueE = calculateWindow(correctedMatrixes[indexOfCenterAs][1] ,window);
            double valueH = calculateWindow(correctedMatrixes[indexOfCenterAs][2] ,window);

            double minValue = Math.min(valueE, Math.min(valueC, valueH));
            double maxValue = Math.max(valueE, Math.max(valueC, valueH));
            if (maxValue == valueE) {struct.append("E");}
            else if (maxValue == valueH) {struct.append("H");}
            else {struct.append("C");}
            double total = valueC + valueE + valueH -(3*(minValue));

            int H = (int) Math.round(((valueH -minValue)/ total) * 9);
            int E = (int) Math.round(((valueE -minValue)/ total) * 9);
            int C = (int) Math.round(((valueC -minValue)/ total) * 9);


            builderH.append(H);
            builderE.append(E);
            builderC.append(C);

        }
        if(!probs){return new ProteinData(header, seq.substring(8, seq.length()-8), struct.toString());}
        ProteinData temp = new ProteinData(header, seq.substring(8, seq.length()-8),struct.toString(), builderH.toString(), builderE.toString(), builderC.toString());

        return temp;

    }
    public static ArrayList<ProteinData> predictionGor2FromFasta( boolean probs) {
        HashMap<String,String> fastas = fastaReader(fasta);

        ArrayList<ProteinData> proteinsWithPrediction = new ArrayList<>();
        fastas.forEach((key, value) -> {
            StringBuilder seq = new StringBuilder();
            seq.append(value);

            ProteinData tempProtein = predictionGor2prob( seq.toString(), key, probs);
            proteinsWithPrediction.add(tempProtein);


        });
        return proteinsWithPrediction;

    }


    public static void main(String[] args) {
        String modelPath = null;
        String fastaPath = null;
        String format = null;
        boolean showProbs = false;


        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "--model": modelPath = args[i+1]; break;
                case "--format": format  = args[i+1]; break;
                case "--seq": fastaPath = args[i+1]; break;
                case "--probabilities": showProbs = true; break;
            }
        }
        File fasta = new File(fastaPath);
        File model = new File(modelPath);
        if(modelPath ==  null || fastaPath == null || format == null ){
            System.err.println("output or input is null");
            System.exit(1);

        }

        Predict2 hmm = new  Predict2(model, fasta);
        matrixReader();

        ArrayList<ProteinData> out = predictionGor2FromFasta( showProbs);

        for (ProteinData p : out) {
            if(showProbs) {
                if (format.equalsIgnoreCase("txt")) {
                    p.print(true);
                } else if (format.equalsIgnoreCase("html")) {
                    p.print("html", true);
                }
            }
            else {
                if (format.equalsIgnoreCase("txt")) {
                    p.print(false);
                } else if (format.equalsIgnoreCase("html")) {
                    p.print("html", false);
                }

            }
        }


    }




}
