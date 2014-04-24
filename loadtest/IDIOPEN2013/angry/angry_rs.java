import java.io.*;
import java.util.*;

public class angry_rs {
	public static void main(String[]a) {
		Scanner in=new Scanner(System.in);
		int T=Integer.parseInt(in.nextLine());
		while(T-->0) {
			String t[]=in.nextLine().split(" ");
			int count=0;
			for(String s:t) {
				if(s.equals("u")) count++;
				else if(s.equals("ur")) count++;
				else if(s.contains("lol")) count++;
			}
			for(int i=0;i<t.length-1;i++) {
				if(t[i+1].equals("of") && (t[i].equals("should") || t[i].equals("would"))) count++;
			}
			System.out.println(count*10);
		}
	}
}
