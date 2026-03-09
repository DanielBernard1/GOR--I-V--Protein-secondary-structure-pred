import java.io.IOException;

public class runner {
    public static void main(String[] args) throws IOException {
        SubstitutionMatrix substitutionMatrix = new SubstitutionMatrix("/Users/davidhuynhngoc/Downloads/dayhoff-2.mat");
        DynamicProgramming gotoh = new DynamicProgramming("SIVTKSIVNADAEARYLSPGELDRIKSFVTSGERRVRIAETMTGARERIIKQAGDQLFGKRPDVVSPGGNAYGADMTATCLRDLDYYLRLITYGIVAGDVTPIEEIGVVGVREMYKSLGTPIEAIAEGVRAMKSVATSLLSGADAAEAGSYFDYLIGAM", "MQDPYVKEAENLKKYFNAGHSDVADNGTLFLGILKNWKEESDRKIMQSQIVSFYFKLFKNFKDDQSIQKSVETIKEDMNVKFFNSNKKKRDDFEKLTNYSVTDLNVQRKAIDELIQVMAEL", substitutionMatrix, -200, AlignmentType.global);
        System.out.println(gotoh.NW_score() / 100.0);
        System.out.println(gotoh.NW_alignment()[0]);
        System.out.println(gotoh.NW_alignment()[1]);
        System.out.println(gotoh.traceback_indexes);

//        StringBuilder scoreMatrix = new StringBuilder();
//        scoreMatrix.append("Score Matrix: \n");
//        for (int[] row : dynamicProgramming.scoring_matrix) {
//            for (int value : row) {
//                scoreMatrix.append((value/100.0) + " ");
//            }
//            scoreMatrix.append("\n");
//        }
//        scoreMatrix.append("\n");
//        System.out.println(scoreMatrix.toString());
    }
}
