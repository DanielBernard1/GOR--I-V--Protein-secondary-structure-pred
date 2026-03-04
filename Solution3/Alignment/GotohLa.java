public class Gotoh extends Scoring{

    private int go;
    private int ge;

    public Gotoh(String seq1, String seq2, SubstitutionMatrix matrix, int go, int ge, AlignmentType mode) {
        super(seq1, seq2, matrix, 0, mode);
        this.go = go;
        this.ge = ge;
    }

    public int score(){
        //brauchen 3 Matrizen
        //1tens Alignment endet mit Match/Mismatch

        //2ten endet mit Gap in Seq1

        //3tens endet mit Gap in Seq2
    }
}
