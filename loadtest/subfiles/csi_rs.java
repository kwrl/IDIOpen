import java.util.*;

public class csi_rs {
	public static void main(String[]a) {
		new csi_rs().go();
	}
	int r,c;
	int flowers,birds;
	char m[][];
	boolean isthing(int x,int y) {
		if(x<0 || y<0 || x>=r || y>=c) return false;
		return m[x][y]=='|' ||
		       m[x][y]=='/' ||
		       m[x][y]=='\\' ||
		       m[x][y]=='-' ||
		       m[x][y]=='@';
	}
	boolean isnothing(int x,int y) {
		if(x<0 || y<0 || x>=r || y>=c) return true;
		return m[x][y]==0 || m[x][y]=='.';
	}
	int dx[]={1,0,-1,-1,-1,0,1,1};
	int dy[]={1,1,1,0,-1,-1,-1,0};
	void flood(int x,int y) {
		m[x][y]='0';
		LinkedList<Integer> q=new LinkedList<Integer>();
		q.add(x); q.add(y);
		while(!q.isEmpty()) {
			int atx=q.poll(),aty=q.poll();
			for(int d=0;d<8;d++) {
				int x2=atx+dx[d],y2=aty+dy[d];
				if(isthing(x2,y2)) {
					m[x2][y2]=0;
					q.add(x2); q.add(y2);
				}
			}
		}
	}
	void solve() {
		flowers=birds=0;
		if(r<2) return;
		// find flowers
		for(int i=0;i<c;i++) if(isthing(r-2,i)) {
			flood(r-2,i);
			flowers++;
		}
		// find birds: check each position for '/\/\' and check that it
		// isn't connected to anything else
		for(int i=0;i<r-2;i++) for(int j=0;j<c-3;j++) {
			boolean isbird=true;
			if(m[i][j]=='/' && m[i][j+1]=='\\' && m[i][j+2]=='/' && m[i][j+3]=='\\') {
				for(int k=-1;k<5;k++) if(!isnothing(i-1,j+k)) isbird=false;
				for(int k=-1;k<5;k++) if(!isnothing(i+1,j+k)) isbird=false;
				if(!isnothing(i,j-1)) isbird=false;
				if(!isnothing(i,j+4)) isbird=false;
				if(isbird) birds++;
			}
		}
	}
	void go() {
		Scanner in=new Scanner(System.in);
		int T=in.nextInt();
		while(T-->0) {
			r=in.nextInt();
			c=in.nextInt();
			m=new char[r][];
			for(int i=0;i<r;i++) m[i]=in.next().toCharArray();
			solve();
			System.out.printf("Flowers: %d\nBirds: %d\n",flowers,birds);
		}
	}
}
