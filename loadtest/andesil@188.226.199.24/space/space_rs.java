/* ternary search on one of the lines, use point-to-distance within search */

import java.util.*;
import java.math.*;

public class space_rs {
	public static void main(String[]a) {
		new space_rs().go();
	}

	int ln; /* lines */
	int[] x1,y1,z1,x2,y2,z2;

	double f[][]; /* shortest distance between each line */

	/* squared distance */
	double distsq(double x1,double y1,double z1,double x2,double y2,double z2) {
		double dx=x1-x2,dy=y1-y2,dz=z1-z2;
		return dx*dx+dy*dy+dz*dz;
	}

	/* distance from point (x,y,z) to line segment (x1,y1,z1)-(x2,y2,z2) */
	double pointtoline(double x,double y,double z,double x1,double y1,
	                   double z1,double x2,double y2,double z2) {
		double vx=x2-x1, vy=y2-y1, vz=z2-z1;
		double wx=x-x1, wy=y-y1, wz=z-z1;
		double c1=vx*wx+vy*wy+vz*wz;
		/* left endpoint closest? */
		if(c1<0) return Math.sqrt(distsq(x,y,z,x1,y1,z1));
		double c2=vx*vx+vy*vy+vz*vz;
		/* right endpoint closest? */
		if(c2<=c1) return Math.sqrt(distsq(x,y,z,x2,y2,z2));
		double b=c1/c2;
		/* find the actual point in the segment */
		double bx=x1+vx*b, by=y1+vy*b, bz=z1+vz*b;
		return Math.sqrt(distsq(bx,by,bz,x,y,z));
	}

	double calcdist(double x,double y,double z,int iy) {
		return pointtoline(x,y,z,x1[iy],y1[iy],z1[iy],x2[iy],y2[iy],z2[iy]);
	}

	double ternarydist(int ix,int iy) {
		double lo=0,hi=1;
		int dx=x2[ix]-x1[ix],dy=y2[ix]-y1[ix],dz=z2[ix]-z1[ix];
		for(int it=0;it<400;it++) {
			double m1=lo+(hi-lo)/3;
			double m2=lo+(hi-lo)/1.5;
			double r1=calcdist(x1[ix]+dx*m1,y1[ix]+dy*m1,z1[ix]+dz*m1,iy);
			double r2=calcdist(x1[ix]+dx*m2,y1[ix]+dy*m2,z1[ix]+dz*m2,iy);
			if(r1<r2) hi=m2;
			else lo=m1;
		}
		return calcdist(x1[ix]+dx*lo,y1[ix]+dy*lo,z1[ix]+dz*lo,iy);
	}

	void go() {
		Scanner sc=new Scanner(System.in);
		int T=sc.nextInt();
		while(T-->0) {
			int n=sc.nextInt();
			ln=n+2;
			x1=new int[ln];
			y1=new int[ln];
			z1=new int[ln];
			x2=new int[ln];
			y2=new int[ln];
			z2=new int[ln];
			/* treat start and end as degenerate lines */
			x1[0]=x2[0]=sc.nextInt();
			y1[0]=y2[0]=sc.nextInt();
			z1[0]=z2[0]=sc.nextInt();
			x1[n+1]=x2[n+1]=sc.nextInt();
			y1[n+1]=y2[n+1]=sc.nextInt();
			z1[n+1]=z2[n+1]=sc.nextInt();
			for(int i=0;i<n;i++) {
				x1[i+1]=sc.nextInt();
				y1[i+1]=sc.nextInt();
				z1[i+1]=sc.nextInt();
				x2[i+1]=sc.nextInt();
				y2[i+1]=sc.nextInt();
				z2[i+1]=sc.nextInt();
			}
			/* calculate all pairwise distances */
			f=new double[ln][ln];
			for(int i=0;i<ln;i++) f[i][i]=0; 
			for(int i=0;i<ln;i++) for(int j=0;j<i;j++)
				f[j][i]=f[i][j]=ternarydist(i,j);
			/* floyd-warshall */
			for(int k=0;k<ln;k++) for(int i=0;i<ln;i++) for(int j=0;j<ln;j++) 
				f[i][j]=Math.min(f[i][j],f[i][k]+f[k][j]);
			System.out.println(f[0][n+1]);
		}
	}
}
