import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;


public class Train {

int size = 17;
List<entry> data  = new ArrayList<>();


public List<entry> read(){
    String line;

    try {
        BufferedReader br = new BufferedReader(new FileReader("C:\\Users\\lucia\\IdeaProjects\\propragruppe15\\Solution3\\GorI\\seclib"));
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;

            if (line.startsWith(">")) {
                String header = line.substring(1).trim();

                String seqLine = br.readLine();
                String ssLine  = br.readLine();

                if (seqLine == null || ssLine == null) break;

                char[] seq = seqLine.trim().toCharArray();
                char[] ss  = ssLine.trim().toCharArray();
            entry a  = new entry(header, seq, ss);
            data.add(a);

        }


        }
    }
    catch (IOException e){System.out.println(e);}
  return data;
    }



public Model train(){Model model = new Model(size);

   for(entry e:data){
       for(char c:e.seq){



   }

    }




    for (int i = 0; i < size-1;i++ ) {
        for (int j = 0; j < 19;j++ ) {



    }



}


}




