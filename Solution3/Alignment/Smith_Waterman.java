import java.util.Arrays;

public class Smith_Waterman extends Scoring{
    private final int[][] scoring_matrix;

    public Smith_Waterman(String sequence_1, String sequence_2, int match_score, int mismatch_penalty, int gap_penalty) {
        super(sequence_1, sequence_2, match_score, mismatch_penalty, gap_penalty);
        scoring_matrix = new int[sequence_1.length() + 1][sequence_2.length() + 1];
        submatrix = false;
    }

    public Smith_Waterman(String sequence_1, String sequence_2, int gap_score, boolean submatrix) {
        super(sequence_1, sequence_2, gap_score, submatrix);
        scoring_matrix = new int[sequence_1.length() + 1][sequence_2.length() + 1];
    }

    public Smith_Waterman(String sequence_1, String sequence_2, boolean submatrix){
        super(sequence_1, sequence_2, submatrix);
        scoring_matrix = new int[sequence_1.length() + 1][sequence_2.length() + 1];
    }

    public int[][] calculate_alignment_matrix(){
        for (int i = 0; i < scoring_matrix.length; i++) {
            scoring_matrix[i][0] = 0;
        }
        Arrays.fill(scoring_matrix[0], 0);
        for (int i = 1; i < scoring_matrix.length; i++) {
            for (int j = 1; j < scoring_matrix[0].length; j++) {
                int match;
                if (submatrix){
                    match = substitutionMatrix.getScore(sequence_1.charAt(i-1), sequence_2.charAt(j-1));
                }
                else{
                    match = scoring_matrix[i-1][j-1] + (sequence_1.charAt(i-1) == sequence_2.charAt(j-1) ? match_score : mismatch_penalty);
                }
                int delete = scoring_matrix[i-1][j] + gap_penalty;
                int insert = scoring_matrix[i][j-1] + gap_penalty;
                scoring_matrix[i][j] = Math.max(match, Math.max(delete, Math.max(insert, 0)));
            }
        }
        return scoring_matrix;
    }
}
