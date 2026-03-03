public class Scoring {
    protected final String seq1;
    protected final String seq2;
    protected SubstitutionMatrix matrix;
    protected int gap;
    protected AlignmentType mode;

    public Scoring(String seq1, String seq2, SubstitutionMatrix matrix, int gap, AlignmentType mode){
        this.seq1 = seq1;
        this.seq2 = seq2;
        this.matrix = matrix;
        this.gap = gap;
        this.mode = mode;
    }

    public finalAlignment result() {
    }
}
