class NMWDP extends Scoring{
    private int[][] scoring_matrix;
    private final String sequence_1;
    private final String sequence_2;
    public NMWDP(String sequence_1, String sequence_2){
        super(sequence_1, sequence_2);
        this.sequence_1 = sequence_1;
        this.sequence_2 = sequence_2;
    }

    public int calculate_alignment(){
        int alignment_score = 0;
        for (int i = 0; i < scoring_matrix.length; i++) {
            scoring_matrix[i][0] = i * gap_penalty;
        }
        for (int j = 0; j < scoring_matrix[0].length; j++) {
            scoring_matrix[0][j] = j * gap_penalty;
        }

        return alignment_score;
    }

}