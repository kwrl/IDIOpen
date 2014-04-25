/* dp where rows are processed one by one.
   time complexity: O(x*y^2*3.236^x), not necessarily a tight bound
   solution by ruben spaans */

import java.util.*;
import java.io.*;

public class kings_rs {
	int MOD=1000000007;
	// list of eligible ways to place kings
	int list[]=new int[65536]; // bitmasks of king placements
	int listk[]=new int[65536]; // number of kings placed in list
	int ln; // number of entries in list
	void btr(int avoid,int mask,int atx,int x,int k) {
		while(atx<x && (avoid&(1<<atx))>0) atx++;
		if(atx>=x) {
			list[ln]=mask;
			listk[ln++]=k;
			return;
		}
		// place, advance x by 2 since kings cannot be adjacent
		btr(avoid,mask|(1<<atx),atx+2,x,k+1);
		// don't place
		btr(avoid,mask,atx+1,x,k);
	}
	void generate(int x,int m2) {
		ln=0;
		btr(m2,0,0,x,0);
	}
	int solve(int x,int y,int k) {
		// trivial case: cannot fit k kings no matter what
		if(((x+1)/2)*((y+1)/2)<k) return 0;
		int dp[][][]=new int[y+1][1<<x][k+1];
		dp[0][0][0]=1;
		for(int row=0;row<y;row++) {
			for(int mask=0;mask<(1<<x);mask++) {
				for(int kings=0;kings<=k;kings++) if(dp[row][mask][kings]>0) {
					// create a mask where we mark cells that
					// kings in the previous row can reach
					int m2=(mask | (mask<<1) | (mask>>1))&((1<<x)-1);
					// generate all ways to place kings that avoids
					// the cells in this bitmask
					generate(x,m2);
					for(int i=0;i<ln;i++) if((m2&list[i])==0 && listk[i]+kings<=k) {
						dp[row+1][list[i]][listk[i]+kings]=(dp[row+1][list[i]][listk[i]+kings]+dp[row][mask][kings])%MOD;
					}
				}
			}
		}
		int ans=0;
		for(int i=0;i<(1<<x);i++) ans=(ans+dp[y][i][k])%MOD;
		return ans;
	}
	void go() {
		Scanner in=new Scanner(System.in);
		int T=in.nextInt();
		while(T-->0) {
			int x=in.nextInt();
			int y=in.nextInt();
			int k=in.nextInt();
			System.out.printf("%d\n",solve(x,y,k));
		}
	}
	public static void main(String[]a) {
		new kings_rs().go();
	}
}
