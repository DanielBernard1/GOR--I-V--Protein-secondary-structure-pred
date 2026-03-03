import java.util.Arrays;

public class Smith_Waterman extends Scoring{
    private final int[][] scoring_matrix;
    public Smith_Waterman(String sequence_1, String sequence_2, SubstitutionMatrix submatrix, int gap, AlignmentType mode){
        super(sequence_1, sequence_2, submatrix, gap, mode);
        scoring_matrix = new int[sequence_1.length() + 1][sequence_2.length() + 1];
    }

    public int[][] calculate_alignment_matrix(){
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
        return scoring_matrix;
    }
}
