//Autor: Laura Martin

public enum AlignmentType {
    //alle möglichen Arten die sich von der Anwendung unterscheiden

    global, //Needleman Wunsch start(n,m) Ende (0,0) also ganz rechts unten bis ganz links oben
    local, // Smith-Waterman: start bei max ende wenn 0 erreicht
    freeshift; // start bei höchstem wert in letzer Zeile oder Spalte Ende wenn oben oder links angekommen

    public boolean isGlobal() {return this == global;}
    public boolean isLocal() {return this == local;}
    public boolean isFreeshift() {return this == freeshift;}

    //verwendung durch if(mode.isGlobal() usw.))

}
