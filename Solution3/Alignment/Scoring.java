public class Scoring{
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
    private String[] backtrack_NW(int[][] scoring_matrix){
        String ali_1 = "";
        String ali_2 = "";

        return new String[]{ali_1, ali_2};
    }

    public int scoreRec(){
        return new Recursion(seq1, seq2, matrix, gap, mode).score();
    }

    public int scoreDp(){
        return new DynamicProgramming(seq1, seq2, matrix, gap, mode).score();
    }

    public int scoreDP(){
        int[][] F = new int[seq1.length()+1][seq2.length()+1];
        int bestLocal = 0;
        if(mode.isLocal()){
            return bestLocal;
        }

        if(mode.isFreeshift()) {
            int best = Integer.MIN_VALUE;
            for(int i = 0; i <= seq1.length(); i++){
                best = Math.max(best, F[i][seq2.length()]);
            }
            for(int j = 0; j <= seq2.length(); j++){
                best = Math.max(best, F[seq1.length()][j]);
            }
        }

        //global
        return F[seq1.length()][seq2.length()];
    }
}
