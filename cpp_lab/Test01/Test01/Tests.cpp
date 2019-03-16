#include "pch.h"
#include <iostream>
#include <memory>
#include <vector>
#include "Tests.h"
#include "Widget.h"

using namespace std;

void Tests::TestUniquePtr()
{
	cout << "TestUniquePtr begin" << endl;

	/*

	A unique_ptr is a wrapper around a raw pointer. 
	We can initialise a unique_ptr by either 
	- wrapping a raw pointer  or by
	- using make_unique utility

	*/

	std::unique_ptr<Widget> foo(new Widget(10));
	std::unique_ptr<Widget> bar = make_unique<Widget>(20);

	cout << foo->getId() << endl;
	cout << bar->getId() << endl;

	// We can also use auto to make code more readable

	auto easyfoo = std::make_unique<Widget>(9);

	// All widgets should get destroyed at end of this scope
	cout << "There should be 3 Widget destructor calls after this" << endl;
	cout << "TestUniquePtr end" << endl;

}


void Tests::TestVectorContainerUsage()
{
	cout << "TestVectorContainerUsage begin" << endl;

	Widget wrench(100);
	Widget ax(50);

	cout << "adding to tools" << endl;
	vector<Widget> tools;
	tools.push_back(wrench);
	tools.push_back(ax);
	tools.push_back(Widget(20));

	cout << "TestVectorContainerUsage end" << endl;
}



void Tests::TestVectorOfWidgetPointers()
{
	cout << "TestVectorOfWidgetPointers begin" << endl;

	vector<Widget *> tools;
	for (int i=0; i<10000; i++)
	{
		tools.push_back(new Widget(i));
	}

	// Does this work?  Is there a memory leak here?

	cout << "TestVectorOfWidgetPointers end" << endl;
}