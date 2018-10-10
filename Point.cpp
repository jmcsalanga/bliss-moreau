// Point.cpp
// implements a point class
//
#include"Point.h"
#include<cstdio>
#include<sstream>
#include<vector>
#include<string>
#include<iostream>
using namespace std;

Point::Point(void):x(0), y(0) {}

Point::Point(int xin, int yin): x(xin), y(yin) {}

Point::Point(string s): x(convert_x(s)), y(convert_y(s)) {}

int Point::convert_x(string s) 
{
	char open_paren;	
	int x_;
	stringstream read(s);
	read >> open_paren >> x_;
	return x_;
}

int Point::convert_y(string s)
{
	char open_paren, comma, end_paren;
	int x_, y_;
	stringstream read(s);
	read >> open_paren >> x_ >> comma >> y_ >> end_paren;
	return y_;
}

bool Point::operator==(const Point& rhs) const
{
	if (x == rhs.x && y == rhs.y) 
	{
		return true;
	} else {
		return false;
	}
}
	
ostream& operator<<(ostream& os, const Point& p)
{
	os << "(" << p.x << "," << p.y << ")";
	return os;
}

string draw_polygon(vector<Point> const &pts)
{
	string polyg = "<polygon fill=\"yellow\" fill-opacity=\"0.4\" stroke=\"black\" stroke-width=\"0.2\" points=\"";
	for (unsigned int i = 0; i < pts.size(); i++)
	{ 
		std::ostringstream stm, stm_;
		stm << pts[i].x;
		stm_ << pts[i].y;
		string s = stm.str() + string(",") + stm_.str() + string(" ");
		polyg = polyg + s;
	}
	string end = "\" />";
	polyg = polyg + end;
	return polyg;
}

void draw_shape(vector<string> &polyg)
{
	cout << "<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"no\"?>" << endl;
        cout << "<svg width=\"600\" height=\"600\"" << endl;
	cout << "viewBox=\"0 0 25 25\" preserveAspectRatio=\"none\"" << endl;
        cout << "xmlns=\"http://www.w3.org/2000/svg\">" << endl;
        cout << "fill=\"white\" fill-opacity=\"0.5\" stroke=\"black\" stroke-width=\"0.5\">" << endl;
        cout << "<rect fill=\"lightgrey\" x=\"0\" y=\"0\" width=\"25\" height=\"25\"/>" << endl;
	for (unsigned int j = 0; j < polyg.size(); j++)
	{
		cout << polyg[j] << endl;
	}
	cout << "</svg>" << endl;
}	
