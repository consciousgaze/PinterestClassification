/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dsll.pinterest.crawler;
import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;
import com.mongodb.Mongo;
import com.mongodb.util.JSON;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import javax.imageio.ImageIO;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

/**
 *
 * @author Ted
 */
public class Reduce extends Reducer<Text, Text, Text, Text> {
    private final static Text pin = new Text("pin");
    private final static Text board = new Text("board");
    private final static Text empty = new Text("empty");

    private  static Mongo mongoClient= new Mongo("52.11.27.173", 27017);
    private  static DB db= mongoClient.getDB("pinterest");
    private  static DBCollection pinCollection= db.getCollection("fast_pins");
    private  static DBCollection boardCollection= db.getCollection("boards");

    private static final BufferedImage dummyImage = new BufferedImage(10, 10, BufferedImage.TYPE_INT_RGB);
    
    @Override
    public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
        System.out.println("Reducer marker!!!!!!");
        for (Text val : values) {
            String url = val.toString();
            if (url.matches("http(s?)://(www\\.)?pinterest\\.com/pin/.*")){
                String id = url.split("/pin/")[1];
                BasicDBObject query = new BasicDBObject("ID", id);
                try{
                    DBCursor c = pinCollection.find(query);
                    if(c.hasNext()){
                        context.write(pin, updatePinContent(url, pinCollection));
                    }else{
                        context.write(pin, getPinContent(url, pinCollection));
                    }
                }catch(Exception e){
                    context.write(pin, new Text(e.toString().replace("\n", "\\n")));
            }
            }else{
                String id = null;
                try{
                    id = url.split("/")[4];
                    BasicDBObject query = new BasicDBObject("ID", id);
                    DBCursor c = boardCollection.find(query);
                    try{
                        if(c.hasNext()){
                            context.write(board, updateBoardContent(url, boardCollection));
                        }else{
                            context.write(board, getBoardContent(url, boardCollection));
                        }
                    }catch(Exception ee){
                        context.write(board, new Text(ee.toString().replace("\n", "\\n")));
                    }
                }catch(Exception e){
                    context.write(board, new Text("Invalid board"+url));
                }
                
            }

        }
    }
    private static Text updatePinContent(String url, DBCollection pinsCollection) throws JSONException, IOException{
        // add more related pins, include more boards
        String id = url.split("/pin/")[1];
        DBCursor c = pinsCollection.find(new BasicDBObject("ID", id));
        DBObject oldPin = c.next();
        JSONArray oldBoards = new JSONArray(oldPin.get("board").toString());
        JSONArray oldRltPin = new JSONArray(oldPin.get("related_pins").toString());

        Document doc = Jsoup.connect(url).get();
        Element bottomDoc = doc.select("div[class=Module CloseupSidebar]").first();

        //pin board
        Element boardEle = bottomDoc.select("div[class=boardHeader]").first();
        JSONArray board = new JSONArray();
        JSONObject b = new JSONObject();
        String boardName = "";
        try{
            boardName = boardEle.select("h3[class=title]").text().trim();
        }catch(Exception ee){}
        String boardSrc = "";
        try{
            boardSrc = "https://www.pinterest.com"+boardEle.select("a").attr("href").trim();
        }catch(Exception ee){}
        b.append("name", boardName);
        b.append("src", boardSrc);
        board.put(b);

        //related pins
        bottomDoc = doc.select("div[class=closeupBottom] div[class=Module CloseupBottom] div[class=relatedPinsWrapper]").first();

        JSONArray relatedPins = new JSONArray();
        Elements relatedPinsConts = bottomDoc.select("div[class=pinWrapper]");
        for(Element relatedPinsCont:relatedPinsConts){
            JSONObject relatedPin = new JSONObject();
            relatedPin.append("src", "https://www.pinterest.com"+relatedPinsCont.select("div[class=pinHolder] > a").attr("href"));
            relatedPins.put(relatedPin);
        }
        
        // process new boards
        List<String> oldBoardNames = new ArrayList<String>();
        for(int i = 0; i<oldBoards.length();i++){
            oldBoardNames.add(oldBoards.getJSONObject(i).getString("name"));
        }
        for(int i = 0; i<board.length();i++){
            JSONObject tmp = board.getJSONObject(i);
            if (oldBoardNames.contains(tmp.getString("name"))){
                continue;
            }
            oldBoards.put(board.get(i));
        }
        
        // process new related pins
        List<String> oldRelatedPins = new ArrayList<String>();
        for(int i =0; i<oldRltPin.length();i++){
            oldRelatedPins.add(oldRltPin.getJSONObject(i).getString("src"));
        }
        for(int i =0; i<relatedPins.length();i++){
            if(oldRelatedPins.contains(relatedPins.getJSONObject(i).get("src"))){
                continue;
            }
            oldRltPin.put(relatedPins.getJSONObject(i));
        }
        
        BasicDBObject newAttr = new BasicDBObject();
        newAttr.append("board", oldBoards);
        newAttr.append("related_pins", oldRltPin);
        BasicDBObject update = new BasicDBObject().append("$set", newAttr);
        
        pinsCollection.update(new BasicDBObject("ID", id), update);
        
        return new Text("Pin "+id+" updated.");
    }
    
    private static Text updateBoardContent(String url, DBCollection baordsCollection) throws JSONException, IOException{
        String id = url.split("/")[4];
        DBCursor c = baordsCollection.find(new BasicDBObject("ID", id));
        DBObject oldPin = c.next();
        JSONArray oldPins = new JSONArray(oldPin.get("pins").toString());

        Elements pinsCont = Jsoup.connect(url).get().select("div[class=pinWrapper]");
        // new pins
        JSONArray pins = new JSONArray();
        for(Element pinCont:pinsCont){
                JSONObject pin = new JSONObject();
                pin.append("src", pinCont.select("div[class=pinHolder]>a").first().attr("href"));
                pins.put(pin);
        }
        
        List<String> oldPinURL = new ArrayList<String>();
        for(int i =0; i<oldPins.length(); i++){
            oldPinURL.add(oldPins.getJSONObject(i).getString("src"));
        }
        
        for(int i = 0; i<pins.length();i++){
            if(oldPinURL.contains(pins.getJSONObject(i).getString("src"))){
                continue;
            }
            oldPins.put(pins.getJSONObject(i));
        }
        
        BasicDBObject newAttr = new BasicDBObject();
        newAttr.append("pins", oldPins);
        BasicDBObject update = new BasicDBObject().append("$set", newAttr);
        
        baordsCollection.update(new BasicDBObject("ID", id), update);
        return new Text("baord "+id+" updated...");
    }
    
    private static Text getPinContent(String url, DBCollection pinsCollection) throws JSONException{
        Document html = null;
        JSONObject pin = new JSONObject();
        try{
                html = Jsoup.connect(url).get();
        }catch(Exception e){
                return new Text("HTTP connection failed...");
        }

        // Gather major pins data
        Element doc = html.select("body").first();
        // Pin ID
        String id = (url.split("pin/")[1].split("/")[0]);
        pin.append("ID", id);

        // Pin image
        String imageURL = "";
        Element tmp = doc.select("div[class=pinImageSourceWrapper]").first();
        try{
            tmp = tmp.select("div[class=imageContainer]").select("img").first();
            imageURL = tmp.attr("src");
        }catch(Exception e){}
//        try{
//            ByteArrayOutputStream pimg=new ByteArrayOutputStream(), cimg = new ByteArrayOutputStream();
//            for(int i=0; i<3; i++){ 
//                BufferedImage img=dummyImage;
//                try{
//                    img = ImageIO.read(new URL(imageURL));
//                
//                }catch(Exception e){}
//                ImageIO.write(img, "jpg", cimg);
//                if(pimg.size()<cimg.size()){
//                        pimg = cimg;
//                }
//            }
//            // save to hdfs
//            Configuration conf = new Configuration();
//            FileSystem fs = FileSystem.get(conf);
//            Path outFile = new Path("/home/hadoop/"+id+".png");
//            FSDataOutputStream out = fs.create(outFile);
//            out.write(pimg.toByteArray());
//
//        }catch(Exception e){
//                e.printStackTrace();
//        }
        pin.append("image", imageURL);

        //Pin name
        tmp = doc.select("h2[itemprop=name]").first();
        String name = "";
        if(tmp!=null){
            name = tmp.text().trim();
        }
        pin.append("name", name);

        // Pin source
        Element sourceCont = doc.select("div[class=sourceFlagWrapper]").first();
        JSONObject source = new JSONObject();
        if (sourceCont!=null){
            String title = sourceCont.text().trim();
            String src = sourceCont.select("a").first().attr("href");
            source.append("title", title);
            source.append("src", src);
        }
        pin.append("source", source);

        //pin credit
        JSONObject pinCredit = new JSONObject();
        Element credit = doc.select("div[class=pinCredits]").first();
        String creditName = "", creditTitle="",creditSource = "";
        try{
                creditName = credit.select("div[class=creditName]").text().trim();
        }catch(Exception e){
        }
        try{
                creditTitle = credit.select("div[class=creditTitle]").text().trim();
        }catch(Exception e){
        }
        try{
                creditSource = credit.select("a").attr("href");
        }catch(Exception e){
        }
        pinCredit.append("name", creditName);
        pinCredit.append("title", creditTitle);
        pinCredit.append("src", creditSource);
        pin.append("credit", pinCredit);

        //comments
        JSONArray comments = new JSONArray();
        Elements commentsConts = doc.select("div[class=commenterNameCommentText]");
        for (Element commentCont:commentsConts){
                JSONObject comment = new JSONObject();
                Element creatorEle = commentCont.select("div[class=commenterWrapper] a").first();
                String creatorName = creatorEle.text().trim();
                String creatorSrc = creatorEle.attr("href");
                String content = "", raw="";
                Element commentContent = commentCont.select(".commentDescriptionContent").first();
                try{
                        content = commentContent.text().trim();
                        raw = commentContent.html();
                comment.append("creator", creatorName);
                comment.append("creator_url", creatorSrc);
                comment.append("content", content);
                comment.append("content_raw", raw);
                comments.put(comment);
                }catch(Exception e){}
                
        }
        pin.append("comments", comments);

        //pin board link and related pins
        Element bottomDoc = doc.select("div[class=Module CloseupSidebar]").first();

        //pin board
        JSONArray board = new JSONArray();
        if(bottomDoc!=null){
            Element boardEle = bottomDoc.select("div[class=boardHeader]").first();
            JSONObject b = new JSONObject();
            String boardName = "";
            try{
                boardName = boardEle.select("h3[class=title]").text().trim();
            }catch(Exception ee){}
            String boardSrc = "";
            try{
                boardSrc = "https://www.pinterest.com"+boardEle.select("a").attr("href").trim();
            }catch(Exception ee){}
            b.append("name", boardName);
            b.append("src", boardSrc);
            board.put(b);
        }
        pin.append("board", board); //CAUTION: what if a pin shows up in different boards?

                //related pins
        bottomDoc = doc.select("div[class=closeupBottom] div[class=Module CloseupBottom] div[class=relatedPinsWrapper]").first();

        JSONArray relatedPins = new JSONArray();
        if(bottomDoc != null){
            Elements relatedPinsConts = bottomDoc.select("div[class=pinWrapper]");
            for(Element relatedPinsCont:relatedPinsConts){
                JSONObject relatedPin = new JSONObject();
                try{
                relatedPin.append("src", "https://www.pinterest.com"+relatedPinsCont.select("div[class=pinHolder] > a").attr("href"));
                }catch(Exception e){}
                relatedPins.put(relatedPin);
            }
        }
        pin.append("related_pins", relatedPins);

                // Optional: push data to database
        BasicDBObject dbObject = (BasicDBObject)JSON.parse(pin.toString());
                pinsCollection.insert(dbObject);
                return new Text(pin.toString());
    }


    private static Text getBoardContent(String url, DBCollection boardsCollection) throws JSONException{
        // NOTE: only board information is crawled. the pins are left to the expanding process
        Document html = null;
        JSONObject board = new JSONObject();
        try{
                html = Jsoup.connect(url).get();
        }catch(Exception e){
                return new Text("HTTP connection failed...");
        }

        // board major information
        String[] tmp = url.split("/");
        String boardID = tmp[4];
        String boardOwnrID = tmp[3];
        String boardName = html.select("h1[class=boardName]").text().trim();
        String boardDesp = html.select("p[class=description]").text().trim();
        String boardOwnr = html.select("h4[classs=fullname]").text().trim();

        // Contained Pins
        Elements pinsCont = html.select("div[class=pinWrapper]");
        JSONArray pins = new JSONArray();
        for(Element pinCont:pinsCont){
                JSONObject pin = new JSONObject();
                pin.append("src", pinCont.select("div[class=pinHolder]>a").first().attr("href"));
                pins.put(pin);
        }
        board.append("ID", boardID);
        board.append("owner_id", boardOwnrID);
        board.append("src", url);
        board.append("name", boardName);
        board.append("description", boardDesp);
        board.append("owner", boardOwnr);
        board.append("pins", pins);

        // Optional: push data to database
        BasicDBObject dbObject = (BasicDBObject)JSON.parse(board.toString());
        boardsCollection.insert(dbObject);
        return new Text(board.toString());
    }
    
}