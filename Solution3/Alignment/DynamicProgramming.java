import java.util.Arrays;

public class DynamicProgramming extends Scoring {
    private int[][] scoring_matrix;

    public DynamicProgramming(String seq1, String seq2, SubstitutionMatrix matrix, int gap, AlignmentType mode) {
        super(seq1, seq2, matrix, gap, 0,  mode);
        scoring_matrix = new int[seq1.length() + 1][seq2.length() + 1];
    }

    public void calculate_alignment_matrix_NW() {
        for (int i = 0; i < scoring_matrix.length; i++) {
            scoring_matrix[i][0] = i * gap;
        }
        for (int j = 0; j < scoring_matrix[0].length; j++) {
            scoring_matrix[0][j] = j * gap;
        }
        for (int i = 1; i < scoring_matrix.length; i++) {
            for (int j = 1; j < scoring_matrix[0].length; j++) {

                int match = scoring_matrix[i - 1][j - 1] + substitution_matrix.getScore(seq1.charAt(i - 1), seq2.charAt(j - 1));
                int delete = scoring_matrix[i - 1][j] + gap;
                int insert = scoring_matrix[i][j - 1] + gap;

                scoring_matrix[i][j] = Math.max(match, Math.max(delete, insert));
            }
        }
    }

    public int NW_score() {
        calculate_alignment_matrix_NW();
        return scoring_matrix[seq1.length()][seq2.length()];
    }

    public String[] NW_alignment() {
        calculate_alignment_matrix_NW();
        StringBuilder ali1 = new StringBuilder();
        StringBuilder ali2 = new StringBuilder();
        int i = seq1.length();
        int j = seq2.length();
        while (i > 0 && j > 0) {
            int current = scoring_matrix[i][j];
            int diag = scoring_matrix[i - 1][j - 1];
            int up = scoring_matrix[i - 1][j];
            int left = scoring_matrix[i][j - 1];

            if (current == diag + substitution_matrix.getScore(seq1.charAt(i - 1), seq2.charAt(j - 1))){
                ali1.insert(0, seq1.charAt(i - 1));
                ali2.insert(0, seq2.charAt(j - 1));
                i--; j--;
            }
            else if (current == up + gap){
                ali1.insert(0, seq1.charAt(i - 1));
                ali2.insert(0, "-");
                i--;
            }
            else if (current == left + gap){
                ali1.insert(0, "-");
                ali2.insert(0, seq2.charAt(j - 1));
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

    public void calculate_alignment_matrix_SW() {
        for (int i = 0; i < scoring_matrix.length; i++) {
            scoring_matrix[i][0] = 0;
        }
        Arrays.fill(scoring_matrix[0], 0);
        for (int i = 1; i < scoring_matrix.length; i++) {
            for (int j = 1; j < scoring_matrix[0].length; j++) {

                int match = scoring_matrix[i - 1][j - 1] + substitution_matrix.getScore(seq1.charAt(i - 1), seq2.charAt(j - 1));
                int delete = scoring_matrix[i - 1][j] + gap;
                int insert = scoring_matrix[i][j - 1] + gap;

                scoring_matrix[i][j] = Math.max(match, Math.max(delete, Math.max(insert, 0)));
            }
        }
    }
    private int[] find_max_coords(){
        calculate_alignment_matrix_SW();
        int[] coords = new int[2];
        int max = Integer.MIN_VALUE;
        for (int i = 0; i < scoring_matrix.length; i++) {
            for (int j = 0; j < scoring_matrix[0].length; j++) {
                if (scoring_matrix[i][j] > max) {
                    max = scoring_matrix[i][j];
                    coords[0] = i;
                    coords[1] = j;
                }
            }
        }
        return coords;
    }

    public int SW_score() {
        int[] coords = find_max_coords();
        return scoring_matrix[coords[0]][coords[1]];
    }

    public String[] SW_alignment() {
        int[] coords = find_max_coords();
        StringBuilder ali1 = new StringBuilder();
        StringBuilder ali2 = new StringBuilder();
        int i = coords[0];
        int j = coords[1];
        while (i > 0 && j > 0 && scoring_matrix[i][j] > 0) {
            int current = scoring_matrix[i][j];
            int diag = scoring_matrix[i - 1][j - 1];
            int up = scoring_matrix[i - 1][j];
            int left = scoring_matrix[i][j - 1];

            if (current == diag + substitution_matrix.getScore(seq1.charAt(i - 1), seq2.charAt(j - 1))){
                ali1.insert(0, seq1.charAt(i - 1));
                ali2.insert(0, seq2.charAt(j - 1));
                i--; j--;
            }
            else if (current == up + gap){
                ali1.insert(0, seq1.charAt(i - 1));
                ali2.insert(0, "-");
                i--;
            }
            else if (current == left + gap){
                ali1.insert(0, "-");
                ali2.insert(0, seq2.charAt(j - 1));
                j--;
            }
        }
        return new String[]{ali1.toString(), ali2.toString()};
    }

    public void calculate_alignment_matrix_FS() {
        for (int i = 0; i < scoring_matrix.length; i++) {
            scoring_matrix[i][0] = 0;
        }
        Arrays.fill(scoring_matrix[0], 0);

        for (int i = 1; i < scoring_matrix.length; i++) {
            for (int j = 1; j < scoring_matrix[0].length; j++) {

                int match = scoring_matrix[i - 1][j - 1] + substitution_matrix.getScore(seq1.charAt(i - 1), seq2.charAt(j - 1));
                int delete = scoring_matrix[i - 1][j] + gap;
                int insert = scoring_matrix[i][j - 1] + gap;

                scoring_matrix[i][j] = Math.max(match, Math.max(delete, insert));
            }
        }
    }

    private int[] fs_coords(){
        int[] coords = new int[2];
        calculate_alignment_matrix_FS();
        int max = Integer.MIN_VALUE;
        for (int i = 0; i < scoring_matrix.length; i++) {
            if (scoring_matrix[i][scoring_matrix[0].length - 1] > max) {
                max = scoring_matrix[i][scoring_matrix[0].length - 1];
                coords[0] = i;
                coords[1] = scoring_matrix[0].length - 1;
            }
        }
        for (int i = 0; i < scoring_matrix[0].length; i++) {
            if (scoring_matrix[scoring_matrix.length - 1][i] > max) {
                max = scoring_matrix[scoring_matrix.length - 1][i];
                coords[0] = scoring_matrix.length - 1;
                coords[1] = i;
            }
        }
        return coords;
    }

    public int FS_score() {
        int[] coords = fs_coords();
        return scoring_matrix[coords[0]][coords[1]];
    }

    public String[] FS_alignment() {
        StringBuilder ali1 = new StringBuilder();
        StringBuilder ali2 = new StringBuilder();
        int[] coords = fs_coords();
        int i = coords[0];
        int j = coords[1];

        int lastRow = scoring_matrix.length - 1;
        int lastCol = scoring_matrix[0].length - 1;

        for (int k = lastRow; k > i; k--) {
            ali1.insert(0, seq1.charAt(k - 1));
            ali2.insert(0, "-");
        }
        for (int k = lastCol; k > j; k--) {
            ali1.insert(0, "-"); //hier stand davor Stringbuilder
            ali2.insert(0, seq2.charAt(k - 1));
        }
        while (i > 0 && j > 0) {
            int current = scoring_matrix[i][j];
            int diag = scoring_matrix[i - 1][j - 1];
            int up = scoring_matrix[i - 1][j];
            int left = scoring_matrix[i][j - 1];

            if (current == diag + substitution_matrix.getScore(seq1.charAt(i - 1), seq2.charAt(j - 1))){
                ali1.insert(0, seq1.charAt(i - 1));
                ali2.insert(0, seq2.charAt(j - 1));
                i--; j--;
            }
            else if (current == up + gap){
                ali1.insert(0, seq1.charAt(i - 1));
                ali2.insert(0, "-");
                i--;
            }
            else if (current == left + gap){
                ali1.insert(0, "-");
                ali2.insert(0, seq2.charAt(j - 1));
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