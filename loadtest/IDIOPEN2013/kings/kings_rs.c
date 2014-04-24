/* cell-by-cell dp keeping a bitmask of coming cells which cannot contain
   king. precalculate all answers and answer queries in O(1).
   time complexity: O(x^4*2^(x+1)) for a given width x
   by ruben spaans */

#include <stdio.h>
#include <string.h>

#define MOD 1000000007
#define MAX 15
#define MAXK ((MAX+1)/2)*((MAX+1)/2)
int dp[2][MAXK+1][1<<(MAX+1)];
int ans[MAX*MAX+1][MAX+1][MAX+1];

void calc(int n) {
	int prev=0,cur=1,x,y,k,M=((n+1)/2)*((n+1)/2),m,z,v;
	memset(dp,0,sizeof(dp));
	dp[prev][0][0]=1;
	for(y=0;y<n;y++) {
		for(x=0;x<n;x++) {
			memset(dp[cur],0,sizeof(dp[cur]));
			for(k=0;k<=M;k++) for(m=0;m<(1<<(n+1));m++) if((v=dp[prev][k][m])) {
				z=(m>>1)|(1<<(n-1))|(x?1<<(n-2):0)|(x<n-1?(1<<n)|1:0);
				/* place king */
				if(k<M && !(m&1)) {
					dp[cur][k+1][z]+=v;
					if(dp[cur][k+1][z]>=MOD) dp[cur][k+1][z]-=MOD;
				}
				/* don't place king */
				dp[cur][k][m>>1]+=v;
				if(dp[cur][k][m>>1]>=MOD) dp[cur][k][m>>1]-=MOD;
			}
			cur=prev; prev=1-cur;
		}
		for(k=0;k<=M;k++) {for(m=0;m<(1<<(n+1));m++) if(dp[prev][k][m]) {
			ans[k][y+1][n]+=dp[prev][k][m];
			if(ans[k][y+1][n]>=MOD) ans[k][y+1][n]-=MOD;}
		}
	}
}

void precalc() {
	int n;
	memset(ans,0,sizeof(ans));
	ans[1][1][1]=1;
	for(n=2;n<=MAX;n++) calc(n);
}

int main() {
	int T,x,y,k,t;
	precalc();
	scanf("%d",&T);
	while(T--) {
		scanf("%d %d %d",&x,&y,&k);
		if(x>y) t=x,x=y,y=t;
		printf("%d\n",ans[k][x][y]);
	}
	return 0;
}
