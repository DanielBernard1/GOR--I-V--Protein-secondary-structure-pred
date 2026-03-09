public class SecondaryStructureMatrix {
    private int[][] levitt_matrix = new int[][]{
            //HEC
            {  200, -1500, -400},
            {-1500,   400, -400},
            { -400,  -400,  200},
    };
    private String levitt_format = "HEC";

    protected int[][] ss_matrix;
    protected String format;

    public SecondaryStructureMatrix() {
        this.ss_matrix = levitt_matrix;
        this.format = levitt_format;
    }
    public int getScore(char a, char b){
        return ss_matrix[format.indexOf(a)][format.indexOf(b)];
    }

}
