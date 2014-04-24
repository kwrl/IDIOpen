#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;

int main(void) {
	int cases, workload, n_minions; 
	cin >> cases;

	for (int case_n=0; case_n<cases; case_n++) {
		cin >> workload;
		cin >> n_minions;
		cin.ignore();
		vector<int> minions(n_minions);
		for (int i=0; i<n_minions; i++) {
			cin >> minions[i];
		}

		sort(minions.begin(), minions.end());
		reverse(minions.begin(), minions.end());
		int workload_sum=0;
		int minions_needed=-1;
		for (int m=0; m<n_minions; m++) {
			workload_sum += minions[m];
			if (workload_sum >= workload) {
				minions_needed=m+1;
				break;
			}
		}
		if (minions_needed > 0) {
			cout << minions_needed << endl;
		}
		else {
			cout << "no rest for Ruben" << endl;
		}
	}

	
	return 0;
}
