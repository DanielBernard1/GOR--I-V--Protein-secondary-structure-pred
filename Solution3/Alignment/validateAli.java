import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

public class validateAli {
    private static class Tuple{
        int val1;
        int val2;
        public Tuple(int val1, int val2) {
            this.val1 = val1;
            this.val2 = val2;
        }

        public int getVal1() {
            return val1;
        }

        public int getVal2() {
            return val2;
        }
        @Override
        public String toString(){
            return "(" + val1 + ", " + val2 + ")";
        }
        @Override
        public boolean equals(Object tuple){
            if (this == tuple) return true;
            if (!(tuple instanceof Tuple tuple1)) return false;
            return val1 == tuple1.getVal1() && val2 == tuple1.getVal2();
        }
        @Override
        public int hashCode() {
            return Objects.hash(val1, val2);
        }
    }
    public static void main(String[] args) throws IOException {
        if (Objects.equals(args[0], "-f")){
            String filepath = args[1];
            fileReader(filepath);
        }
        else {
            System.out.println("INVALID ARGUMENT(S)/SYNTAX");
        }

    }


    private static void fileReader(String filepath) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new FileReader(filepath));
        String line, header = "", seq1 = "", seq2 = "", seq3 = "", seq4;
        int counter = 0;
        while ((line = bufferedReader.readLine()) != null){
            line = line.trim();
            if (line.isEmpty()){continue;}
            if (line.startsWith(">")){
                header = line;
                counter = 0;
                continue;
            }
            if (counter == 0){
                seq1 = line;
            }
            else if (counter == 1){
                seq2 = line;
            }
            else if (counter == 2){
                seq3 = line;
            }
            else if (counter == 3){
                seq4 = line;
                double[] values = calculations(seq1.split("\\s+")[1], seq2.split("\\s+")[1], seq3.split("\\s+")[1], seq4.split("\\s+")[1]);
                System.out.println(header + " " +
                        String.format("%.4f", values[0]) + " " +
                        String.format("%.4f", values[1]) + " " +
                        String.format("%.4f", values[2]) + " " +
                        String.format("%.4f", values[3]) + " " +
                        String.format("%.4f", values[4]));

                System.out.println(seq1);
                System.out.println(seq2);
                System.out.println(seq3);
                System.out.println(seq4);
            }
            counter++;
        }
    }

    private static double[] calculations(String candidate1, String candidate2, String ref1, String ref2){
        double[] values = new double[5];
        Set<Tuple> candidate_set = new HashSet<>();
        Set<Tuple> reference_set = new HashSet<>();
        int templateCounter = -1;
        int targetCounter = -1;

        for (int col = 0; col < candidate1.length(); col++) {
            char i = candidate2.charAt(col);
            char j = candidate1.charAt(col);

            if (i != '-') templateCounter++;
            if (j != '-') targetCounter++;

            if (i != '-' && j != '-') {
                candidate_set.add(new Tuple(templateCounter, targetCounter));
            }
        }
        templateCounter = -1;
        targetCounter = -1;
        for (int col = 0; col < ref1.length(); col++) {
            char i = ref2.charAt(col);
            char j = ref1.charAt(col);

            if (i != '-') templateCounter++;
            if (j != '-') targetCounter++;

            if (i != '-' && j != '-') {
                reference_set.add(new Tuple(templateCounter, targetCounter));
            }
        }

        double counter = 0;
        double shift_index = 0;
        double inverse_shift_index = 0;
        double inverse_shift_counter = 0;
        double shift_counter = 0;
        Set<Integer> candidate_targets = new HashSet<>();
        for (Tuple a : candidate_set){
            if (reference_set.contains(a)){
                counter++;
            }

            for (Tuple b : reference_set){
                if (a.getVal1() == b.getVal1()){
                    shift_index += Math.abs(a.getVal2() - b.getVal2());

                    shift_counter++;
                }
                if (a.getVal2() == b.getVal2()){
                    inverse_shift_index += Math.abs(a.getVal1() - b.getVal1());
                    inverse_shift_counter++;
                }
            }
            candidate_targets.add(a.getVal1());
        }
        Set<Integer> ref_targets = new HashSet<>();
        for (Tuple a : reference_set){
            ref_targets.add(a.getVal1());
        }
        candidate_targets.retainAll(ref_targets);

        values[0] = counter / (double) reference_set.size();
        values[1] = counter / (double) candidate_set.size();
        values[2] = candidate_targets.size() / (double) candidate_set.size();
        values[3] = shift_index / shift_counter;
        values[4] = inverse_shift_index / inverse_shift_counter;

        return values;
    }
}
