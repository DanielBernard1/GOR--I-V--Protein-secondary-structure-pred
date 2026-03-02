public class Scoring {
    private final String sequence_1;
    private final String sequence_2;
    protected int match_score;
    protected int mismatch_penalty;
    protected int gap_penalty;
    public Scoring(String sequence_1, String sequence_2, int match_score, int mismatch_penalty, int gap_penalty){
        this.sequence_1 = sequence_1;
        this.sequence_2 = sequence_2;
        this.match_score = match_score;
        this.mismatch_penalty = mismatch_penalty;
        this.gap_penalty = gap_penalty;

    }
    public Scoring(String sequence_1, String sequence_2, int gap_score){
        this.sequence_1 = sequence_1;
        this.sequence_2 = sequence_2;
        this.match_score = 1;
        this.mismatch_penalty = -1;
        this.gap_penalty = gap_score;
    }
    public Scoring(String sequence_1, String sequence_2){
        this.sequence_1 = sequence_1;
        this.sequence_2 = sequence_2;
        this.match_score = 1;
        this.mismatch_penalty = -1;
        this.gap_penalty = -2;
    }
}
