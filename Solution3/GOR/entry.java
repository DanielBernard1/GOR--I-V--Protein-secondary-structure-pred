public class entry {
    public final String header;
    public final char[] seq;
    public final char[] ss;  // kann null sein

    public entry(String header, char[] seq, char[] ss) {
        this.header = header;
        this.seq = seq;
        this.ss = ss;
    }
}
