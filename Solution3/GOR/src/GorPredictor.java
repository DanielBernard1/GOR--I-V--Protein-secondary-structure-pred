import java.io.File;
import java.util.HashMap;
import java.util.Scanner;

public abstract class GorPredictor {
    protected static final int WINDOW_SIZE = 17;
    protected static final int STEPS = 8;
    protected static final HashMap<Character, Integer> AS_TO_INDEX = new HashMap<>();
    static {
        char[] as_in_order = {
                'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
                'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y'
        };
        for (int i = 0; i < as_in_order.length; i++) {
            AS_TO_INDEX.put(as_in_order[i], i);
        }
    }
    protected static int getAsToIndex(Character A) {
        return AS_TO_INDEX.get(A);
    }
    protected static int indexforstruct(char structChar) {
        if (structChar =='H') return 0;
        if (structChar =='E') return 1;
        else return 2;
    }
    protected static double sum(Integer[][] matrix) {
        double total = 0;
        for (Integer[] row : matrix) {
            for (Integer val : row) {
                if (val != null) total += val;
            }
        }
        return total;
    }
    protected static double calculateWindow (Double[][] matrixHEC, String sequence) {
        Double[][] currentMatrix = matrixHEC;

        double score = 0;
        for (int i = 0; i < sequence.length(); i++) {
            char as = sequence.charAt(i);
            if(as=='_') continue;
            Integer asIndex= AS_TO_INDEX.get(as);
            if (asIndex == null){ continue;}

            score += currentMatrix[asIndex][i];



        }
        return score;
    }
    protected static HashMap<String, String> fastaReader (File file) {
        HashMap<String, String> fasta = new HashMap<>();
        String currentKey = null;
        StringBuilder seq = new StringBuilder();
        try (Scanner myReader = new Scanner(file)){
            while (myReader.hasNextLine()) {
                String line = myReader.nextLine();
                if (line.isEmpty()) continue;

                if (line.startsWith(">")) {
                    if (currentKey != null) {
                        fasta.put(currentKey, seq.toString());
                    }
                    currentKey = line;
                    seq = new StringBuilder();
                } else {
                    seq.append(line);
                }
            }
            if (currentKey != null) {
                fasta.put(currentKey, seq.toString());
            }
        }catch (Exception e) {
            System.err.println("An error occurred when reading the fasta file");
            e.printStackTrace();
        }
        return fasta;
    }
}
