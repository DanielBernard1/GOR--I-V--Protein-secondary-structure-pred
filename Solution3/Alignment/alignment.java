import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

//Autor Laura Martin
public class alignment {
    //hier drüber wird alles abgerufen
    public static void main (String[] args) throws Exception {
        String pairsPath = null; // pro Zeile stehen 2 ids die miteinander Aligned werden sollen
        String seqlibPath = null;
        String matrixName = null;
        String modeStr = null;
        boolean secStruct = false;

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
            if(a.equals("--ss")){secStruct = true; continue;}
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

        SubstitutionMatrix m1 = new SubstitutionMatrix(matrixName);

        if (secStruct){
            SecondaryStructureMatrix secondaryStructureMatrix = new SecondaryStructureMatrix();
            Map<String, List<String>> SecStructLib = readStructLib(seqlibPath);
            readPairsSecStruct(go, ge, dpDir, check, pairsPath, SecStructLib, m1, secondaryStructureMatrix, mode, useNW, format);
        }
        else {
            Map<String, String> seqlib = readSeqLib(seqlibPath);
            readPairs(go, ge, dpDir, check, pairsPath, seqlib, m1, mode, useNW, format);
        }
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
                """);
    }
    private static Map<String, List<String>> readStructLib(String filepath) throws IOException {
        Map<String, List<String>> map = new HashMap<>();
        BufferedReader br = new BufferedReader(new FileReader(filepath));
        String line, header = null, aseq = null, sseq = null;
        int counter = 0;
        while ((line = br.readLine())!=null){
            line = line.trim();
            if (line.startsWith(">")){
                header = line;
                counter = 1;
            }
            else if (line.startsWith("AS")){
                aseq = line.substring(3);
                counter = 2;
            }
            else if (line.startsWith("SS")){
                sseq = line.substring(3);
                counter = 3;
            }
            if (counter == 3){
                List<String> list = new ArrayList<>();
                list.add(aseq);
                list.add(sseq);
                map.put(header, list);
            }
        }
        br.close();
        return map;
    }
    private static void readPairsSecStruct(int go, int ge, String dpPath, boolean check, String pairsPath, Map<String, List<String>> seqlib, SubstitutionMatrix matrix, SecondaryStructureMatrix secondaryStructureMatrix, AlignmentType mode, boolean useNW, String format) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader(pairsPath));
        String line;

        while ((line = br.readLine())!= null){
            line = line.trim();
            if(line.isEmpty()){continue;}
            String[] parts = line.split("\\s+"); //soll auf mehrere spaces, taps ud leerzeichen splitten
            String id1 = parts[0];
            String id2 = parts[1];

            String aseq1 = seqlib.get(id1).get(0);
            String sseq1 = seqlib.get(id1).get(1);
            String aseq2 = seqlib.get(id2).get(0);
            String sseq2 = seqlib.get(id2).get(1);

            if(aseq1 == null || aseq2 == null || sseq1 == null || sseq2 == null ){continue;}

            Scoring scoring = new Scoring(aseq1, aseq2, sseq1, sseq2, matrix, secondaryStructureMatrix, go, ge, mode);

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
                System.out.println(buildHtmlOutput(id1, id2, aseq1, aseq2, score, alignments[0], alignments[1], matrix));
            }
            else{
                printHelp();
                return;
            }
            if (dpPath != null && format.equals("html")){
                File file = new File(dpPath);
                File fpFile = new File(new File(dpPath), "fixedpoint_" + id1 + "_" + id2 + ".txt");

                FixedPoint fp = new FixedPoint(aseq1, aseq2, matrix, ge);
                fp.fixedPointScores(fpFile.getPath());
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
                try (FileWriter fw = new FileWriter("traceback_index.txt")) {
                    List<String> indexes = scoring.getTracebackIndexes();
                    for (String a : indexes){
                        fw.write(a + "\n");
                    }
                }
            }
        }
        br.close();
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
            if (dpPath != null && format.equals("html")){
                File file = new File(dpPath);
                File fpFile = new File(new File(dpPath), "fixedpoint_" + id1 + "_" + id2 + ".txt");

                FixedPoint fp = new FixedPoint(seq1, seq2, matrix, ge);
                fp.fixedPointScores(fpFile.getPath());
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
                try (FileWriter fw = new FileWriter("traceback_index.txt")) {
                    List<String> indexes = scoring.getTracebackIndexes();
                    for (String a : indexes){
                        fw.write(a + "\n");
                    }
                }
            }
        }
        br.close();
    }


    private static String buildHtmlOutput(String id1, String id2, String seq1, String seq2, double score, String alignment1, String alignment2, SubstitutionMatrix matrix) {
        int matches = 0;
        int alignLen = alignment1.length();

        StringBuilder mid = new StringBuilder(alignLen);
        for (int i = 0; i < alignLen; i++) {
            char c1 = alignment1.charAt(i);
            char c2 = alignment2.charAt(i);
            if (c1 == c2 && c1 != '-') {
                matches++;
                mid.append('|');
            } else if (c1 != '-' && c2 != '-') {
                int s = matrix.getScore(c1, c2);
                mid.append(s > 0 ? '+' : ' ');
            } else {
                mid.append(' ');
            }
        }

        int width = 100;
        String pad = " ".repeat(id1.length() + 2); // dynamisch, passt sich an ID-Länge an

        StringBuilder out = new StringBuilder();
        out.append("<!doctype html>\n<html>\n<head>\n")
                .append("<meta charset=\"utf-8\">")
                .append("<title>").append(id1).append(" vs ").append(id2).append("</title>")
                .append("<style>")
                .append("pre { font-family: 'Courier New', monospace; font-size: 20px; line-height: 1.6; white-space: pre; overflow-x: auto; }")
                .append("body { max-width: 1200px; margin: auto; padding: 20px; background: #f0f6fc; border-left: 4px solid #2c5f8a; }")
                .append("</style>")
                .append("\n</head>\n<body>\n");

        out.append("<p><b>").append(id1).append("</b> vs <b>").append(id2).append("</b><br>\n")
                .append("score: ").append(score).append("<br>\n")
                .append("len1: ").append(seq1.length()).append(", len2: ").append(seq2.length()).append("<br>\n")
                .append("alignment length: ").append(alignLen).append("<br>\n")
                .append("#matches: ").append(matches).append("<br>\n</p>");

        out.append("<pre>\n");

        int pos1 = 0;
        int pos2 = 0;
        for (int i = 0; i < alignLen; i += width) {
            int jEnd = Math.min(alignLen, i + width);

            String s1  = alignment1.substring(i, jEnd);
            String sm  = mid.substring(i, jEnd);       // <-- sm wird hier definiert
            String s2  = alignment2.substring(i, jEnd);

            for (int k = 0; k < s1.length(); k++) if (s1.charAt(k) != '-') pos1++;
            for (int k = 0; k < s2.length(); k++) if (s2.charAt(k) != '-') pos2++;

            // coloredMid hier im Loop bauen, weil sm hier verfügbar ist
            StringBuilder coloredMid = new StringBuilder();
            for (char c : sm.toCharArray()) {
                if      (c == '|') coloredMid.append("<span style='color:#2a9d2a'>|</span>");
                else if (c == '+') coloredMid.append("<span style='color:#e08000'>+</span>");
                else               coloredMid.append(c);
            }

            out.append(id1).append(": ").append(s1).append(" ").append(pos1).append("\n");
            out.append(pad).append(coloredMid).append("\n");
            out.append(id2).append(": ").append(s2).append(" ").append(pos2).append("\n\n");
        }

        out.append("</pre>\n</body>\n</html>\n");
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
            map.put(parts[0].trim().replace(">", ""), parts[1].trim());

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

