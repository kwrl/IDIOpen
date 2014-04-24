/* backtracking solution that should not run within the time limit
   by ruben spaans */

#include <stdio.h>

char b[16][16];
int x,y;
int MOD=1000000007;

int btr(int atx,int aty,int k) {
	int i,j,r=0,x2,y2,left;
	if(atx==x) atx=0,aty++;
	if(aty==y) return k==0;
	/* prune if it's impossible to place k kings on the remaining squares */
	left=(y-aty)*x+x-atx;
	if(left<2*k-1) return 0;
	/* place king */
	if(k && !b[atx][aty]) {
		for(i=-1;i<2;i++) for(j=-1;j<2;j++) {
			x2=atx+i; y2=aty+j;
			if(x2>=0 && y2>=0 && x2<x && y2<y) b[x2][y2]++;
		}
		r=btr(atx+1,aty,k-1);
		for(i=-1;i<2;i++) for(j=-1;j<2;j++) {
			x2=atx+i; y2=aty+j;
			if(x2>=0 && y2>=0 && x2<x && y2<y) b[x2][y2]--;
		}
	}
	/* don't place king */
	return (r+btr(atx+1,aty,k))%MOD;
}

int main() {
	int T,k;
	scanf("%d",&T);
	while(T--) {
		scanf("%d %d %d",&x,&y,&k);
		printf("%d\n",btr(0,0,k));
	}
	return 0;
}
