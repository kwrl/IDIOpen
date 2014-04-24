#include <iostream>
#include <string>
#include <vector>
#include <stack>
#include <cmath>

using namespace std;

bool fpart(char c) {
	return c == '\\' || c == '|' || c == '/' || c == '@' || c == '-';
}

bool out_of_bounds(int x, int y, int X, int Y) {
	return x < 0 || y < 0 || x >= X || y >= Y;
}

int main(void) {
	int cases; cin >> cases; cin.ignore();

	for (int m=0; m<cases; m++)	{
		int X,Y;
		cin >> Y >> X; cin.ignore(); 

		vector<string> grid;
		for (int y=0; y<Y; y++) {
			string input;
			getline(cin, input);
			grid.push_back(input);
		}

		if (Y == 1) {
			cout << "Flowers: 0" << endl;
			cout << "Birds: 0" << endl;
			continue;
		}

		int flowers=0;

		for (int x=0; x<X; x++) {
			char ch = grid.at(Y-2).at(x);
			if (!fpart(ch)) continue;

			flowers++;

			stack<int> stack_x,stack_y;
			stack_y.push(Y-2);
			stack_x.push(x);

			while (!stack_x.empty() && !stack_y.empty()) {
				int x = stack_x.top();	stack_x.pop();
				int y = stack_y.top();	stack_y.pop();

				if (out_of_bounds(x,y,X,Y)) continue;

				char c = grid.at(y).at(x);

				if (!fpart(c)) continue;

				stack_x.push(x-1); stack_y.push(y); // left
				stack_x.push(x+1); stack_y.push(y); // right
				stack_x.push(x+1); stack_y.push(y-1); // right top diagonal
				stack_x.push(x-1); stack_y.push(y-1); // left top diagonal
				stack_x.push(x+1); stack_y.push(y+1); // right bottom diagonal
				stack_x.push(x-1); stack_y.push(y+1); // left bottom diagonal
				stack_x.push(x); stack_y.push(y-1); // top
				stack_x.push(x); stack_y.push(y+1); // bottom

				grid[y][x] = 'X'; // ate it
			}
		}

		int birds=0;
		string bird = "/\\/\\";
		int bird_length = bird.size();

		for (int y=0; y<Y-1; y++) {
			int bird_pos = grid[y].find(bird);
			while (bird_pos!=string::npos) {
				int parts=0;

				for (int yy=y-1; yy<y+1; yy++) {
					for (int xx=bird_pos-1; xx<bird_pos+bird_length+1; xx++) {
						if (out_of_bounds(xx,yy,X,Y)) continue;

						if (fpart(grid.at(yy).at(xx))) {
							parts++;
						}
					}
				}
				if (parts == 4) {
					birds++;
				}
				bird_pos = grid.at(y).find(bird, bird_pos+1);
			}
		}

		cout << "Flowers: " << flowers << endl;
		cout << "Birds: " << birds << endl;

#if 0
		for (int y=0; y<Y; y++) {
			for (int x=0; x<X; x++) {
				cout << grid[y][x];
			}
			cout << endl;
		}
#endif

	}
}