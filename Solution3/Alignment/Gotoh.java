public class Gotoh extends Scoring {
    private int[][] M, Ix, Iy;
    private final int NEG_INF = -100000000;
    private final int gapOpen, gapExtend;

    public Gotoh(String sequence_1, String sequence_2, SubstitutionMatrix submatrix, int gap, AlignmentType mode, int gapOpen, int gapExtend) {
        super(sequence_1, sequence_2, submatrix, gap, mode);
        this.gapOpen = gapOpen;
        this.gapExtend = gapExtend;
    }

    public void FS_Matrices() {
        int n = seq1.length();
        int m = seq2.length();

        M  = new int[n + 1][m + 1];
        Ix = new int[n + 1][m + 1];
        Iy = new int[n + 1][m + 1];

        M[0][0]  = 0;
        Ix[0][0] = NEG_INF;
        Iy[0][0] = NEG_INF;

        for (int i = 1; i <= n; i++) {
            M[i][0]  = NEG_INF;
            Ix[i][0] = 0;
            Iy[i][0] = NEG_INF;
        }

        for (int i = 1; i <= m; i++) {
            M[0][i]  = NEG_INF;
            Ix[0][i] = NEG_INF;
            Iy[0][i] = 0;
        }

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {

                int score = substitution_matrix.getScore(seq1.charAt(i - 1), seq2.charAt(j - 1));

                M[i][j]  = Math.max(Math.max(M[i-1][j-1], Ix[i-1][j-1]), Iy[i-1][j-1]) + score;
                Ix[i][j] = Math.max(M[i-1][j] - gapOpen, Ix[i-1][j] - gapExtend);
                Iy[i][j] = Math.max(M[i][j-1] - gapOpen, Iy[i][j-1] - gapExtend);
            }
        }
    }

    public double FS_score() {
        FS_Matrices();
        int n = seq1.length();
        int m = seq2.length();
        int max = NEG_INF;

        for (int j = 0; j <= m; j++) {
            max = Math.max(max, Math.max(M[n][j], Math.max(Ix[n][j], Iy[n][j])));
        }

        for (int i = 0; i <= n; i++) {
            max = Math.max(max, Math.max(M[i][m], Math.max(Ix[i][m], Iy[i][m])));
        }

        return max;
    }
}