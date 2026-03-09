//Autor Laura Martin

import java.io.FileWriter;
import java.io.IOException;

public class FixedPoint {
    //fixed point für (i,j) Paare
    //aus Vorlesung: Score(i,j) = forward[i-1][j-1] + S(si, ti) + backward[n-i][m-j]


    protected String seq1;
    protected String seq2;
    protected SubstitutionMatrix matrix;
    protected int gap;

    public FixedPoint(String seq1, String seq2, SubstitutionMatrix matrix, int gap){
        this.seq1 = seq1;
        this.seq2 =  seq2;
        this.matrix = matrix;
        this.gap = gap;
    }

    //Forward-Matrix
    public int[][] forwardMatrix(){
        int [][] forward = new int[seq1.length()+1][seq2.length()+1];
        for(int i = 0; i<= seq1.length(); i++){
            forward[i][0] = i* gap;
        }
        for(int j=0; j<seq2.length(); j++){
            forward[0][j] = j*gap;
        }
        for (int i = 1; i <= seq1.length(); i++) {
            for (int j = 1; j <= seq2.length(); j++) {
                int match  = forward[i-1][j-1] + matrix.getScore(seq1.charAt(i-1), seq2.charAt(j-1));
                int delete = forward[i-1][j]   + gap;
                int insert = forward[i][j-1]   + gap;
                forward[i][j] = Math.max(match, Math.max(delete, insert));
            }
        }

        return forward;
    }

    //Backward-Matrix
    public int[][] backwardMatrix(){
        String reverse1 = new StringBuilder(seq1).reverse().toString();
        String reverse2 = new StringBuilder(seq2).reverse().toString();

        int [][] backward = new int[seq1.length()+1][seq2.length()+1];

        for(int i = 0; i<= seq1.length(); i++){
            backward[i][0] = i* gap;
        }
        for(int j=0; j<seq2.length(); j++){
            backward[0][j] = j*gap;
        }
        for (int i = 1; i <= seq1.length(); i++) {
            for (int j = 1; j <= seq2.length(); j++) {
                int match  = backward[i-1][j-1] + matrix.getScore(reverse1.charAt(i-1), reverse2.charAt(j-1));
                int delete = backward[i-1][j]   + gap;
                int insert = backward[i][j-1]   + gap;
                backward[i][j] = Math.max(match, Math.max(delete, insert));
            }
        }

        return backward;
    }

    //suchen den score alles fixedpoint (i,j)
    public void fixedPointScores(String filepath) throws IOException {
        int[][] backward = backwardMatrix();
        int[][] forward = forwardMatrix();

        int [][] ScoreFP = new int[seq1.length()][seq2.length()];
        int min = Integer.MAX_VALUE;
        int max = Integer.MAX_VALUE;

        for(int i =0; i < seq1.length(); i++){
            for(int j=0; j<seq2.length(); j++){
                //Formel von oben
                int score = forward[i][j] + matrix.getScore(seq1.charAt(i), seq2.charAt(j)) + backward[seq1.length()-i-1][seq2.length()-j-1];
                ScoreFP[i][j] = score;
                if(score < min){
                    min = score;
                }
                if(score > max){
                    max = score;
                }
            }
        }

        FileWriter fw = new FileWriter(filepath);
        fw.write(min + "\t" +max + "\n");
        for(int i=0; i<seq1.length(); i++){
            for(int j=0; j<seq2.length(); j++){
                fw.write(ScoreFP[i][j] + "\t");
            }
            fw.write("\n");
        }
    }
}
