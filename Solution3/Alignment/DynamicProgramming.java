import java.util.Arrays;

public class DynamicProgramming extends Scoring {
    private static int[][] scoring_matrix;
    public DynamicProgramming(String seq1, String seq2, SubstitutionMatrix matrix, int gap, AlignmentType mode) {
        super(seq1, seq2, matrix, gap, mode);
        scoring_matrix = new int[seq1.length() + 1][seq2.length() + 1];
    }
    public void calculate_alignment_matrix_NW() {
        for (int i = 0; i < scoring_matrix.length; i++) {
            scoring_matrix[i][0] = i * gap;
        }
        for (int j = 0; j < scoring_matrix[0].length; j++) {
            scoring_matrix[0][j] = j * gap;
        }
        for (int i = 1; i < scoring_matrix.length; i++) {
            for (int j = 1; j < scoring_matrix[0].length; j++) {

                int match = matrix.getScore(seq1.charAt(i - 1), seq2.charAt(j - 1));
                int delete = scoring_matrix[i - 1][j] + gap;
                int insert = scoring_matrix[i][j - 1] + gap;

                scoring_matrix[i][j] = Math.max(match, Math.max(delete, insert));
            }
        }
    }

    public int NW_score(){
        calculate_alignment_matrix_NW();
        return scoring_matrix[seq1.length()][seq2.length()];
    }

    public String[] NW_alignment(){
        calculate_alignment_matrix_NW();
        return null;
    }
    public void calculate_alignment_matrix_SW(){
        for (int i = 0; i < scoring_matrix.length; i++) {
            scoring_matrix[i][0] = 0;
        }
        Arrays.fill(scoring_matrix[0], 0);
        for (int i = 1; i < scoring_matrix.length; i++) {
            for (int j = 1; j < scoring_matrix[0].length; j++) {

                int match = matrix.getScore(seq1.charAt(i-1), seq2.charAt(j-1));
                int delete = scoring_matrix[i-1][j] + gap;
                int insert = scoring_matrix[i][j-1] + gap;

                scoring_matrix[i][j] = Math.max(match, Math.max(delete, Math.max(insert, 0)));
            }
        }
    }
    public int SW_score(){
        calculate_alignment_matrix_SW();
        int max = Integer.MIN_VALUE;
        for (int i = 0; i < scoring_matrix.length; i++) {
            for (int j = 0; j < scoring_matrix[0].length; j++) {
                if (scoring_matrix[i][j] > max){
                    max = scoring_matrix[i][j];
                }
            }
        }
        return max;
    }

    public String[] SW_alignment(){
        calculate_alignment_matrix_SW();
        return null;
    }

    public void calculate_alignment_matrix_FS(){
        for (int i = 0; i < scoring_matrix.length; i++) {
            scoring_matrix[i][0] = 0;
        }
        Arrays.fill(scoring_matrix[0], 0);

        for (int i = 1; i < scoring_matrix.length; i++) {
            for (int j = 1; j < scoring_matrix[0].length; j++) {

                int match = matrix.getScore(seq1.charAt(i-1), seq2.charAt(j-1));
                int delete = scoring_matrix[i-1][j] + gap;
                int insert = scoring_matrix[i][j-1] + gap;

                scoring_matrix[i][j] = Math.max(match, Math.max(delete, insert));
            }
        }
    }

    public int FS_score(){
        calculate_alignment_matrix_FS();
        int max = Integer.MIN_VALUE;
        for (int i = 0; i < scoring_matrix.length; i++) {
            if (scoring_matrix[i][scoring_matrix[0].length - 1] > max){
                max = scoring_matrix[i][scoring_matrix[0].length - 1];
            }
        }
        for (int i = 0; i < scoring_matrix[0].length; i++) {
            if (scoring_matrix[scoring_matrix.length - 1][i] > max) {
                max = scoring_matrix[scoring_matrix.length - 1][i];
            }
        }
        return max;
    }

    public String[] FS_alignment(){
        calculate_alignment_matrix_FS();
        return null;
    }

//
//
//
//
//
//    public int score(){
//        int [][]F = new int[seq1.length()+1][seq2.length()+1];
//
//        if (mode.isGlobal()){
//            for(int i = 1; i<seq1.length(); i++){
//                F[i][0] = F[i-1][0] + gapScore();
//            }
//            for(int j=1; j<seq2.length(); j++){
//                F[0][j] = F[0][j-1] + gapScore();
//            }
//        }
//
//        int bestLocal = Integer.MIN_VALUE;
//
//        for(int i=1; i<seq1.length(); i++){
//            for(int j=1; j<seq2.length(); j++){
//                int diag = F[i-1][j-1] + diaScore(i,j);
//                int up = F[i-1][j] + gapScore();
//                int left = F[i][j-1] + gapScore();
//
//                int Score1 = Math.max(diag, up);
//                int best =  Math.max(Score1, left);
//
//                if(mode.isLocal()){
//                    best = Math.max(0, best);
//                    bestLocal = Math.max(bestLocal,best);
//                }
//                F[i][j] = best;
//            }
//        }
//
//        if(mode.isLocal()){
//            return bestLocal;
//        }
//
//        if(mode.isFreeshift()){
//
//        }
//        return F[seq1.length()][seq2.length()];
//    }
}
