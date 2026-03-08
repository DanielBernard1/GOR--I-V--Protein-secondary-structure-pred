//Autor: Laura Martin

public class Recursion extends Scoring{
    public Recursion(String seq1, String seq2, SubstitutionMatrix substitution_matrix, int gap, AlignmentType mode){
        super(seq1, seq2, substitution_matrix, gap, 0, mode);
    }
    public int scoreRec(){
        return f(seq1.length(), seq2.length());
    }

    private int f(int i, int j){
        if (i==0 && j ==0){
            return 0;
        }
        if(i==0){
            return f(0, j-1) + gap;
        }
        if(j==0){
            return f(i-1, 0) + gap;
        }

        int diag = f(i-1,j-1) + diaScore(i,j);
        int up = f(i-1, j) + gap;
        int left = f(i, j-1) + gap;

        int Score1 = Math.max(diag, up);
        return Math.max(Score1, left);
    }

    public int score(){
        return f(seq1.length(), seq2.length());
    }
}
