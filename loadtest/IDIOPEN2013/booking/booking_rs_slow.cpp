/* This solution is too slow, since the flow (residual graph) is
   cleared between each booking. */

#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <string>
#include <map>
#include <vector>

#define MAXRES 200
#define MAXQUAL 100

#define MAXC 16
#define MAXD 16

using namespace std;

/* set up flow graph:
   - from source to each resource (cap 1)
   - from resource to each capability it has (cap 1)
   - from capability to sink (cap: sum of requirements from current
     bookings)
*/

typedef unsigned long long ull;

/* mapping from capability name to int */
map<string,int> capability;
int ids;

int resource[MAXRES][MAXC]; /* list of capabilities */
int rno[MAXRES];
int rn; /* number of resources */
int qn; /* number of queries */
int cn; /* number of capabilities, total */

map<int,int> bookingmap; /* mapping from bookingid to position in array */
int bookings[MAXRES+1][MAXD];
int bookn[MAXRES+1];
int bookingid[MAXRES+1];
int bn;

int getid(string s) {
	if(capability.find(s)!=capability.end()) return capability[s];
	capability[s]=ids;
	return ids++;
}

int getid2(string s) {
	if(capability.find(s)!=capability.end()) return capability[s];
	return -1;
}

#define MAXV MAXRES+MAXQUAL+2
#define MAXE 2000000
#define INF 1000000000

/* maxflow! uses edge lists and assumes that cost=1 everywhere.
   uses bfs to find augmenting paths.
   however, memory usage is MAXV*MAXV.

   usage: (no need to init f[][]!)
   - set MAXV,MAXE to guaranteed maximum values for the problem
   - set n to desired number of nodes, set ne=0
   - add edges using the macro addedge(from,to,capacity), no need to set
     backedges
   - call countingsort(), then maxflow(source,sink)

   nb! the above only works if an edge only occurs once and in one
   direction. if both (a,b), (b,a) exist or multiple (a,b) exist, then
   init f[][] first, and update f[][], from[], to[] manually instead of
   using the macro
*/
int f[MAXV][MAXV];      /*  initial flow, 0 means no edge */
int n,ne;               /*  number of nodes, number of edges */
int from[MAXE],to[MAXE];/*  edge i: from[i] to[i] */
int gs[MAXV+1];         /*  gs[i]: start of edges from i, gs[i+1]: end */

int maxflow(int source,int sink) {
	int i,j,done,flow=0,done2,a,r,qe=0,k,l;
	static char t[MAXV];
	static int parent[MAXV],min[MAXV],q[MAXV];
	memset(t,0,n);
	memset(parent,-1,n*sizeof(int));
	memset(min,126,n*sizeof(int));
	do {
		done=1;
		t[source]=1;
		q[qe++]=source;
		do {
			done2=1;
			for(k=0;k<qe;k++) if(t[i=q[k]]) for(l=gs[i];l<gs[i+1];l++) {
				j=to[l];
				if(!t[j] && f[i][j]>0) {
					a=f[i][j];
					t[j]=1; parent[j]=i; done2=0;
					q[qe++]=j;
					if(min[i]<a) min[j]=min[i]; else min[j]=a;
					if(j==sink) { done=0; goto out; }
				}
			}
		} while(!done2);
		break;
	out:
		i=sink; r=min[sink];
		while(i!=-1) {
			j=parent[i]; if(j==-1) break;
			f[j][i]-=r; f[i][j]+=r;
			i=j;
		}
		flow+=r;
		while(qe) {
			j=q[--qe];
			t[j]=0; parent[j]=-1; min[j]=INF;
		}
	} while(!done);
	return flow;
}

void countingsort() {
	static int newto[MAXE];
	int i,j;
	for(i=0;i<=n;i++) gs[i]=0;
	for(i=0;i<ne;i++) gs[from[i]]++;
	for(i=1;i<n;i++) gs[i]+=gs[i-1];
	gs[n]=ne;
	for(i=0;i<ne;i++) {
		j=--gs[from[i]];
		newto[j]=to[i];
	}
	for(i=0;i<ne;i++) to[i]=newto[i];
	for(i=0;i<n;i++) for(j=gs[i];j<gs[i+1];j++) from[j]=i;
}

/* add an edge */
#define addedge(a,b,c) from[ne]=a,to[ne++]=b,from[ne]=b,to[ne++]=a,f[a][b]=c,f[b][a]=0;

int from2[MAXE],to2[MAXE],ne2;
/* left: resources, right: capabilities */
/* max n: 2 + 50 + 100 = 152 */
int source,left,right,sink;

void constructgraph() {
	source=0;
	left=1;
	right=left+rn;
	sink=right+ids;
	n=sink+1;
	ne=ne2=0;
	/* source to resources: cap 1 */
	for(int i=0;i<rn;i++) {
		addedge(source,left+i,1);
		from2[ne2]=source; to2[ne2++]=left+i;
	}
	/* for each resource, edge to all its capabilities */
	for(int i=0;i<rn;i++) for(int k=0;k<rno[i];k++) {
		int j=resource[i][k];
		addedge(left+i,right+j,1);
		from2[ne2]=left+i; to2[ne2++]=right+j;
	}
	/* for each capability, edge to sink (cap 0 for now) */
	for(int i=0;i<ids;i++) addedge(right+i,sink,0);
	countingsort();
}

void readresources() {
	capability.clear();
	ids=0;
	memset(resource,0,sizeof(resource));
	scanf("%d %d",&rn,&qn);
	cn=0;
	for(int i=0;i<rn;i++) {
		int n;
		scanf("%d",&n);
		cn+=n;
		rno[i]=0;
		for(int j=0;j<n;j++) {
			static char s[65536];
			scanf("%s",s);
			int id=getid(s);
			/* safeguard: check if qualification exists */
			for(int k=0;k<rno[i];k++) if(resource[i][k]==id) goto fail;
			resource[i][rno[i]++]=id;
		fail:;
		}
	}
}

/* how much we need of each resource */
int req[MAXQUAL+10];

/* check if we can fulfill the graph with current bookings */
int can() {
	int need=0,flow;
	for(int i=0;i<bookn[bn-1];i++) req[bookings[bn-1][i]]++;
	/* set caps */
	for(int i=0;i<ids;i++) {
		need+=f[right+i][sink]=req[i];
		f[sink][right+i]=0;
	}
	if(need>rn) {
		for(int i=0;i<bookn[bn-1];i++) req[bookings[bn-1][i]]--;
		return 0;
	}
	for(int i=0;i<ne2;i++) {
		f[from2[i]][to2[i]]=1;
		f[to2[i]][from2[i]]=0;
	}
//	for(int i=0;i<ne;i++) if(from[i]<to[i]) printf("  %d -> %d (%d)\n",from[i],to[i],f[from[i]][to[i]]);
	flow=maxflow(source,sink);
//	printf("need %d, flow %d\n",need,flow);
	if(flow!=need) {
		for(int i=0;i<bookn[bn-1];i++) req[bookings[bn-1][i]]--;
		return 0;
	}
	return 1;
}

void removebooking(int id) {
	int pos=bookingmap[id];
	bookingmap.erase(id);
	/* remove from req */
	for(int i=0;i<bookn[pos];i++) req[bookings[pos][i]]--;
	for(int i=pos+1;i<bn;i++) {
		for(int j=0;j<bookn[i];j++) bookings[i-1][j]=bookings[i][j];
		bookn[i-1]=bookn[i];
		bookingid[i-1]=bookingid[i];
		bookingmap[bookingid[i-1]]=i-1;
	}
	bn--;
}

void solvecase() {
	for(int i=0;i<ids;i++) req[i]=0;
	bn=0;
	bookingmap.clear();
	while(qn--) {
		static char s[65536];
		int id;
		scanf("%s %d",s,&id);
		if(!strcmp("cancel",s)) {
			if(bookingmap.find(id)==bookingmap.end()) puts("Rejected");
			else {
				removebooking(id);
				puts("Accepted");
			}
		} else {
			int n;
			scanf("%d",&n);
			if(bookingmap.find(id)!=bookingmap.end()) {
				puts("Rejected");
				for(int j=0;j<n;j++) scanf("%s",s);
			} else {
				bookn[bn]=0;
				int failed=0;
				for(int j=0;j<n;j++) {
					scanf("%s",s);
					int id=getid2(s);
					if(id<0) failed=1;
					else bookings[bn][bookn[bn]++]=id;
				}
				bn++;
				if(!failed && can()) {
					puts("Accepted");
					bookingmap[id]=bn-1;
					bookingid[bn-1]=id;
				} else {
					puts("Rejected");
					bn--;
				}
			}
		}
	}
}

void solve() {
	readresources();
	constructgraph();
	solvecase();
}

int main() {
	int T;
	scanf("%d",&T);
	while(T--) solve();
	return 0;
}
