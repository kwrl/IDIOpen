#include <iostream>

using namespace std;

int main(void) {
	int cases;
	cin >> cases;
	for (int c=0; c<cases; c++) {
		int M;
		cin >> M;
		int people_start=0;
		int people_now=0;
		for (int m=0; m<M; m++) {
			int people_in;
			cin >> people_in;
			people_now += people_in;

			int people_out;
			cin >> people_out;
			people_now -= people_out;

			if (people_now < 0) {
				people_start += -people_now;
				people_now=0;
			}

		}
		cout << people_start << endl;
	}
}