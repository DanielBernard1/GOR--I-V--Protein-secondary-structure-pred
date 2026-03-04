public class DynamicProgramming extends Scoring {

    public DynamicProgramming(String seq1, String seq2, SubstitutionMatrix matrix, int gap, AlignmentType mode) {
        super(seq1, seq2, matrix, gap, mode);
    }

    public int score(){
        int [][]F = new int[seq1.length()+1][seq2.length()+1];

        if (mode.isGlobal()){
            for(int i = 1; i<seq1.length(); i++){
                F[i][0] = F[i-1][0] + gapScore();
            }
            for(int j=1; j<seq2.length(); j++){
                F[0][j] = F[0][j-1] + gapScore();
            }
        }

        int bestLocal = Integer.MIN_VALUE;

        for(int i=1; i<seq1.length(); i++){
            for(int j=1; j<seq2.length(); j++){
                int diag = F[i-1][j-1] + diaScore(i,j);
                int up = F[i-1][j] + gapScore();
                int left = F[i][j-1] + gapScore();

                int Score1 = Math.max(diag, up);
                int best =  Math.max(Score1, left);

                if(mode.isLocal()){
                    best = Math.max(0, best);
                    bestLocal = Math.max(bestLocal,best);
                }
                F[i][j] = best;
            }
        }

        if(mode.isLocal()){
            return bestLocal;
        }

        if(mode.isFreeshift()){

        }
        return F[seq1.length()][seq2.length()];
    }
}
