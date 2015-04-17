package dsll.pinterest.crawler;

import java.util.Arrays;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
//import com.amazonaws.auth.BasicAWSCredentials;
import java.awt.image.BufferedImage;

@SuppressWarnings("deprecation")
public class Crawler extends Configured implements Tool {
        //private static BasicAWSCredentials cred = new BasicAWSCredentials("AKIAICYSGZ5KW3MSJ5OQ", "z7ek8JflNE1XkPKfUoET0Esh7XSL5x4ung0rwODy");
	//private static ProfileCredentialsProvider cred = new ProfileCredentialsProvider();
//	private static String imageFolder = "http://pinterest-crawling.s3-website-us-west-2.amazonaws.com";
	
	public static void main(String[] args) throws Exception {
	      System.out.println(Arrays.toString(args));

	      int res = ToolRunner.run(new Configuration(), new Crawler(), args);
	      
	      System.exit(res);
	}
	
	

	@Override
        public int run(String[] args) throws Exception {
           System.out.println(Arrays.toString(args));
           Job job = new Job(getConf(), "Crawler");
           job.setJarByClass(Crawler.class);
           job.setOutputKeyClass(Text.class);
           job.setOutputValueClass(Text.class);

           job.setMapperClass(Map.class);
           job.setReducerClass(Reduce.class);

           job.setInputFormatClass(TextInputFormat.class);
           job.setOutputFormatClass(TextOutputFormat.class);

           FileInputFormat.addInputPath(job, new Path(args[0]));
           FileOutputFormat.setOutputPath(job, new Path(args[1]));

           job.waitForCompletion(true);

           return 0;
        }
}
