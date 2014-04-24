/* slow solution using two nested ternary searches */

#include <stdio.h>
#include <string.h>
#include <math.h>

#define MAXITER 500

int n;
double f[52][52];
typedef struct {
	int x1,y1,z1,x2,y2,z2;
} t_linje;
t_linje linje[52];

double dist(double x1,double y1,double z1,double x2,double y2,double z2) {
	double dx=x2-x1,dy=y2-y1,dz=z2-z1;
	return dx*dx+dy*dy+dz*dz;
}

void setpos(double *x1,double *y1,double *z1,int ix,double mid11) {
	*x1=linje[ix].x1+mid11*(linje[ix].x2-linje[ix].x1);
	*y1=linje[ix].y1+mid11*(linje[ix].y2-linje[ix].y1);
	*z1=linje[ix].z1+mid11*(linje[ix].z2-linje[ix].z1);
}

double calcdist(double x,double y,double z,int iy) {
	int it;
	double lo=0,mid1,mid2,hi=1,r1,r2;
	double x1,y1,z1;
	for(it=0;it<MAXITER;it++) {
		mid1=lo+(hi-lo)/3;
		mid2=lo+(hi-lo)/1.5;
		setpos(&x1,&y1,&z1,iy,mid1);
		r1=dist(x,y,z,x1,y1,z1);
		setpos(&x1,&y1,&z1,iy,mid2);
		r2=dist(x,y,z,x1,y1,z1);
		if(r1<r2) hi=mid2;
		else lo=mid1;
	}
	return r1;
}

double calc(int ix,int iy) {
	int it;
	double lo=0,mid1,mid2,hi=1,r1,r2;
	double x1,y1,z1;
	for(it=0;it<MAXITER;it++) {
		mid1=lo+(hi-lo)/3;
		mid2=lo+(hi-lo)/1.5;
		setpos(&x1,&y1,&z1,ix,mid1);
		r1=calcdist(x1,y1,z1,iy);
		setpos(&x1,&y1,&z1,ix,mid2);
		r2=calcdist(x1,y1,z1,iy);
		if(r1<r2) hi=mid2;
		else lo=mid1;
	}
	return sqrt(r1);
}

void solve() {
	int N,x,y,z,i,j,k;
	scanf("%d",&N);
	n=N+2;
	for(i=0;i<2;i++) {
		scanf("%d %d %d",&x,&y,&z);
		linje[i].x1=linje[i].x2=x;
		linje[i].y1=linje[i].y2=y;
		linje[i].z1=linje[i].z2=z;
	}
	for(i=0;i<N;i++) {
		scanf("%d %d %d %d %d %d",&linje[i+2].x1,&linje[i+2].y1,
		  &linje[i+2].z1,&linje[i+2].x2,&linje[i+2].y2,&linje[i+2].z2);
	}
	for(i=0;i<n;i++) f[i][i]=0;
	for(i=0;i<n;i++) for(j=0;j<i;j++) f[i][j]=f[j][i]=calc(i,j);
	for(k=0;k<n;k++) for(i=0;i<n;i++) for(j=0;j<n;j++) if(f[i][j]>f[i][k]+f[k][j])
		f[i][j]=f[i][k]+f[k][j];
	printf("%.15f\n",f[0][1]);
}

int main() {
	int T;
	scanf("%d",&T);
	while(T--) solve();
	return 0;
}
