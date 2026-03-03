import java.lang.Math;
class NMWDP extends Scoring{

    private final int[][] scoring_matrix;
    private boolean subMatrix;
    public NMWDP(String sequence_1, String sequence_2, boolean subMatrix){
        super(sequence_1, sequence_2, subMatrix);
        scoring_matrix = new int[sequence_1.length() + 1][sequence_2.length() + 1];
    }

    public int[][] calculate_alignment(){
        int alignment_score = 0;
        for (int i = 0; i < scoring_matrix.length; i++) {
            scoring_matrix[i][0] = i * gap_penalty;
        }
        for (int j = 0; j < scoring_matrix[0].length; j++) {
            scoring_matrix[0][j] = j * gap_penalty;
        }
        for (int i = 1; i < scoring_matrix.length; i++) {
            for (int j = 1; j < scoring_matrix[0].length; j++) {
                int match;
                if (subMatrix){
                    match = substitutionMatrix.getScore(sequence_1.charAt(i-1), sequence_2.charAt(j-1));
                }
                else{
                    match = scoring_matrix[i-1][j-1] + (sequence_1.charAt(i-1) == sequence_2.charAt(j-1) ? match_score : mismatch_penalty);
                }
                int delete = scoring_matrix[i-1][j] + gap_penalty;
                int insert = scoring_matrix[i][j-1] + gap_penalty;
                scoring_matrix[i][j] = Math.max(match, Math.max(delete, insert));
            }
        }
        return scoring_matrix;
    }
}