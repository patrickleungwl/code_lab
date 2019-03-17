#include "pch.h"
#include <iostream>
#include <memory>
#include <vector>
#include <algorithm>
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
	for (int i=0; i<10; i++)
	{
		tools.push_back(new Widget(i));
	}

	// Does this work?  Is there a memory leak here?

	// Vector of pointers is a bad idea because
	// you never know when the memory pointed to by a
	// pointer has been deleted or not.
	//
	// Should try a vector of smart pointers.

	cout << "Any Widgets get destroyed after this point?" << endl;
	cout << "TestVectorOfWidgetPointers end" << endl;
}


void Tests::TestVectorOfSharedWidgetPointers()
{
	cout << "TestVectorOfSharedWidgetPointers begin" << endl;
	
	vector<shared_ptr<Widget>> tools;
	for (int i = 0; i < 10; i++)
	{
		tools.push_back(make_shared<Widget>(i));
	}

	// is there a memory leak here?
	// or are 10 Widgets destroyed?

	cout << "10 Widgets should get destroyed after this point" << endl;
	cout << "TestVectorOfSharedWidgetPointers end" << endl;	
}


vector<shared_ptr<Widget>> Tests::GetVectorOfSharedWidgetPointers()
{
	cout << "GetVectorOfSharedWidgetPointers begin" << endl;

	vector<shared_ptr<Widget>> tools;
	for (int i = 0; i < 10; i++)
	{
		tools.push_back(make_shared<Widget>(i));
	}
	cout << "GetVectorOfSharedWidgetPointers end" << endl;

	return tools;
}


void Tests::TestVectorIteration()
{
	cout << "TestVectorIteration begin" << endl;

	vector<shared_ptr<Widget>> tools = GetVectorOfSharedWidgetPointers();
	for (vector<shared_ptr<Widget>>::iterator iter = tools.begin(); iter != tools.end(); iter++)
	{
		shared_ptr<Widget> tmp = *iter;
		cout << tmp->getId() << endl;
	}

	// is there a memory leak here?
	// or are 10 Widgets destroyed?

	cout << "TestVectorIteration end" << endl;
}


void Tests::TestLambdaOnVector()
{
	cout << "TestLambdaOnVector begin" << endl;

	vector<shared_ptr<Widget>> tools = GetVectorOfSharedWidgetPointers();
	for_each(tools.begin(), tools.end(),
		[](shared_ptr<Widget> w) { cout << w->getId() << endl; });

	// is there a memory leak here?
	// or are 10 Widgets destroyed?

	cout << "TestLambdaOnVector end" << endl;
}




void Tests::TestAlgoFindOnVector()
{
	cout << "TestAlgoFindOnVector begin" << endl;

	vector<shared_ptr<Widget>> tools = GetVectorOfSharedWidgetPointers();
	vector<shared_ptr<Widget>>::iterator witer = find_if(
		tools.begin(), 
		tools.end(), 
		[&](shared_ptr<Widget> const& w) {
			return w->getId() == 5;
		}
	);

	// found or not?
	if (witer != tools.end())
	{
		shared_ptr<Widget> tmp = *witer;
		cout << "Found " << tmp->getId() << endl;
	}

	cout << "TestAlgoFindOnVector end" << endl;
}



void Tests::TestAlgoMakeHeapOnVector()
{
	cout << "TestAlgoMakeHeapOnVector begin" << endl;
	vector<shared_ptr<Widget>> tools = GetVectorOfSharedWidgetPointers();

	cout << "Regular iteration" << endl;
	for_each(tools.begin(), tools.end(),
		[](shared_ptr<Widget> w) { cout << w->getId() << endl; });

	make_heap(tools.begin(), tools.end());
	while (!tools.empty())
	{
		// what is topmost?
		shared_ptr <Widget> tmp = tools.front();
		cout << "Front: " << tmp->getId() << endl;

		// pop_heap moves the topmost node to back
		pop_heap(tools.begin(), tools.end());

		// remove the last item
		tools.pop_back();
	}

	cout << "TestAlgoMakeHeapOnVector end" << endl;
}



void Tests::TestAlgoMakeHeapOnVectorOfInts()
{
	cout << "TestAlgoMakeHeapOnVectorOfInts begin" << endl;

	vector<int> tools;
	for (int i = 0; i < 10; i++)
	{
		tools.push_back(i);
	}
	cout << "Regular iteration" << endl;
	for_each(tools.begin(), tools.end(),
		[](int j) { cout << j << endl; });

	make_heap(tools.begin(), tools.end());
	while (!tools.empty())
	{
		// what is topmost?
		int j = tools.front();
		cout << "Front: " << j << endl;

		// pop_heap moves the topmost node to back
		pop_heap(tools.begin(), tools.end());

		// remove the last item
		tools.pop_back();
	}

	cout << "TestAlgoMakeHeapOnVectorOfInts end" << endl;
}


void Tests::TestAlgoMakeHeapOnVectorOfWidgets()
{
	cout << "TestAlgoMakeHeapOnVectorOfWidgets begin" << endl;
	vector<Widget> tools;
	for (int i = 0; i < 10; i++)
	{
		tools.push_back(Widget(i));
	}
	(tools[2] < tools[3]) ?
		cout << "Comparison works" << endl :
		cout << "Comparison failed" << endl;

	cout << "Regular iteration" << endl;
	for_each(tools.begin(), tools.end(),
		[](Widget w) { cout << w.getId() << endl; });

	make_heap(tools.begin(), tools.end());
	while (!tools.empty())
	{
		// what is topmost?
		Widget tmp = tools.front();
		cout << "Front: " << tmp.getId() << endl;

		// pop_heap moves the topmost node to back
		pop_heap(tools.begin(), tools.end());

		// remove the last item
		tools.pop_back();
	}
	cout << "TestAlgoMakeHeapOnVectorOfWidgets end" << endl;
}