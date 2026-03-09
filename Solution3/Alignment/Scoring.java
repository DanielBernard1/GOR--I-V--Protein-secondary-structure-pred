//Autor David und Laura (50/50)

public class Scoring{
    protected final String seq1;
    protected final String seq2;
    protected final String sseq1;
    protected final String sseq2;
    protected boolean secStruct;
    protected SubstitutionMatrix substitution_matrix;
    protected SecondaryStructureMatrix secondaryStructureMatrix;
    protected int gap, go, ge;
    protected AlignmentType mode;

    public Scoring(String seq1, String seq2, SubstitutionMatrix substitution_matrix, int go, int ge, AlignmentType mode){
        this.seq1 = seq1;
        this.seq2 = seq2;
        this.substitution_matrix = substitution_matrix;
        this.gap = ge;
        this.go = go;
        this.ge = ge;
        this.mode = mode;
        sseq1 = null;
        sseq2 = null;
        secStruct = false;
        secondaryStructureMatrix = null;
    }
    public Scoring(String aseq1, String aseq2, String sseq1, String sseq2, SubstitutionMatrix substitutionMatrix, SecondaryStructureMatrix secondaryStructureMatrix, int go, int ge, AlignmentType mode){
        this.seq1 = aseq1;
        this.seq2 = aseq2;
        this.sseq1 = sseq1;
        this.sseq2 = sseq2;
        this.substitution_matrix = substitutionMatrix;
        this.secondaryStructureMatrix = secondaryStructureMatrix;
        this.go = go;
        this.ge = ge;
        this.gap = ge;
        this.mode = mode;
        secStruct = true;
    }
    protected int diaScore (int i, int j){
        char x = seq1.charAt(i-1);
        char y = seq2.charAt(j-1);
        if (secStruct){
            assert sseq1 != null;
            assert sseq2 != null;
            return ((substitution_matrix.getScore(seq1.charAt(i - 1), seq2.charAt(j - 1))) * 70
                    + (secondaryStructureMatrix.getScore(sseq1.charAt(i-1), sseq2.charAt(j-1))) * 30) / 100;
        }
        else {
            return substitution_matrix.getScore(x,y);
        }
    }

    public double checkScore(String al1, String al2){
        int score = 0;
        int gapLen = 0;
        for (int i=0;i<al1.length();i++){
            char x = al1.charAt(i);
            char y = al2.charAt(i);

            if(x=='-' || y=='-'){
                gapLen++;
            }else{
                if(gapLen>0){
                    score += go + ge*gapLen;
                    gapLen=0;
                }
                score += substitution_matrix.getScore(x,y);
            }
        }
        if(gapLen>0){
            score += go + ge*gapLen;
        }
        return score/100.0;
    }

    public finalAlignment result(boolean useNW) {
        double score;
        String[] align;

        if(useNW){
            score = DP_score();
            align = DP_alignment();
        }else{
            score = Gotoh_score();
            align = Gotoh_alignment();
        }

        return new finalAlignment(align[0], align[1], score);
    }

    public double Rec_score(){
        return new Recursion(seq1, seq2, substitution_matrix, gap, mode).score() / 100.0;
    }

    public double DP_score(){
        DynamicProgramming dynamicProgramming;
        if (secStruct){
            dynamicProgramming = new DynamicProgramming(seq1, seq2, sseq1, sseq2, substitution_matrix, secondaryStructureMatrix, gap, mode);
        }
        else{
            dynamicProgramming = new DynamicProgramming(seq1, seq2, substitution_matrix, gap, mode);
        }

        if (mode.isGlobal()){
            return (double)(dynamicProgramming.NW_score()) / 100.0;
        }
        if (mode.isLocal()){
            return (double) (dynamicProgramming.SW_score()) / 100.0;
        }
        if (mode.isFreeshift()) {
            return (double) (dynamicProgramming.FS_score()) / 100.0;
        }
        return Integer.MIN_VALUE;
    }

    public String[] DP_alignment(){
        DynamicProgramming dynamicProgramming;
        if (secStruct){
            dynamicProgramming = new DynamicProgramming(seq1, seq2, sseq1, sseq2, substitution_matrix, secondaryStructureMatrix, gap, mode);
        }
        else{
            dynamicProgramming = new DynamicProgramming(seq1, seq2, substitution_matrix, gap, mode);
        }
        if (mode.isGlobal()){
            return dynamicProgramming.NW_alignment();
        }
        if (mode.isLocal()){
            return dynamicProgramming.SW_alignment();
        }
        if (mode.isFreeshift()) {
            return dynamicProgramming.FS_alignment();
        }
        return null;
    }

    public double Gotoh_score(){
        Gotoh gotoh;
        if (secStruct){
            gotoh = new Gotoh(seq1, seq2, sseq1, sseq2, substitution_matrix, secondaryStructureMatrix, go, ge, mode);
        }
        else {
            gotoh = new Gotoh(seq1, seq2, substitution_matrix, go, ge, mode);
        }
        if (mode.isGlobal()){
            return (double)(gotoh.Global_score()) / 100.0;
        }
        if (mode.isLocal()){
            return (double)(gotoh.Local_score()) / 100.0;
        }
        if (mode.isFreeshift()) {
            return (double)(gotoh.FS_score()) / 100.0;
        }
        return Integer.MIN_VALUE;
    }

    public String[] Gotoh_alignment(){
        Gotoh gotoh = new Gotoh(seq1, seq2, substitution_matrix, go, ge, mode);
        if (mode.isGlobal()){
            return gotoh.Global_alignment();
        }
        if (mode.isLocal()){
            return gotoh.local_alignment();
        }
        if (mode.isFreeshift()) {
            return gotoh.FS_alignment();
        }
        return null;
    }
    public int[][] getScoring_matrix() {
        DynamicProgramming dynamicProgramming = new DynamicProgramming(seq1, seq2, substitution_matrix, gap, mode);
        return dynamicProgramming.getScoring_matrix();
    }
}