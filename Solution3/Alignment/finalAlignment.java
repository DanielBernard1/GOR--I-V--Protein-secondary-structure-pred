public class finalAlignment {
    protected String align1;
    protected String align2;

    protected double score;

    public finalAlignment(String align1, String align2, double score){
        this.align1 = align1;
        this.align2 = align2;
        this.score = score;
    }

    public String getAlign1(){
        return align1;
    }
    public String getAlign2(){
        return align2;
    }
    public double getScore(){
        return score;
    }

}
