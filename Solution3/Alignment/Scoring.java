public class Scoring{
    protected final String seq1;
    protected final String seq2;
    protected SubstitutionMatrix substitution_matrix;
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
    }
    protected int diaScore (int i, int j){
        char x = seq1.charAt(i-1);
        char y = seq2.charAt(j-1);
        return substitution_matrix.getScore(x,y);
    }

    public int checkScore(String al1, String al2){
        int score = 0;
        for (int i=0; i<al1.length(); i++){
            char x = al1.charAt(i);
            char y = al2.charAt(i);
            if (x == '-'||y=='-'){
                score += gap;
            }else{
                score += substitution_matrix.getScore(x,y);
            }
        }
        return score / 100;
    }

    public finalAlignment result(boolean useNW) {
        double score;
        String[] align;

        if(useNW){
            score = DP_score() / 100;
            align = DP_alignment();
        }else{
            score = Gotoh_score() / 100;
            align = Gotoh_alignment();
        }

        return new finalAlignment(align[0], align[1], (int) score);
    }

    public int Rec_score(){
        return new Recursion(seq1, seq2, substitution_matrix, gap, mode).score() / 100;
    }

    public double DP_score(){
        DynamicProgramming dynamicProgramming = new DynamicProgramming(seq1, seq2, substitution_matrix, gap, mode);
        if (mode.isGlobal()){
            return (double)(dynamicProgramming.NW_score()) / 100;
        }
        if (mode.isLocal()){
            return (double) (dynamicProgramming.SW_score()) / 100;
        }
        if (mode.isFreeshift()) {
            return (double) (dynamicProgramming.FS_score()) / 100;
        }
        return Integer.MIN_VALUE;
    }

    public String[] DP_alignment(){
        DynamicProgramming dynamicProgramming = new DynamicProgramming(seq1, seq2, substitution_matrix, gap, mode);
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
        Gotoh gotoh = new Gotoh(seq1, seq2, substitution_matrix, go, ge, mode);
        if (mode.isGlobal()){
            return (double)(gotoh.Global_score()) / 100;
        }
        if (mode.isLocal()){
            return (double)(gotoh.Local_score()) / 100;
        }
        if (mode.isFreeshift()) {
            return (double)(gotoh.FS_score()) / 100;
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
}
