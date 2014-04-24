import java.io.*;
import java.util.*;

public class cellsman_rs {
	public static void main(String[]z) {
		Scanner sc=new Scanner(System.in);
		int T=sc.nextInt();
		while(T-->0) {
			int x=sc.nextInt(),y=sc.nextInt();
			for(int i=0;i<y;i++) sc.next();
			if(x==1) System.out.println(2*(y-1));
			else if(y==1) System.out.println(2*(x-1));
			else System.out.println(x*y+x*y%2); // beware of x*y odd
		}
		System.out.println("LOL");
	}
}
