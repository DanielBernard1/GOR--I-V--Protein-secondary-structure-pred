import java.util.Arrays;

//Autor: David

public class DynamicProgramming extends Scoring {
    protected int[][] scoring_matrix;
    private char[][] traceback_matrix;

    public DynamicProgramming(String seq1, String seq2, SubstitutionMatrix matrix, int gap, AlignmentType mode) {
        super(seq1, seq2, matrix, 0, gap,  mode);
        scoring_matrix = new int[seq1.length() + 1][seq2.length() + 1];
        traceback_matrix = new char[seq1.length() + 1][seq2.length() + 1];
    }

    public int[][] getScoring_matrix() {
        if (mode.isGlobal()){
            calculate_alignment_matrix_NW();
        }
        if (mode.isLocal()){
            calculate_alignment_matrix_SW();
        }
        if (mode.isFreeshift()){
            calculate_alignment_matrix_FS();
        }
        return scoring_matrix;
    }

    public void calculate_alignment_matrix_NW() {
        for (int i = 0; i < scoring_matrix.length; i++) {
            scoring_matrix[i][0] = i * gap;
            traceback_matrix[i][0] = 'U';
        }
        for (int j = 0; j < scoring_matrix[0].length; j++) {
            scoring_matrix[0][j] = j * gap;
            traceback_matrix[0][j] = 'L';
        }
        traceback_matrix[0][0] = '0';
        for (int i = 1; i < scoring_matrix.length; i++) {
            for (int j = 1; j < scoring_matrix[0].length; j++) {

                int match = scoring_matrix[i - 1][j - 1] + substitution_matrix.getScore(seq1.charAt(i - 1), seq2.charAt(j - 1));
                int delete = scoring_matrix[i - 1][j] + gap;
                int insert = scoring_matrix[i][j - 1] + gap;

                int best = Math.max(match, Math.max(delete, insert));
                if (best == match){
                    traceback_matrix[i][j] = 'D';
                }
                else if (best == delete){
                    traceback_matrix[i][j] = 'U';
                }
                else {
                    traceback_matrix[i][j] = 'L';
                }
                scoring_matrix[i][j] = best;
            }
        }
    }

    public int NW_score() {
        calculate_alignment_matrix_NW();
        return scoring_matrix[seq1.length()][seq2.length()];
    }

    public void calculate_alignment_matrix_SW() {
        for (int i = 0; i < scoring_matrix.length; i++) {
            scoring_matrix[i][0] = 0;
            traceback_matrix[i][0] = '0';
        }
        Arrays.fill(scoring_matrix[0], 0);
        Arrays.fill(traceback_matrix[0], '0');

        for (int i = 1; i < scoring_matrix.length; i++) {
            for (int j = 1; j < scoring_matrix[0].length; j++) {

                int match = scoring_matrix[i - 1][j - 1] + substitution_matrix.getScore(seq1.charAt(i - 1), seq2.charAt(j - 1));
                int delete = scoring_matrix[i - 1][j] + gap;
                int insert = scoring_matrix[i][j - 1] + gap;

                int best = Math.max(0, Math.max(match, Math.max(delete, insert)));
                if (best == 0){
                    traceback_matrix[i][j] = '0';
                }
                else if (best == match){
                    traceback_matrix[i][j] = 'D';
                }
                else if (best == delete){
                    traceback_matrix[i][j] = 'U';
                }
                else {
                    traceback_matrix[i][j] = 'L';
                }
                scoring_matrix[i][j] = best;
            }
        }
    }
    private int[] SW_coords(){
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
        int[] coords = SW_coords();
        return scoring_matrix[coords[0]][coords[1]];
    }

    public void calculate_alignment_matrix_FS() {
        for (int i = 0; i < scoring_matrix.length; i++) {
            scoring_matrix[i][0] = 0;
            traceback_matrix[i][0] = 'U';
        }
        Arrays.fill(scoring_matrix[0], 0);
        Arrays.fill(traceback_matrix[0], 'L');
        traceback_matrix[0][0] = '0';

        for (int i = 1; i < scoring_matrix.length; i++) {
            for (int j = 1; j < scoring_matrix[0].length; j++) {

                int match = scoring_matrix[i - 1][j - 1] + substitution_matrix.getScore(seq1.charAt(i - 1), seq2.charAt(j - 1));
                int delete = scoring_matrix[i - 1][j] + gap;
                int insert = scoring_matrix[i][j - 1] + gap;

                int best = Math.max(match, Math.max(delete, insert));
                if (best == match){
                    traceback_matrix[i][j] = 'D';
                }
                else if (best == delete){
                    traceback_matrix[i][j] = 'U';
                }
                else {
                    traceback_matrix[i][j] = 'L';
                }
                scoring_matrix[i][j] = best;
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
    public String[] NW_alignment(){
        calculate_alignment_matrix_NW();
        return traceback(seq1.length(), seq2.length(), new StringBuilder(), new StringBuilder(), mode);
    }

    public String[] SW_alignment(){
        int[] coords = SW_coords();
        String[] aligned = traceback(coords[0], coords[1], new StringBuilder(), new StringBuilder(), mode);

        StringBuilder tail1 = new StringBuilder();
        StringBuilder tail2 = new StringBuilder();

        for (int k = coords[0]; k < seq1.length(); k++) tail1.append(seq1.charAt(k));
        for (int k = coords[1]; k < seq2.length(); k++) tail2.append(seq2.charAt(k));
        while (tail1.length() < tail2.length()) tail1.append('-');
        while (tail2.length() < tail1.length()) tail2.append('-');

        if (tail1.toString().endsWith("-")){
            char[] array = tail1.toString().toCharArray();
            for (char a : array){
                if (a != '-'){
                    tail2.insert(0, '-');
                    tail1.append('-');
                }
            }
        }
        else{
            char[] array = tail2.toString().toCharArray();
            for (char a : array){
                if (a != '-'){
                    tail1.insert(0, '-');
                    tail2.append('-');
                }
            }
        }
        return new String[]{aligned[0] + tail1, aligned[1] + tail2};
    }
    public String[] FS_alignment(){
        int[] coords = fs_coords();
        String[] aligned = traceback(coords[0], coords[1], new StringBuilder(), new StringBuilder(), mode);

        StringBuilder tail1 = new StringBuilder();
        StringBuilder tail2 = new StringBuilder();
        for (int k = coords[0]; k < seq1.length(); k++) tail1.append(seq1.charAt(k));
        for (int k = coords[1]; k < seq2.length(); k++) tail2.append(seq2.charAt(k));
        while (tail1.length() < tail2.length()) tail1.append('-');
        while (tail2.length() < tail1.length()) tail2.append('-');

        return new String[]{aligned[0] + tail1, aligned[1] + tail2};
    }


    private String[] traceback(int i, int j, StringBuilder ali1, StringBuilder ali2, AlignmentType mode) {
        if (mode == AlignmentType.global && i == 0 && j == 0) {
            return new String[]{ali1.toString(), ali2.toString()};
        }
        if (mode == AlignmentType.local && traceback_matrix[i][j] == '0') {
            while (i > 0) {
                ali1.insert(0, seq1.charAt(i - 1));
                ali2.insert(0, '-');
                i--;
            }
            while (j > 0) {
                ali1.insert(0, '-');
                ali2.insert(0, seq2.charAt(j - 1));
                j--;
            }
            return new String[]{ali1.toString(), ali2.toString()};
        }
        if (mode == AlignmentType.freeshift && (i == 0 || j == 0)) {
            while (i > 0) {
                ali1.insert(0, seq1.charAt(i - 1));
                ali2.insert(0, '-');
                i--;
            }
            while (j > 0) {
                ali1.insert(0, '-');
                ali2.insert(0, seq2.charAt(j - 1));
                j--;
            }
            return new String[]{ali1.toString(), ali2.toString()};
        }
        char dir = traceback_matrix[i][j];
        if (dir == 'D') {
            return traceback(i-1, j-1, new StringBuilder(String.valueOf(seq1.charAt(i-1))).append(ali1), new StringBuilder(String.valueOf(seq2.charAt(j-1))).append(ali2), mode);
        } else if (dir == 'U') {
            return traceback(i-1, j, new StringBuilder(String.valueOf(seq1.charAt(i-1))).append(ali1), new StringBuilder("-").append(ali2), mode);
        } else if (dir == 'L') {
            return traceback(i, j-1, new StringBuilder("-").append(ali1), new StringBuilder(String.valueOf(seq2.charAt(j-1))).append(ali2), mode);
        }

        return new String[]{ali1.toString(), ali2.toString()};
    }
}