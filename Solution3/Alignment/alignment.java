import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.HashMap;
import java.util.Map;

public class alignment {
    //hier drüber wird alles abgerufen
    public static void main (String[] args) throws Exception {
        String pairsPath = null; // pro Zeile stehen 2 ids die miteinander Aligned werden sollen
        String seqlibPath = null;
        String matrixName = null;
        String modeStr = null;
        String format = null;
        String dpDir = null;

        int go = -12; //default gap open
        int ge = -1; //default gap extend
        boolean useNW = false;//wenn true --> dp statt gotoh
        boolean check = false;

        for(int i=0; i < args.length; i++){
            String a = args[i];

            if(a.equals("--nw")){useNW = true; continue;}
            if(a.equals("--check")){check = true; continue;}
            if(a.equals("--go")){go = Integer.parseInt(args[++i]); continue;}
            if(a.equals("--ge")){ge = Integer.parseInt(args[++i]); continue;}
            if(a.equals("--dpmatrices")){dpDir = args[++i]; continue;}
            //mandatory
            if(a.equals("--pairs")){pairsPath = args[++i]; continue;}
            if(a.equals("--seqlib")){seqlibPath = args[++i]; continue;}
            if(a.equals("-m")){matrixName = args[++i]; continue;} //soll das wirklich nur mit einem Strich angegeben werden
            if(a.equals("--mode")){modeStr = args[++i]; continue;}
            if(a.equals("--format")){format = args[++i];}
        }

        //maybe in score schlauer
        go*=100;
        ge*=100;

        if (pairsPath == null || seqlibPath == null || matrixName == null
                || modeStr == null || format == null) {
            printHelp();
            return;
        }

        AlignmentType mode = parseMode(modeStr);
        if(mode == null) {
            printHelp();
            return;
        }
        Map<String, String> seqlib = readSeqLib(seqlibPath);
        SubstitutionMatrix m1 = new SubstitutionMatrix(matrixName);
        readPairs(go, ge, dpDir, check, pairsPath, seqlib, m1, mode, useNW, format);
    }
    private static void printHelp(){
        System.out.println("""
                Syntax:
                java -jar alignment.jar [--go <gapopen>] [--ge <gapextend>]
                [--dpmatrices <dir>] [--check]
                --pairs <pairfile> --seqlib <seqlibfile>
                -m <matrixname>
                --mode <local|global|freeshift> [--nw]
                --format <scores|ali|html>
                Options:
                --pairs <pairfile> path to pairs file
                --seqlib <seqlibfile> path to sequence library file
                -m <matrixname> path to substitution matrix file
                --go <gapopen> gap open penalty (default -12)
                --ge <gapextend> gap extend penalty (default -1)
                --mode <local|global|freeshift>
                --nw use NW/SW algorithms
                --format <scores|ali|html> output format
                scores: scores only
                ali: scores + alignment in plaintext
                html: scores + alignment in html
                --dpmatrices <directory> output dynamic programming matrices
                --check calculate checkscores for all alignments
                and output only incorrect alignments
                The Gotoh algorithm should be used as default, if --nw is not set. If called with no (or
                wrong) parameters, your command line tool must output this help text. The output must
                be written to stdout in all cases.""");
    }


    private static void readPairs(int go, int ge, String dpPath, boolean check, String pairsPath, Map<String, String> seqlib, SubstitutionMatrix matrix, AlignmentType mode, boolean useNW, String format) throws Exception{
        BufferedReader br = new BufferedReader(new FileReader(pairsPath));
        String line;

        while ((line = br.readLine())!= null){
            line = line.trim();
            if(line.isEmpty()){continue;}
            String[] parts = line.split("\\s+"); //soll auf mehrere spaces, taps ud leerzeichen splitten
            String id1 = parts[0];
            String id2 = parts[1];

            String seq1 = seqlib.get(id1);
            String seq2 = seqlib.get(id2);
            if(seq1 == null || seq2 == null ){continue;}

            Scoring scoring = new Scoring(seq1, seq2, matrix, go, ge, mode);

            finalAlignment res = scoring.result(useNW);

            double score = res.getScore();

            String[] alignments = new String[]{res.getAlign1(), res.getAlign2()};

            if(check){
                double cs = scoring.checkScore(res.getAlign1(), res.getAlign2());
                if(Math.abs(cs - res.getScore()) < 0.001){
                    continue;
                }
            }

            String scoreStr = String.format("%.4f", score);

            if (format.equals("scores")) {
                System.out.println(id1 + " " + id2 + " " + scoreStr);

            }
            else if (format.equals("ali")){
                System.out.println(">" + id1 + " " + id2 + " " +scoreStr);
                System.out.println(id1 + ": " + alignments[0]);
                System.out.println(id2 + ": " + alignments[1]);
            }
            else if (format.equals("html")){
                System.out.println(buildHtmlOutput(id1, id2, seq1, seq2, score, alignments[0], alignments[1], matrix));
            }
            else{
                printHelp();
                return;
            }
            if (dpPath != null){
                File file = new File(dpPath);
                if (file.isDirectory()){
                    file = new File(file, "scoring_matrix.txt");
                }
                int[][] scoring_matrix = scoring.getScoring_matrix();
                try (FileWriter fw = new FileWriter(file)) {
                    for (int i = 0; i < scoring_matrix.length; i++) {
                        for (int j = 0; j < scoring_matrix[0].length; j++) {
                            fw.write(scoring_matrix[i][j] + "\t");
                        }
                        fw.write("\n");
                    }
                }
            }
        }
        br.close();
    }


    private static String buildHtmlOutput(String id1, String id2, String seq1, String seq2, double score, String alignment1, String alignment2, SubstitutionMatrix matrix) {
        int matches = 0;
        int alignLen = alignment1.length();

        StringBuilder mid = new StringBuilder((alignLen));
        for(int i = 0; i < alignLen; i++){
            char c1 = alignment1.charAt(i);
            char c2 = alignment2.charAt(i);

            if(c1 == c2 && c1 != '-'){

                matches ++;
                mid.append('|');
            }else{
                if(c1 != '-' && c2 != '-'){
                    // Substitution (verschieden, keine gap)
                    int s = matrix.getScore(c1,c2);
                    mid.append(s>0? '+' : ' ');
                }else{
                    //Mindestens 1 Gap --> Leer
                    mid.append(' ');
                }
            }
        }
        int width = 100; //Zeilenumbruch der Sequenz nach 100er Basen
        StringBuilder out = new StringBuilder();
        out.append("<!doctype html>\n<html>" +
                "<head>" +
                "<meta charset=\"utf-8\"><title>").append(id1).append(" vs ").append(id2).append("</title></head><body>\n");
        out.append("<p><b>").append(id1).append("</b> vs <b>").append(id2).append("</b><br>\n")
                .append("score: ").append(score).append("<br>\n")
                .append("len1: ").append(seq1.length()).append(", len2: ").append(seq2.length()).append("<br>\n")
                .append("alignment length: ").append(alignLen).append("<br>\n")
                .append("#matches: ").append(matches).append("<br>\n").append("</p>");
        //.append("%identity: ").append(String.format("%.2f", identity)).append("<br>\n");

        out.append("<pre>\n");

        //müssen das ganze auch als Zeichenblöcke darstellne (BLAST stile)
        int pos1 = 0;
        int pos2 = 0;
        for (int i = 0; i < alignLen; i += width) {
            int jEnd = Math.min(alignLen, i + width);

            String s1 = alignment1.substring(i, jEnd);
            String sm = mid.substring(i, jEnd);
            String s2 = alignment2.substring(i, jEnd);

            for (int k = 0; k < s1.length(); k++) if (s1.charAt(k) != '-') pos1++;
            for (int k = 0; k < s2.length(); k++) if (s2.charAt(k) != '-') pos2++;

            //BLAST like
            out.append(id1).append(": ").append(s1).append(" ").append(pos1).append("\n");
            out.append("      ").append(sm).append("\n");
            out.append(id2).append(": ").append(s2).append(" ").append(pos2).append("\n\n");
        }

        out.append("</pre>\n</body></html>\n");
        return out.toString();
    }


    private static Map<String, String> readSeqLib(String path) throws Exception {
        Map<String, String> map = new HashMap<>();
        BufferedReader br = new BufferedReader(new FileReader(path));
        String line;
        while ((line = br.readLine())!=null){
            line = line.trim();
            if(line.isEmpty()){continue;}
            String[] parts = line.split(":", 2);
            map.put(parts[0], parts[1]);
        }
        br.close();
        return map;
    }

    private static AlignmentType parseMode(String s) {
        s = s.toLowerCase();
        if (s.equals("global")){
            return AlignmentType.global;
        }
        if(s.equals("local")){
            return AlignmentType.local;
        }
        if(s.equals("freeshift")){
            return AlignmentType.freeshift;

        }
        return null;
    }
}