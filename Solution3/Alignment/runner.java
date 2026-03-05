import java.io.IOException;

public class runner {
    public static void main(String[] args) throws IOException {
        SubstitutionMatrix substitutionMatrix = new SubstitutionMatrix("/Users/davidhuynhngoc/Downloads/dayhoff-2.mat");
        DynamicProgramming dynamicProgramming = new DynamicProgramming("GPLDVQVTEDAVRRYLTRKPMTTKDLLKKFQTKKTGLSSEQTVNVLAQILKRLNPERKMINDKMHFSLK", "MEEAKQKVVDFLNSKSKSKFYFNDFTDLFPDMKQREVKKILTALVNDEVLEYWSSGSTTMYGLKG", substitutionMatrix, -200, AlignmentType.freeshift);

        System.out.println(dynamicProgramming.FS_score() / 100.0);
        System.out.println(dynamicProgramming.FS_alignment()[0]);
        System.out.println(dynamicProgramming.FS_alignment()[1]);

        StringBuilder scoreMatrix = new StringBuilder();
        scoreMatrix.append("Score Matrix: \n");
        for (int[] row : dynamicProgramming.scoring_matrix) {
            for (int value : row) {
                scoreMatrix.append((value/100.0) + " ");
            }
            scoreMatrix.append("\n");
        }
        scoreMatrix.append("\n");
        //System.out.println(scoreMatrix.toString());
    }
}
