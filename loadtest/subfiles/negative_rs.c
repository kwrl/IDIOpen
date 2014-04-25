#include <stdio.h>

int main() {
	int T,m,i,cur,low,a,b;
	scanf("%d",&T);
	while(T--) {
		scanf("%d",&m);
		for(low=cur=i=0;i<m;i++) {
			scanf("%d %d",&a,&b);
			cur+=a-b;
			if(low>cur) low=cur;
		}
		printf("%d\n",-low);
	}
	return 0;
}
