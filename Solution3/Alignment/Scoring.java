public class Scoring{
    protected final String seq1;
    protected final String seq2;
    protected static SubstitutionMatrix matrix;
    protected int gap;
    protected AlignmentType mode;

    public Scoring(String seq1, String seq2, SubstitutionMatrix matrix, int gap, AlignmentType mode){
        this.seq1 = seq1;
        this.seq2 = seq2;
        Scoring.matrix = matrix;
        this.gap = gap;
        this.mode = mode;
    }
    protected int diaScore (int i, int j){
        char x = seq1.charAt(i-1);
        char y = seq2.charAt(j-1);
        return matrix.getScore(x,y);
    }

    protected int gapScore(){
        return gap;
    }

    public int checkScore(String al1, String al2){
        int score = 0;
        for (int i=0; i<al1.length(); i++){
            char x = al1.charAt(i);
            char y = al2.charAt(i);
            if (x == '-'||y=='-'){
                score += gap;
            }else{
                score += matrix.getScore(x,y);
            }
        }
        return score;
    }

    public finalAlignment result() {
        return null;
    }

    public int Rec_score(){
        return new Recursion(seq1, seq2, matrix, gap, mode).score();
    }

    public int DP_score(){
        DynamicProgramming dynamicProgramming = new DynamicProgramming(seq1, seq2, matrix, gap, mode);
        if (mode.isGlobal()){
            return dynamicProgramming.NW_score();
        }
        if (mode.isLocal()){
            return dynamicProgramming.SW_score();
        }
        if (mode.isFreeshift()) {
            return dynamicProgramming.FS_score();
        }
        return Integer.MIN_VALUE;
    }
}
