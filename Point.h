// Point.h 
// defines a point class
// 
#ifndef POINT_H
#define POINT_H
#include<iostream>
#include<string>
#include<vector>
class Point
{
	public:
		int x, y;
		Point(void);
		Point(int xin, int yin);
		Point(std::string s);
		int convert_x(std::string s);
		int convert_y(std::string s);
		bool operator==(const Point& rhs) const;
		friend std::ostream& operator<<(std::ostream& os, 
			const Point& p);
		friend std::string draw_polygon(std::vector<Point> const &pts);
		friend void draw_shape(std::vector<std::string> &polyg);
};

std::string draw_polygon(std::vector<Point> const &pts);
void draw_shape(std::vector<std::string> &polyg);

#endif
