import java.io.BufferedReader;
import java.io.FileReader;
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

        int go = -12; //gap open
        int ge = -1; //gap extend
        boolean useNW = false;
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

        if (pairsPath == null || seqlibPath == null || matrixName == null
                || modeStr == null || format == null) {
            printHelp();
            return;
        }

        AlignmentType mode = parseMode(modeStr);
        Map<String, String> seqlib = readSeqLib(seqlibPath);
        SubstitutionMatrix m1 = new SubstitutionMatrix(matrixName);
        readPairs(go, ge, dpDir, check, pairsPath, seqlib, m1, mode, useNW, format);
    }
    private static void printHelp(){
        System.out.println("The output must be written to stdout in all cases");
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

            Scoring scoring = new Scoring(seq1, seq2, matrix, go, ge, mode);

            if (format.equals("scores")) {
                System.out.print(id1 + "\t" + id2 + "\t");
                if (useNW){
                    System.out.println(scoring.DP_score());
                }
                else{
                    System.out.println(scoring.Gotoh_score());
                }
            }
            else if (format.equals("ali")){
                String[] alignments;
                System.out.print(">" + id1 + "\t" + id2 + "\t");

                if (useNW){
                    System.out.println(scoring.DP_score());
                    alignments = scoring.DP_alignment();
                }
                else{
                    System.out.println(scoring.Gotoh_score());
                    alignments = scoring.Gotoh_alignment();
                }

                System.out.println(id1 + "\t" + alignments[0]);
                System.out.println(id2 + "\t" + alignments[1]);
            }
            else if (format.equals("html")){
                //TODO
            }
            if (check){
                //TODO
            }
            if (dpPath != null){

            }
            finalAlignment result = scoring.result();
        }
        br.close();
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
        return AlignmentType.freeshift; //darf ich so
    }
}
