#include <iostream>
#include <string>
#include <sstream>

using namespace std;

int main(void) {
	int T;
	cin >> T;
	cin.ignore();

	for (int t=0; t<T; t++) {
		string line;
		getline(cin, line);

		stringstream ss;
		ss << line;

		int count=0;
		string input;
		string last="";
		while (ss >> input) {
			if (input == "u")
				count+=10;
			else if (input=="ur")
				count+=10;
			else if (input.find("lol") < input.size())
				count+=10;
			else if ((last=="would" || last=="should") && input=="of")
				count+=10;
				
			last=input;
		}
		cout << count << endl;
	}
}