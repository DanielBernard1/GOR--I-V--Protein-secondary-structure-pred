public class Gotoh extends Scoring{
    private static double[][] M, Ix, Iy;
    private static final double NEG_INF = Double.NEGATIVE_INFINITY;
    public Gotoh(String sequence_1, String sequence_2, SubstitutionMatrix submatrix, int gap, AlignmentType mode){
        super(sequence_1, sequence_2, submatrix, gap, mode);
    }

    public static double free_shift(String seq1, String seq2, int gapOpen, int gapExtend) {
        int n = seq1.length();
        int m = seq2.length();

        M  = new double[n + 1][m + 1];
        Ix = new double[n + 1][m + 1];
        Iy = new double[n + 1][m + 1];

        for (int i = 0; i <= n; i++) {
            M[i][0]  = 0;
            Ix[i][0] = NEG_INF;
            Iy[i][0] = NEG_INF;
        }

        for (int j = 0; j <= m; j++) {
            M[0][j]  = 0;
            Ix[0][j] = NEG_INF;
            Iy[0][j] = NEG_INF;
        }
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {

                int score = matrix.getScore(seq1.charAt(i), seq2.charAt(j));

                M[i][j] = Math.max(Math.max(M[i - 1][j - 1], Ix[i - 1][j - 1]), Iy[i - 1][j - 1]) + score;

                Ix[i][j] = Math.max(M[i - 1][j] - gapOpen, Ix[i - 1][j] - gapExtend);

                Iy[i][j] = Math.max(M[i][j - 1] - gapOpen, Iy[i][j - 1] - gapExtend);
            }
        }
        double maxScore = NEG_INF;
        for (int j = 0; j <= m; j++) {
            maxScore = Math.max(maxScore, M[n][j]);
        }
        for (int i = 0; i <= n; i++) {
            maxScore = Math.max(maxScore, M[i][m]);
        }

        return maxScore;
    }


}
