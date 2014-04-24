import java.io.*;
import java.util.*;

public class spawns_rs {
	public static void main(String[]z) {
		Scanner sc=new Scanner(System.in);
		int T=sc.nextInt();
		while(T-->0) {
			int w=sc.nextInt(),m=sc.nextInt();
			int a[]=new int[m];
			for(int i=0;i<m;i++) a[i]=sc.nextInt();
			Arrays.sort(a);
			int s=0,r;
			for(r=0;r<m && s<w;r++) s+=a[m-r-1];
			if(s<w) System.out.println("no rest for Ruben");
			else System.out.println(r);
		}
	}
}