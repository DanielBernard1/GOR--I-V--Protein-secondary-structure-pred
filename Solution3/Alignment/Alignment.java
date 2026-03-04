import java.io.BufferedReader;
import java.io.FileReader;
import java.util.HashMap;
import java.util.Map;

public class Alignment {
    //hier drüber wird alles abgerufen
    public static void main (String[] args) throws Exception {
        String pairsPath = null; // pro Zeile stehen 2 ids die miteinander Aligned werden sollen
        String seqlibPath = null;
        String matrixName = null;
        String modeStr = null;
        String formatStr = null;
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
            if(a.equals("--format")){formatStr = args[++i]; continue;}
        }

        AlignmentType mode = parseMode(modeStr);
        Map<String, String> seqlib = readSeqLib(seqlibPath);
        int gap = go; //--nw falls = true
        SubstitutionMatrix m1 = new SubstitutionMatrix(matrixName);

        readPairs(pairsPath, seqlib, mode, gap, m1);
    }

    private static void readPairs(String path, Map<String, String> seqlib, AlignmentType mode, int gap, SubstitutionMatrix matrix) throws Exception{
        BufferedReader br = new BufferedReader(new FileReader(path));
        String line;

        while ((line = br.readLine())!= null){
            line = line.trim();
            if(line.isEmpty()){continue;}
            String[] parts = line.split("\\s+"); //soll auf mehrere spaces, taps ud leerzeichen splitten
            String id1 = parts[0];
            String id2 = parts[1];
            String seq1 = seqlib.get(id1);
            String seq2 = seqlib.get(id2);

            Scoring s = new Scoring(seq1, seq2, matrix, gap, mode);
            finalAlignment result = s.result();
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
            return AlignmentType.Global;
        }
        if(s.equals("local")){
            return AlignmentType.Local;
        }
        return AlignmentType.Freeshift; //darf ich so

    }
}
