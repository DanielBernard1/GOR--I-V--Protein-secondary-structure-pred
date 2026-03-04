public class Gotoh extends Scoring{
    private enum State{M, Gx, Gy} //traceback
    private int[][] M, Gx, Gy;

    private final int go;
    private final int ge;
    private final int min_inf = -10000000;

    //Pointer für Traceback
    private State[][] prevM;
    private State[][] prevGx;
    private State[][] prevGy;

    public Gotoh(String seq1, String seq2, SubstitutionMatrix matrix, int go, int ge, AlignmentType mode) {
        super(seq1, seq2, matrix, go, ge, mode);
        this.go = go;
        this.ge = ge;
    }

    //GLOBAL Gotoh
    public int Global_score(){
        //brauchen 3 Matrizen
        //1tens Alignment endet mit Match/Mismatch --> diag
        int[][] M = new int[seq1.length()+1][seq2.length()+1];
        prevM = new State[seq1.length()+1][seq2.length()+1];//pointer
        //2ten endet mit Gap in Seq1 --> up
        int[][] Gx = new int[seq1.length()+1][seq2.length()+1];
        prevGx = new State[seq1.length()+1][seq2.length()+1];//pointer
        //3tens endet mit Gap in Seq2 --> left
        int[][] Gy = new int[seq1.length()+1][seq2.length()+1];
        prevGy = new State[seq1.length()+1][seq2.length()+1];//pointer

        M[0][0] = 0;
        Gx[0][0] = min_inf;
        Gy[0][0] = min_inf;
        prevM[0][0] = State.M;

        //gap in Seq1, nach links
        for(int j=1; j<=seq2.length(); j++){
            M[0][j] = min_inf;
            Gx[0][j] = min_inf;
            Gy[0][j] = go + j*ge;

            prevGy[0][j] = State.Gy;
        }
        //gap in Seq2, nach oben
        for(int i=1; i<=seq1.length(); i++){
            M[i][0] = min_inf;
            Gx[i][0] = go + i*ge;
            Gy[i][0] = min_inf;

            prevGx[i][0] = State.Gx;
        }
        //noch mit einbeziehung Match/Mismatch --> Matrix M
        for(int i =1; i<= seq1.length(); i++){
            for(int j = 1; j<= seq2.length(); j++){

                //int bestGxy = Math.max(Gx[i-1][j-1],Gy[i-1][j-1]);
                //int best = Math.max(M[i-1][j-1], bestGxy);
                //M[i][j] = best + diaScore(i,j);

                //Start Traceback pointer
                int fromM = M[i-1][j-1];
                int fromGx = Gx[i-1][j-1];
                int fromGy = Gy[i-1][j-1];

                int bestPrev = fromM;
                State preState = State.M;

                if(fromGx > bestPrev){
                    bestPrev = fromGx;
                    preState = State.Gx;
                }
                if(fromGy > bestPrev){
                    bestPrev = fromGy;
                    preState = State.Gy;
                }

                M[i][j] = bestPrev + diaScore(i,j);
                prevM[i][j] = preState;
                //Ende Tracebackpointer

                //Gap in seq2 (up)
                int gxOpen = M[i-1][j] + go +ge;
                int gxExtend = Gx[i-1][j] + ge;
                //Gx[i][j] = Math.max(gxOpen, gxExtend);

                //Pointer Gx
                if(gxOpen >= gxExtend){
                    Gx[i][j] = gxOpen;
                    prevGx[i][j] = State.M;
                }else{
                    Gx[i][j] = gxExtend;
                    prevGx[i][j] = State.Gx;
                }

                //Gap in seq1 (left)
                int gyOpen = M[i][j-1] + go + ge;
                int gyExtend = Gy[i][j-1] +ge;
                //Gy[i][j] = Math.max(gyOpen, gyExtend);

                //Pointer Gy
                if(gyOpen >= gyExtend){
                    Gy[i][j] = gyOpen;
                    prevGy[i][j] = State.M;
                }else{
                    Gy[i][j] = gyExtend;
                    prevGy[i][j] = State.Gy;
                }
            }
        }
        this.M = M;
        this.Gx = Gx;
        this.Gy = Gy;

        int maxGxGy = Math.max(Gx[seq1.length()][seq2.length()], Gy[seq1.length()][seq2.length()]);
        return Math.max(M[seq1.length()][seq2.length()], maxGxGy);
    }

    //In welcher Matrix starten wir:
    public String[] Global_alignment(){
        Global_score();
        //Matrix mit bestem Endwert?
        State state = State.M;
        int best = M[seq1.length()][seq2.length()];

        if(Gx[seq1.length()][seq2.length()]> best){
            best = Gx[seq1.length()][seq2.length()];
            state = State.Gx;
        }
        if(Gy[seq1.length()][seq2.length()] > best){
            best = Gy[seq1.length()][seq2.length()];
            state = State.Gy;
        }
        return Global_alignment(seq1.length(), seq2.length(), state);
    }

    //Traceback Global -->  bauen die alignments von hinten auf
    public String[] Global_alignment(int i, int j, State state){
        StringBuilder align1 = new StringBuilder();
        StringBuilder align2 = new StringBuilder();

        while(i>0 || j>0){
            if(state == State.M){
                align1.append(seq1.charAt(i-1));
                align2.append(seq2.charAt(j-1));
                state = prevM[i][j];
                i= i-1;
                j= j-1;
            }
            else{
                if (state == State.Gx){
                    align1.append(seq1.charAt(i-1));
                    align2.append("-");
                    state = prevGx[i][j];
                    i = i-1;
                }else{
                    align1.append("-");
                    align2.append(seq2.charAt(j-1));
                    state = prevGy[i][j];
                    j = j-1;
                }
            }
        }
        String[] alignment = new String[2];
        String al1 = align1.reverse().toString();
        String al2 = align2.reverse().toString();

        alignment[0] = al1;
        alignment[1] = al2;

        return alignment;
    }


    //LOCAL Gotoh
    public int Local_score(){
        //brauchen 3 Matrizen
        //1tens Alignment endet mit Match/Mismatch --> diag
        int[][] M = new int[seq1.length()+1][seq2.length()+1];
        //2ten endet mit Gap in Seq1 --> up
        int[][] Gx = new int[seq1.length()+1][seq2.length()+1];
        //3tens endet mit Gap in Seq2 --> left
        int[][] Gy = new int[seq1.length()+1][seq2.length()+1];

        //erste Zeile auf 0 initialisieren
        for(int i=0; i<= seq1.length(); i++){
            M[i][0] = 0;
            Gx[i][0] = 0;
            Gy[i][0] = 0;
        }
        //erste Spalte auf 0 intialisieren
        for(int j=0; j <= seq2.length(); j++){
            M[0][j] = 0;
            Gx[0][j] = 0;
            Gy[0][j] = 0;
        }

        int bestLocal = 0;

        for(int i=1; i <= seq1.length(); i++){
            for(int j=1; j<= seq2.length(); j++){
                int bestGxGy = Math.max(Gx[i-1][j-1], Gy[i-1][j-1]);
                int best = Math.max(M[i-1][j-1], bestGxGy);
                int maxVal = best + diaScore(i,j);

                int gxOpen = M[i-1][j] + go +ge;
                int gxExtend = Gx[i-1][j] + ge;
                int maxGapX = Math.max(gxOpen, gxExtend);

                int gyOpen = M[i][j-1] +go +ge;
                int gyExtend = Gy[i][j-1] + ge;
                int maxGapY = Math.max(gyOpen, gyExtend);

                //Darf nicht unter 0
                maxVal = Math.max(0, maxVal);
                maxGapX = Math.max(0, maxGapX);
                maxGapY = Math.max(0, maxGapY);

                //Matrizen füllen
                M[i][j] = maxVal;
                Gx[i][j] = maxGapX;
                Gy[i][j] = maxGapY;

                //was ist das beste
                int maxGxGy = Math.max(maxGapX, maxGapY);
                int einzelBest = Math.max(maxVal, maxGxGy);

                if(einzelBest > bestLocal){
                    bestLocal = einzelBest;
                }
            }
        }
        return bestLocal;
    }

    private void FS_Matrices() {
        int n = seq1.length();
        int m = seq2.length();

        M  = new int[n + 1][m + 1];
        Gx = new int[n + 1][m + 1];
        Gy = new int[n + 1][m + 1];

        M[0][0]  = 0;
        Gx[0][0] = min_inf;
        Gy[0][0] = min_inf;

        for (int i = 1; i <= n; i++) {
            M[i][0]  = min_inf;
            Gx[i][0] = 0;
            Gy[i][0] = min_inf;
        }

        for (int i = 1; i <= m; i++) {
            M[0][i]  = min_inf;
            Gx[0][i] = min_inf;
            Gy[0][i] = 0;
        }

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {

                int score = substitution_matrix.getScore(seq1.charAt(i - 1), seq2.charAt(j - 1));

                M[i][j]  = Math.max(Math.max(M[i-1][j-1], Gx[i-1][j-1]), Gy[i-1][j-1]) + score;
                Gx[i][j] = Math.max(M[i-1][j] - go, Gx[i-1][j] - ge);
                Gy[i][j] = Math.max(M[i][j-1] - go, Gy[i][j-1] - ge);
            }
        }
    }

    public int FS_score() {
        FS_Matrices();
        int n = seq1.length();
        int m = seq2.length();
        int max = min_inf;

        for (int j = 0; j <= m; j++) {
            max = Math.max(max, Math.max(M[n][j], Math.max(Gx[n][j], Gy[n][j])));
        }
        for (int i = 0; i <= n; i++) {
            max = Math.max(max, Math.max(M[i][m], Math.max(Gx[i][m], Gy[i][m])));
        }
        return max;
    }
    public String[] FS_alignment() {
        FS_Matrices();
        int n = seq1.length();
        int m = seq2.length();
        int max = min_inf;
        int startI = n;
        int startJ = m;
        String startMatrix = "M";

        for (int i = 0; i <= m; i++) {
            if (M[n][i] > max)  {
                max = M[n][i];
                startI = n;
                startJ = i;
                startMatrix = "M";
            }
            if (Gx[n][i] > max) {
                max = Gx[n][i];
                startI = n;
                startJ = i;
                startMatrix = "Gx";
            }
            if (Gy[n][i] > max) {
                max = Gy[n][i];
                startI = n;
                startJ = i;
                startMatrix = "Gy";
            }
        }
        for (int i = 0; i <= n; i++) {
            if (M[i][m] > max)  {
                max = M[i][m];
                startI = i;
                startJ = m;
                startMatrix = "M";
            }
            if (Gx[i][m] > max) { max = Gx[i][m]; startI = i; startJ = m; startMatrix = "Gx"; }
            if (Gy[i][m] > max) { max = Gy[i][m]; startI = i; startJ = m; startMatrix = "Gy"; }
        }

        StringBuilder ali1 = new StringBuilder();
        StringBuilder ali2 = new StringBuilder();

        for (int k = n; k > startI; k--) {
            ali1.insert(0, seq1.charAt(k - 1));
            ali2.insert(0, "-");
        }
        for (int k = m; k > startJ; k--) {
            ali1.insert(0, "-");
            ali2.insert(0, seq2.charAt(k - 1));
        }

        int i = startI;
        int j = startJ;
        String current = startMatrix;

        while (i > 0 && j > 0) {
            if (current.equals("M")) {
                int score = substitution_matrix.getScore(seq1.charAt(i - 1), seq2.charAt(j - 1));
                ali1.insert(0, seq1.charAt(i - 1));
                ali2.insert(0, seq2.charAt(j - 1));
                if      (M[i-1][j-1]  + score == M[i][j]) current = "M";
                else if (Gx[i-1][j-1] + score == M[i][j]) current = "Gx";
                else                                        current = "Gy";
                i--; j--;

            } else if (current.equals("Ix")) {
                ali1.insert(0, seq1.charAt(i - 1));
                ali2.insert(0, "-");
                if (M[i-1][j] - go == Gx[i][j]) current = "M";
                else                              current = "Gx";
                i--;

            } else { // Iy
                ali1.insert(0, "-");
                ali2.insert(0, seq2.charAt(j - 1));
                if (M[i][j-1] - go == Gy[i][j]) current = "M";
                else                              current = "Gy";
                j--;
            }
        }
        while (i > 0) {
            ali1.insert(0, seq1.charAt(i - 1));
            ali2.insert(0, "-");
            i--;
        }
        while (j > 0) {
            ali1.insert(0, "-");
            ali2.insert(0, seq2.charAt(j - 1));
            j--;
        }

        return new String[]{ali1.toString(), ali2.toString()};
    }
}
