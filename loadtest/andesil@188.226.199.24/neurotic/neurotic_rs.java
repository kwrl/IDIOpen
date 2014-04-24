import java.io.*;
import java.util.*;

public class neurotic_rs {
	BufferedReader in=new BufferedReader(new InputStreamReader(System.in));
	StringTokenizer st=new StringTokenizer("");
	String LINE() throws Exception { return in.readLine(); }
	String STR() throws Exception {
		while(!st.hasMoreTokens()) st=new StringTokenizer(LINE());
		return st.nextToken();
	}
	int INT() throws Exception { return Integer.parseInt(STR()); }
	public static void main(String[]a) throws Exception {
		new neurotic_rs().go();
	}
	void go() throws Exception {
		int T=INT();
		while(T-->0) solve();
	}
	void solve() throws Exception {
		int MOD=1000000007;
		int n=INT();
		int parent[]=new int[n];
		int weight[]=new int[n];
		boolean leaf[]=new boolean[n];
		parent[0]=-1;
		for(int i=1;i<n;i++) parent[i]=INT();
		weight[0]=0;
		for(int i=1;i<n;i++) weight[i]=INT();
		Arrays.fill(leaf,true);
		for(int i=1;i<n;i++) leaf[parent[i]]=false;

		long value[]=new long[n];
		for(int i=0;i<n;i++) value[i]=leaf[i]?1:0;
		// q holds at any time all unprocessed nodes such that all their
		// upstream neighbours are processed
		LinkedList<Integer> q=new LinkedList<Integer>();
		int indeg[]=new int[n];
		for(int i=1;i<n;i++) indeg[parent[i]]++;
		for(int i=1;i<n;i++) if(leaf[i]) q.add(i);
		while(!q.isEmpty()) {
			int at=q.poll();
			int next=parent[at];
			if(next>0) {
				indeg[next]--;
				if(indeg[next]==0) q.add(next);
			}
			value[next]=(value[next]+value[at]*weight[at])%(2*MOD);
		}
		if(value[0]%2==0) System.out.println("FREAK OUT");
		else System.out.println(value[0]%MOD);
	}
}
