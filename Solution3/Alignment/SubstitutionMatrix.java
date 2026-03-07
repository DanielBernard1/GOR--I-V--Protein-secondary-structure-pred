import java.io.*;
import java.util.*;
public class SubstitutionMatrix {
    private String index = "ARNDCQEGHILKMFPSTWYV";
    private int[][] submatrix = new int[20][20];

    public SubstitutionMatrix(String filepath) throws IOException{
        generate_matrix(filepath);
    }

    private void generate_matrix(String filepath) throws IOException {
        List<int[]> rows = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(filepath))) {
            String line;
            while ((line = br.readLine()) != null) {

                if (line.startsWith("MATRIX")) {
                    String[] parts = line.trim().split("\\s+");

                    int[] rowValues = new int[parts.length - 1];
                    for (int i = 1; i < parts.length; i++) {
                        String val = parts[i].replaceAll("\\.$", "");
                        rowValues[i - 1] = (int)(Math.round(Double.parseDouble(val) * 100.0)) ;
                    }
                    rows.add(rowValues);
                }
                else if (line.startsWith("ROWINDEX")){
                    index = line.split("\\s+")[1];
                }
            }
        }
        for (int i = 0; i < rows.size(); i++) {
            int[] row = rows.get(i);
            for (int j = 0; j < row.length; j++) {
                submatrix[i][j] = row[j];
                submatrix[j][i] = row[j];
            }
        }
    }
    public int getScore(char a, char b){
        return submatrix[index.indexOf(a)][index.indexOf(b)];
    }

}
