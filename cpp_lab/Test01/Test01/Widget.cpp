#include "pch.h"
#include <iostream>
#include "Widget.h"

using namespace std;

Widget::Widget(int i) : _id(i)
{
	cout << "Widget ctor" << endl;
	pmemory = new int[widget_size];
	memset(pmemory, 88, sizeof(int)*widget_size);
}

Widget::~Widget()
{
	cout << "Widget dtor" << endl;
	delete pmemory;
}


Widget::Widget(const Widget &other)
{
	cout << "Widget copy ctor" << endl;
	_id = other._id;
	pmemory = new int[widget_size];
	memcpy(pmemory, other.pmemory, sizeof(int)*widget_size);
}


Widget &Widget::operator=(const Widget &other)
{
	cout << "Widget assignment optr" << endl;
	if (this == &other)
		return *this;

	_id = other._id;
	pmemory = new int[widget_size];
	memcpy(pmemory, other.pmemory, sizeof(int)*widget_size);
	return *this;
}


Widget::Widget(Widget &&other) :
	_id(other._id),
	pmemory(other.pmemory)
{
	cout << "Widget move ctor" << endl;
	other.pmemory = nullptr;
}


Widget& Widget::operator=(Widget &&other)
{
	cout << "Widget move optr" << endl;
	if (this == &other)
		return *this;

	_id = other._id;
	pmemory = other.pmemory;
	other.pmemory = nullptr;
	return *this;
}


bool Widget::operator==(const Widget &other) const
{
	bool result = false;
	if (this->_id == other._id)
		result = true;
	return result;
}


bool Widget::operator<(const Widget &other) const
{
	bool result = false;
	if (this->_id > other._id)
		result = true;
	return result;
}


int Widget::getId() const
{
	return _id;
}

