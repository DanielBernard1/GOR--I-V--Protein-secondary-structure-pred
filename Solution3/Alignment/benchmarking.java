import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

//muss eigtl aus git bash machen aber kb, ich hasse git
//habe gegoogelt und gefunden dass man es mit Subtraktion von System.nanoTime() machen kann

//Ausgabe csv Datei die das Ergebnis von Benchmark ausgibt
//Das ganze soll dann in Python aufgenommen werden, wo man dann mit matplot den Plot erstellt
public class benchmarking {
    static final int anz_align = 10000;

    static final int[] laengen = {5, 8, 10};

    static final char[] as = "ARNDCQEGHILKMFPSTWYV".toCharArray(); //alle Aminosäuren

    public static void main(String[] args) throws IOException {
        SubstitutionMatrix matrix = new SubstitutionMatrix(args[0]);

        int ge = -2 * 100;

        Random random = new Random(30);//beliebige Zahl --> ausprobieren was gut ist
        //csv-Datei
        FileWriter csv = new FileWriter("res_benchmark.csv");
        csv.write("laenge,dp_time,rec_time\n");

        for (int len : laengen){

            String[] s1 = new String[anz_align];
            String[] s2 = new String[anz_align];

            for(int e = 0; e<anz_align; e++){
                s1[e] = randomSeq(len, random);
                s2[e] = randomSeq(len, random);
            }
            long t0 = System.nanoTime();
            for(int t = 0; t < anz_align; t++){
                new DynamicProgramming(s1[t], s2[t], matrix, ge, AlignmentType.global).NW_score();
            }
            double dp = (System.nanoTime() - t0)/1000.0/anz_align;

            long t1 = System.nanoTime();
            for(int t = 0; t<100; t++){
                new Recursion(s1[t], s2[t], matrix, ge, AlignmentType.global).score();
            }
            double rec = (System.nanoTime() - t1)/1000.0/100;

            csv.write(String.format("%d,%.4f,%.4f%n",(len),dp,rec));//reddit

        }
        csv.close();
    }

    private static String randomSeq(int len, Random random) {
        StringBuilder sb = new StringBuilder(len);
        for (int i=0; i<len; i++){
            sb.append(as[random.nextInt(as.length)]);
        }
        return sb.toString();
    }
}
