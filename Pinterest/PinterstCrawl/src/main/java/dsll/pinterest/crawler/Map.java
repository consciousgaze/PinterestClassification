/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dsll.pinterest.crawler;

import java.io.IOException;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

/**
 *
 * @author Ted
 */
public class Map extends Mapper<LongWritable, Text, Text, Text> {
    private final static int nodeNum = 30;

//    private static Mongo mongoClient= new Mongo("52.11.27.173", 27017);
//    private static DB db= mongoClient.getDB("pinterest");
//    private static DBCollection pinCollection= db.getCollection("pins");
//    private static DBCollection boardCollection= db.getCollection("boards");

    @Override
    public void map(LongWritable key, Text value, Mapper.Context context)
          throws IOException, InterruptedException {
        int i = 0;
        for (String token: value.toString().split("\\n+")) {
            String url = "";
            try{
                String [] tmpurl = token.split("\"\"expanded_url\"\":");
                url = tmpurl[1].split("\"\"")[1];
            }catch(Exception e){}
            
            System.out.println("url is: "+url);
            
            if (url.equals("")){
                // pass
            }else if(url.matches("http(s?)://(www\\.)?pinterest\\.com/.*")){
                // check whether has record
                context.write(new Text("Mapper"+String.valueOf(i)), new Text(url));
                i = (i+1)%nodeNum;
            }

        }
    }
}
