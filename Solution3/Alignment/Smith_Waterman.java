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

}
