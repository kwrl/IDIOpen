#include <iostream>
#include <string>
#include <cmath>

using namespace std;

int main(void) {
	int cases;
	cin >> cases;
	for (int c=0; c<cases; c++) {
		int X,Y; cin >> X >> Y; cin.ignore();
		for (int y=0; y<Y; y++) {
			string discard;
			getline(cin, discard);
		}
		if (X == 1) {
			cout << Y*2-2 << endl;
		}
		else if (Y == 1) {
			cout << X*2-2 << endl;
		}

		else if (X%2 != 0 && Y%2 != 0) {
			cout << X*Y+1 << endl;
		}

		else {
			cout << X*Y << endl;
		}
	}
	cout << "LOL" << endl;
}