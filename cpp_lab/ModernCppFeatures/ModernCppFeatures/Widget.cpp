#include <iostream>
#include "Widget.h"

using namespace std;

Widget::Widget(int i) : _id(i)
{
	++widgetCount;
	pmemory = new int[widget_size];
	memset(pmemory, 88, sizeof(int)*widget_size);
}

Widget::~Widget()
{
	--widgetCount;
	delete pmemory;
}

/*
Widget::Widget(Widget& other)
{
	++copyConstructorCount;
	cout << "Widget copy ctor" << endl;
	_id = other._id;
	pmemory = new int[widget_size];
	memcpy(pmemory, other.pmemory, sizeof(int) * widget_size);
}
*/


Widget::Widget(const Widget &other)
{
	++widgetCount;
	++copyConstructorCount;
	//cout << "Widget const copy ctor" << endl;
	_id = other._id;
	pmemory = new int[widget_size];
	memcpy(pmemory, other.pmemory, sizeof(int)*widget_size);
}


Widget &Widget::operator=(const Widget &other)
{
	++assignmentCount;
	if (this == &other)
		return *this;

	_id = other._id;
	pmemory = new int[widget_size];
	memcpy(pmemory, other.pmemory, sizeof(int)*widget_size);
	return *this;
}


Widget::Widget(Widget &&other) noexcept :
	_id(other._id),
	pmemory(other.pmemory) 
{
	++widgetCount;
	++moveConstructorCount;
	//cout << "Widget move ctor" << endl;
	other.pmemory = nullptr;
}


Widget& Widget::operator=(Widget &&other) noexcept
{
	cout << "Widget move optr" << endl;
	if (this == &other)
		return *this;

	_id = other._id;
	pmemory = other.pmemory;
	other.pmemory = nullptr;
	return *this;
}


// used by find

bool Widget::operator==(const Widget &other) const
{
	bool result = false;
	if (this->_id == other._id)
		result = true;
	return result;
}


// used for sorting by set container

bool Widget::operator<(const Widget &other) const
{
	bool result = false;
	if (this->_id < other._id)
		result = true;
	return result;
}


int Widget::getId() const
{
	return _id;
}


int Widget::getContents(int memId) const
{
	return pmemory[memId];
}