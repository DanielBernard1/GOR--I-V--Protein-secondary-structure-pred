import javax.xml.stream.FactoryConfigurationError;
import java.io.File;
import java.util.ArrayList;
import java.util.Scanner;

public class Predict3 extends GorPredictor{
    static Integer [][][][][][] matrixes;
    static Integer [][][][] matrixes2;
    static File matrixInput;
    static File fasta;
    static Double[][][] correctedValues;
    static Double[][][][][][] correctedMatrixes;
    static Double[][] correctedValues2;
    static Double[][][][] correctedMatrixes2;
    public Predict3(File matrixInput, File fasta) {
        this.matrixInput = matrixInput;
        this.fasta = fasta;

    }

    public static void matrixReader () {
        matrixes = new Integer[3][20][20][17][20][17];
        matrixes2 = new Integer[20][3][20][WINDOW_SIZE];
        int currentStruct = 0;
        int currentAS1 = 0;
        int currentAS2 = 0;
        int currentPos = 0;

        int counter = 0;
        int counterLoop = 0;


        int counterAS = 0;
        boolean isInitialized = false;
        boolean Gor3 = false;

        try (Scanner myReader = new Scanner(matrixInput)) {

            Integer[][] currentMatrix2 = new Integer[20][WINDOW_SIZE];
            Integer[][][][] currentMatrix = new Integer[20][3][20][WINDOW_SIZE];

            while (myReader.hasNextLine()) {
                String line = myReader.nextLine();
                if (line.isEmpty()) continue;
                if (line.charAt(0) == '/') continue;
                if (line.matches("^=([A-Z]),([A-Z]),([A-Z]),(-?\\d+)=$")) {
                    String[] header = line.replace("=", "").split(",");
                    currentStruct = indexforstruct(header[0].charAt(0));
                    currentAS1 = getAsToIndex(header[1].charAt(0));
                    currentAS2 = getAsToIndex(header[2].charAt(0));
                    currentPos = Integer.parseInt(header[3]) +8;
                    counterAS = 0;
                    continue;

                }


                if (line.matches("^=([A-Z]),([A-Z])=$")) {
                    Gor3 = true;
                    if (!isInitialized) {isInitialized = true; counter= 0; continue; }

                    if (counter == 0) {

                        matrixes2[counterLoop][0] = currentMatrix2;
                        counter++;
                        currentMatrix2 = new Integer[20][WINDOW_SIZE];

                    } else if (counter == 1) {
                        matrixes2[counterLoop][1] = currentMatrix2;
                        counter++;
                        currentMatrix2 = new Integer[20][WINDOW_SIZE];
                    } else if (counter == 2) {
                        matrixes2[counterLoop][2] = currentMatrix2;
                        counter = 0;
                        counterLoop++;
                        currentMatrix2 = new Integer[20][WINDOW_SIZE];
                    }
                    continue;
                }

                if (AS_TO_INDEX.get(line.charAt(0)) == null) continue;
                String[] weights = line.split("\\t");

                if(!Gor3){
                    for (int i = 1; i < weights.length; i++) {
                        matrixes[currentStruct][currentAS1][currentAS2][currentPos][counterAS][i - 1] = Integer.parseInt(weights[i]);
                    }

                    counterAS++;
                    if (counterAS == 20) {
                        counterAS = 0;
                    }


                } else {

                    for (int i = 1; i < weights.length; i++) {
                        currentMatrix2[counterAS][i - 1] = Integer.parseInt(weights[i]);
                    }
                    counterAS++;
                    if (counterAS == 20) {
                        counterAS = 0;
                    }

                }


            }
            matrixes2[counterLoop][counter] = currentMatrix2;
        } catch (Exception e) {
            System.err.println("An error occurred when reading the matrix file");
            e.printStackTrace();
        }


    }
    public static void setCorrectedValues(){
        correctedValues = new Double[3][20][20];
        double eps = 0.001;
        for (int struc = 0; struc < 3; struc++) {
            for (int as1 = 0; as1 < 20; as1++) {
                for (int as2 = 0; as2 < 20; as2++) {
                    double countH = 0;
                    double countE = 0;
                    double countC = 0;
                    for (int i = 0; i < 17; i++) {
                        for (int row = 0; row < 20; row++) {
                            for (int col = 0; col < 17; col++) {
                                countH += matrixes[0][as1][as2][i][row][col];
                                countE += matrixes[1][as1][as2][i][row][col];
                                countC += matrixes[2][as1][as2][i][row][col];
                            }
                        }
                    }
                    double total = countH + countE + countC;
                    correctedValues[0][as1][as2] = Math.log((total - countH + eps) / (countH + eps));
                    correctedValues[1][as1][as2] = Math.log((total - countE + eps) / (countE + eps));
                    correctedValues[2][as1][as2] = Math.log((total - countC + eps) / (countC + eps));
                }
            }
        }
    }
    public static void correctMatrix() {
        correctedMatrixes = new Double[3][20][20][WINDOW_SIZE][20][WINDOW_SIZE];
        double epsilon = 0.001;
        for (int as1 = 0; as1 < 20; as1++) {
            for (int as2 = 0; as2 < 20; as2++) {
                for (int i = 0; i < 17; i++) {
                    for (int row = 0; row < 20; row++) {
                        for (int col = 0; col < 17; col++) {
                            double h = matrixes[0][as1][as2][i][row][col] + epsilon;
                            double e = matrixes[1][as1][as2][i][row][col] + epsilon;
                            double c = matrixes[3][as1][as2][i][row][col] + epsilon;

                            correctedMatrixes[0][as1][as2][i][row][col] = Math.log(h / (e + c)) + correctedValues[0][row][col];
                            correctedMatrixes[1][as1][as2][i][row][col] = Math.log(h / (e + c)) + correctedValues[1][row][col];
                            correctedMatrixes[2][as1][as2][i][row][col] = Math.log(h / (e + c)) + correctedValues[2][row][col];
                        }
                    }
                }
            }
        }

    }

    public static void printMatrixes() {
        System.out.println("--- GOR IV Matrix (6D) ---");
        for (int s = 0; s < 3; s++) {
            for (int as1 = 0; as1 < 20; as1++) {
                for (int as2 = 0; as2 < 20; as2++) {
                    for (int posK = 0; posK < 17; posK++) {
                        // prüfe ob dieser Block überhaupt Daten hat
                        if (matrixes[s][as1][as2][posK][0][0] == null) continue;

                        System.out.println("\nStruct[" + s + "] AS1[" + as1 + "] AS2[" + as2 + "] PosK[" + (posK - 8) + "]:");
                        for (int asRow = 0; asRow < 20; asRow++) {
                            for (int col = 0; col < 17; col++) {
                                System.out.print(matrixes[s][as1][as2][posK][asRow][col] + " ");
                            }
                            System.out.println();
                        }
                    }
                }
            }
        }

        System.out.println("\n--- GOR III Matrix (4D) ---");
        for (int as = 0; as < 20; as++) {
            for (int s = 0; s < 3; s++) {
                if (matrixes2[as][s][0][0] == null) continue;
                System.out.println("\nAS[" + as + "] Struct[" + s + "]:");
                for (int asRow = 0; asRow < 20; asRow++) {
                    for (int col = 0; col < WINDOW_SIZE; col++) {
                        System.out.print(matrixes2[as][s][asRow][col] + " ");
                    }
                    System.out.println();
                }
            }
        }
    }
    public static void main(String[] args) {
        File fasta = new File("C:\\1.Allgemein\\ProgrammierenIntelliJ\\propraGOR\\gor_examples\\1VZV\\1VZV.fasta~");
        File matrix = new File("C:\\1.Allgemein\\Pycharm\\propra2.07\\GOR\\gor_examples\\gor4_cb513_model.txt");

        Predict3 p = new Predict3(matrix, fasta);
        p.matrixReader();
        p.printMatrixes();

/*


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

        //Predict2 hmm = new  Predict2(model, fasta);
        //matrixReader();

        //ArrayList<ProteinData> out = predictionGor2FromFasta( showProbs);
        /*
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
        }*/

    }
}
