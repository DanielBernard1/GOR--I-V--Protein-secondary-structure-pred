public class GotohLa extends Scoring{

    private final int go;
    private final int ge;
    private final int min_unendlich = -10000000;

    public GotohLa(String seq1, String seq2, SubstitutionMatrix matrix, int go, int ge, AlignmentType mode) {
        super(seq1, seq2, matrix, 0, mode);
        this.go = go;
        this.ge = ge;
    }

    public int scoreGlobal(){
        //brauchen 3 Matrizen
        //1tens Alignment endet mit Match/Mismatch --> diag
        int[][] M = new int[seq1.length()+1][seq2.length()+1];
        //2ten endet mit Gap in Seq1 --> up
        int[][] Gx = new int[seq1.length()+1][seq2.length()+1];
        //3tens endet mit Gap in Seq2 --> left
        int[][] Gy = new int[seq1.length()+1][seq2.length()+1];

        M[0][0] = 0;
        Gx[0][0] = min_unendlich;
        Gy[0][0] = min_unendlich;

        //gap in Seq1, nach links
        for(int j=1; j<=seq2.length(); j++){
            M[0][j] = min_unendlich;
            Gx[0][j] = min_unendlich;
            Gy[0][j] = go + j*ge;
        }
        //gap in Seq2, nach oben
        for(int i=1; i<=seq1.length(); i++){
            M[i][0] = min_unendlich;
            Gx[i][0] = go + i*ge;
            Gy[i][0] = min_unendlich;
        }
        //noch mit einbeziehung Match/Mismatch --> Matrix M
        for(int i =1; i<= seq1.length(); i++){
            for(int j = 1; j<= seq2.length(); j++){
                int bestGxy = Math.max(Gx[i-1][j-1],Gy[i-1][j-1]);
                int best = Math.max(M[i-1][j-1], bestGxy);
                M[i][j] = best + diaScore(i,j);
                //Gap in seq2 (up)
                int gxOpen = M[i-1][j] + go +ge;
                int gxExtend = Gx[i-1][j] + ge;
                Gx[i][j] = Math.max(gxOpen, gxExtend);
                //Gap in seq1 (left)
                int gyOpen = M[i][j-1] + go + ge;
                int gyExtend = Gy[i][j-1] +ge;
                Gy[i][j] = Math.max(gyOpen, gyExtend);
            }
        }
        int maxGxGy = Math.max(Gx[seq1.length()][seq2.length()], Gy[seq1.length()][seq2.length()]);
        return Math.max(M[seq1.length()][seq2.length()], maxGxGy);
    }
}
