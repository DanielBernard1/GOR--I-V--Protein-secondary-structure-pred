public class ProteinData {
    public String id;
    public String sequence;
    public String structure;
    public String structureH;
    public String structureE;
    public String structureC;

    public ProteinData(String id, String sequence, String structure ,String structureH, String structureE, String structureC) {
        this.id = id;
        this.sequence = sequence;
        this.structure = structure;
        this.structureH = structureH;
        this.structureE = structureE;
        this.structureC = structureC;
    }

    public ProteinData(String id, String sequence, String structure) {
        this.id = id;
        this.sequence = sequence;
        this.structure = structure;
    }
    public void print(boolean probs) {
        System.out.println(id);
        System.out.println("AS " + sequence);
        System.out.println("SS " + structure);
        if (probs) {
            System.out.println("PH " + structureH);
            System.out.println("PE " + structureE);
            System.out.println("PC " + structureC);
        }
    }
    public void print(String html, boolean probs) {
        System.out.println("<html>)");
        System.out.println("<body>)");
        System.out.println("<pre>)");

        System.out.println(id);
        System.out.println("AS " + sequence);
        System.out.println("SS " + structure);
        if (probs) {
            System.out.println("PH " + structureH);
            System.out.println("PE " + structureE);
            System.out.println("PC " + structureC);
        }
        System.out.println("</pre>)");
        System.out.println("</body>)");
        System.out.println("</html>)");

    }
}