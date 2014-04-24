/* n^2 algorithm that tries to be marginally clever. should not
   run within the time limit */

#include <stdio.h>

#define MAX 10002
typedef long long ll;

#define MOD 1000000007

int n;
int to[MAX];
int w[MAX];
ll val[MAX];

void readinput() {
	int i;
	scanf("%d",&n);
	for(i=1;i<n;i++) scanf("%d",&to[i]);
	for(i=1;i<n;i++) scanf("%d",&w[i]);
}

void solve() {
	static int in[MAX];
	static char taken[MAX];
	int i,done;
	for(i=0;i<n;i++) in[i]=taken[i]=0;
	for(i=1;i<n;i++) in[to[i]]++;
	for(i=0;i<n;i++) val[i]=(in[i]==0)?1:0;
	do {
		done=1;
		/* dubious heuristic: sweep back and forth */
		for(i=1;i<n;i++) if(!taken[i] && !in[i]) {
			in[to[i]]--;
			taken[i]=1;
			val[to[i]]+=(w[i]*val[i])%(2*MOD);
			done=0;
		}
		for(i=n-1;i;i--) if(!taken[i] && !in[i]) {
			in[to[i]]--;
			taken[i]=1;
			val[to[i]]+=(w[i]*val[i])%(2*MOD);
			done=0;
		}
	} while(!done);
	if(val[0]&1) printf("%d\n",(int)(val[0]%MOD));
	else puts("FREAK OUT");
}

int main() {
	int T;
	scanf("%d",&T);
	while(T--) {
		readinput();
		solve();
	}
	return 0;
}
