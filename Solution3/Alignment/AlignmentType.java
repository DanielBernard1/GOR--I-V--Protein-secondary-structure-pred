public enum AlignmentType {
    //alle möglichen Arten die sich von der Anwendung unterscheiden

    Global, //Needleman Wunsch start(n,m) Ende (0,0) also ganz rechts unten bis ganz links oben
    Local, // Smith-Waterman: start bei max ende wenn 0 erreicht
    Freeshift; // start bei höchstem wert in letzer Zeile oder Spalte Ende wenn oben oder links angekommen

    public boolean isGlobal() {return this == Global;}
    public boolean isLocal() {return this == Local;}
    public boolean isFreeshift() {return this == Freeshift;}

    //verwendung durch if(mode.isGlobal() usw.))

}
