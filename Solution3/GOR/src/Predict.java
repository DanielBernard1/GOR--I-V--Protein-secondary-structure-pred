
import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class Predict extends GorPredictor {

    private static Integer[][] matrixH;
    private static Integer[][] matrixE;
    private static Integer[][] matrixC;
    private static double correctionH;
    private static double correctionE;
    private static double correctionC;
    private static Double[][] CorrectedMatrixH;
    private static Double[][] CorrectedMatrixE;
    private static Double[][] CorrectedMatrixC;



    public static void matrixReader (File file) {
        ArrayList<Integer[][]> matrixHEC = new ArrayList<>();
        Integer[][] temp = new Integer[20][WINDOW_SIZE];
        int counter = 0;
        try (Scanner myReader = new Scanner(file)){
            while (myReader.hasNextLine()) {
                String line = myReader.nextLine();

                if (line.isEmpty()) continue;
                String[] weights = line.split("\\t");

                if (line.startsWith("A") && counter > 0) {
                    matrixHEC.add(temp);
                    temp = new Integer[20][WINDOW_SIZE];
                }
                char as = line.charAt(0);
                if(!AS_TO_INDEX.containsKey(as)) {
                    continue;
                }
                Integer row = getAsToIndex(as);



                for (int i = 1; i < weights.length; i++) {
                    temp[row][i-1] = Integer.parseInt(weights[i]);
                }
                counter++;

            }
            matrixHEC.add(temp);
        }catch (Exception e) {
            System.err.println("An error occurred when reading the matrix file");
            e.printStackTrace();
        }
        matrixH = matrixHEC.get(2);
        matrixE = matrixHEC.get(1);
        matrixC = matrixHEC.get(0);
        double countH = sum(matrixH);
        double countE = sum(matrixE);
        double countC = sum(matrixC);
        double total = countH + countE + countC;
        correctionH = Math.log((total -countH)/countH);
        correctionE = Math.log((total -countE)/countE);
        correctionC = Math.log((total -countC)/countC);


    }
    public static void correctMatrix() {
        CorrectedMatrixH = new Double[20][WINDOW_SIZE];
        CorrectedMatrixE = new Double[20][WINDOW_SIZE];
        CorrectedMatrixC = new Double[20][WINDOW_SIZE];
        for (int row = 0; row < 20 ; row++) {
            for (int col = 0; col < WINDOW_SIZE; col++) {
                double h = matrixH[row][col];
                double e = matrixE[row][col];
                double c = matrixC[row][col];

                CorrectedMatrixH[row][col] = Math.log(h / (e + c)) + correctionH;
                CorrectedMatrixE[row][col] = Math.log(e / (h + c)) + correctionE;
                CorrectedMatrixC[row][col] = Math.log(c / (h + e)) + correctionC;

            }
        }

    }



    public static ProteinData predictionGor1(File trainingData, String sequence, String header, boolean create_matrix) {
        if (create_matrix) {matrixReader (trainingData);correctMatrix();}

        StringBuilder seq = new StringBuilder();
        String overlapProof = "________" + sequence + "________";
        seq.append(overlapProof);
        StringBuilder struct = new StringBuilder();
        for (int i = STEPS; i < seq.length()-STEPS; i++) {
            String window = seq.substring(i-STEPS, i + STEPS+1);

            double valueC = calculateWindow(CorrectedMatrixC, window);
            double valueE = calculateWindow(CorrectedMatrixE, window);
            double valueH = calculateWindow(CorrectedMatrixH, window);


            double maxValue = Math.max(valueE, Math.max(valueC, valueH));
            if (maxValue == valueE) {
                struct.append("E");
            }

            else if (maxValue == valueH) {
                struct.append("H");
            }
            else {
                struct.append("C");
            }
        }
        ProteinData Protein = new ProteinData(header, seq.substring(8, seq.length()-8), struct.toString());
        return Protein;
    }
    public static ProteinData predictionGor1prob(File trainingData, String sequence, String header, boolean create_matrix){
        StringBuilder seq = new StringBuilder();
        String overlapProof = "________" + sequence + "________";
        seq.append(overlapProof);
        StringBuilder struct = new StringBuilder();
        StringBuilder builderH = new StringBuilder();
        StringBuilder builderE = new StringBuilder();
        StringBuilder builderC = new StringBuilder();

        for (int i = STEPS; i < seq.length()-STEPS; i++) {
            String window = seq.substring(i - STEPS, i + STEPS + 1);

            double valueC = calculateWindow(CorrectedMatrixC, window);
            double valueE = calculateWindow(CorrectedMatrixE, window);
            double valueH = calculateWindow(CorrectedMatrixH, window);

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
        return new ProteinData(header, seq.substring(8, seq.length()-8),struct.toString(), builderH.toString(), builderE.toString(), builderC.toString());

    }
    public static ArrayList<ProteinData> predictionGor1FromFasta(File fasta, File trainingData, boolean probs) {
        HashMap<String,String> fastas = fastaReader(fasta);
        matrixReader (trainingData);
        correctMatrix();
        ArrayList<ProteinData> proteinsWithPrediction = new ArrayList<>();
        fastas.forEach((key, value) -> {
            StringBuilder seq = new StringBuilder();
            seq.append(value);
            if (probs) {
                ProteinData tempProtein = predictionGor1prob(trainingData, seq.toString(), key, probs);
                proteinsWithPrediction.add(tempProtein);
            }else{
                ProteinData tempProtein = predictionGor1(trainingData, seq.toString(), key, false);
                proteinsWithPrediction.add(tempProtein);
            }

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

        ArrayList<ProteinData> out = predictionGor1FromFasta(fasta, model, showProbs);

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

