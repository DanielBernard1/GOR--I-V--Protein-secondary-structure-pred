import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
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
        boolean useNW = false; //--nw
        boolean check = false;

        for(int i=0; i < args.length; i++){
            String a = args[i];
            if(a.equals("--nw")){useNW = true; continue;}
            if(a.equals("--check")){check = true; continue;}
            if(a.equals("--go")){go = Integer.parseInt(args[i+1]); continue;}
            if(a.equals("--ge")){ge = Integer.parseInt(args[i+1]); continue;}
            if(a.equals("--dpmatrices")){modeStr = args[i+1]; continue;}
            //mandatory
            if(a.equals("--pairs")){pairsPath = args[i+1]; continue;}
            if(a.equals("--seqlibs")){seqlibPath = args[i+1]; continue;}
            if(a.equals("-m")){matrixName = args[i+1]; continue;} //soll das wirklich nur mit einem Strich angegeben werden
            if(a.equals("--mode")){modeStr = args[i+1]; continue;}
            if(a.equals("--format")){formatStr = args[i+1]; continue;}
        }

        AlignmentType mode = parseMode(modeStr);

        Map<String, String> seqlib = readSeqLib(seqlibPath);
        List<String[]> pairs = readPairs(pairsPath);
        //String seq1 = seqlib.get();
    }

    private static List<String[]> readPairs(String path) throws Exception{
        List<String[]> list = new ArrayList<>();
        BufferedReader br = new BufferedReader(new FileReader(path));
        String line;
        while ((line = br.readLine())!= null){
            line = line.trim();
            if(line.isEmpty()){continue;}
            String[] parts = line.split("\t"); //woran soll ich splitten?
            list.add(new String[]{parts[0], parts[1]});
        }
        br.close();
        return list;
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
