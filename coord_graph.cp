// takes in points from a csv file and graphs them in svg format
//
//
#include"Point.h"
#include<iostream>
#include<fstream>
#include<cstdio>
#include<cstdlib>
#include<string>
#include<sstream> 
#include<vector>
#include<algorithm>
using namespace std;

int main(void)
{
	ifstream myfile("coord_graph.csv");		// uses the given csv file as an example
	string line;
	vector<string> lines;
	vector<string> polyg;
	vector<Point> pts_temp;
	vector<Point> pts; 
	if (!myfile)
	{
		cout << "File not read, exiting now" << endl;
		exit(1);
	} else if (myfile.is_open()) {
			while (getline(myfile, line, '\"')) {		// reads each point in as a string
				if (line != ",")
				{	
					lines.push_back(line);	
				} else {
					continue;
				}	
		}
	}
	myfile.close();
	
	for (unsigned int i = 1; i < lines.size(); i++)
	{	
		Point p(lines[i]);			// point constructor
		vector<Point>::iterator iter = find(pts.begin(), pts.end(), p);	// if the point is already in points
		if (iter == pts.end()) // if point not in the primary vector of points
		{
			Point &pt = p;
			pts.push_back(p);
			pts_temp.push_back(p);	// store point in a temporary vector (construction of sev. shapes)
		} else {
			string shape(draw_polygon(pts_temp));
			string& shape_ = shape;		// saves polygon "description" 
			polyg.push_back(shape_);
			pts_temp.clear();	// vector of points used to draw shape is reset
			continue;
		}
	}
	draw_shape(polyg);	// generates svg file viewable in browser (with different shapes)
}

// x-y axis is flipped - upper-left corner is (0,0) and the y-axis from that point to lower-left corner is positive
