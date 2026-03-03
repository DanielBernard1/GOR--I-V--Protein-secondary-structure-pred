import java.util.List;

public class Train_main {
    public static void main(String[] args) {
        Train a =new Train();
        for(entry e:a.read()){
            System.out.println(e.header);
            System.out.println(e.seq);
            System.out.println(e.ss);

        }

    }
}
