#include "pch.h"
#include <iostream>
#include <memory>
#include <vector>
#include <algorithm>
#include <thread>
#include "Tests.h"
#include "Widget.h"
#include <chrono>
#include <set>


using namespace std;


void test_function();

void test_function()
{
	cout << "test_function called" << endl;
}


Tests::Tests(int i, int j)
{
	cout << "Ctr 2" << endl;
}

Tests::Tests(int i, int j, int k)
{
	cout << "Ctr 3" << endl;
}


void Tests::TestExplicitKeyword()
{
	Tests tester(1, 2);
	Tests testerb(1, 2, 3);
	Tests testerc{ 1,2 };
	Tests testerd{ 1,2,3 };
	Tests testere = { 1,2 };
	//Tests testerf = { 1,2,3 };
}


void Tests::TestAssignmentOperator()
{

	cout << "TestAssignmentOperator begin" << endl;
	vector<Widget> tools;
	for (int i = 0; i < 10; i++)
	{
		tools.push_back(Widget(i));
	}

	cout << "Test if widgets calls copy ctor or assignment operator now" << endl;
	for (Widget &t : tools)
	{
		Widget temp(10);
		temp = t;
	}

	cout << "TestAssignmentOperator end" << endl;
}

void Tests::TestForEachCopies()
{
	cout << "TestForEachCopies begin" << endl;
	vector<Widget> tools;
	for (int i = 0; i < 10; i++)
	{
		tools.push_back(Widget(i));
	}

	cout << "Test if any widgets get copied during for iteration" << endl;
	for (int i = 0; i < 10; i++)
	{
		Widget t = tools[i];
		cout << t.getId() << endl;
	}

	cout << "Test if widgets calls copy ctor now- using iterator" << endl;
	typedef vector<Widget> vwid;
	for (vwid::const_iterator iter = tools.cbegin(); iter != tools.cend(); ++iter)
	{
		cout << (*iter).getId() << endl;
	}
	
	cout << "Test if widgets calls copy ctor using dumb value range for" << endl;
	for (Widget t : tools)
	{
		cout << t.getId() << endl;
	}


	cout << "Test if widgets calls copy ctor now" << endl;
	for (Widget &t : tools)
	{
		cout << t.getId() << endl;
	}
	
	cout << "TestForEachCopies end" << endl;
}


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
	auto easycopy = move(easyfoo);

	// unique_ptrs cannot be copied, only moved


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
	cout << "added wrench" << endl;
	tools.push_back(ax);
	cout << "added ax" << endl;
	tools.push_back(Widget(20));
	cout << "added temp widget" << endl;

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


void Tests::TestNewThreadWithFunction()
{
	cout << "TestNewThreadWithFunction begin" << endl;
	thread test_thread(test_function);
	test_thread.join();
	cout << "TestNewThreadWithFunction end" << endl;
}



void Tests::TestNewThreadWithLambdaFunction()
{
	cout << "TestNewThreadWithLambdaFunction begin" << endl;
	thread test_thread([](int maxcount) {
		for (int i = 0; i < maxcount; i++)
		{
			cout << i << endl;
		}
	}, 8);
	test_thread.join();
	cout << "TestNewThreadWithLambdaFunction end" << endl;
}


void Tests::TestVectorPushback()
{
	cout << "TestVectorPushback begin" << endl;

	vector<Widget> tools;
	for (int i = 0; i < 10; i++)
	{
		cout << "adding to vector begin " << i << endl;
		tools.push_back(Widget(i));
		cout << "adding to vector end " << i << endl;
	}

	cout << "TestVectorPushback end" << endl;
}



void Tests::TestVectorOfSharedWidgetPointers()
{
	cout << "TestVectorOfSharedWidgetPointers begin" << endl;

	vector<shared_ptr<Widget>> tools;
	for (int i = 0; i < 10; i++)
	{
		cout << "adding to vector begin " << i << endl;
		tools.push_back(make_shared<Widget>(i));
		cout << "adding to vector end " << i << endl;
	}

	// is there a memory leak here?
	// or are 10 Widgets destroyed?

	cout << "10 Widgets should get destroyed after this point" << endl;
	cout << "TestVectorOfSharedWidgetPointers end" << endl;
}


void Tests::TestMoveConstructor()
{
	cout << "TestMoveConstructor begin" << endl;
	Widget w1(10);
	Widget w2(w1);		// this calls regular copy constructor
						// the original widget remains intact
	Widget w3(move(w1));	// this calls move contructor
							// the move ctr sets m1 contents to null 
							// this means the original widget is unusable

	cout << w2.getId() << endl;
	cout << w3.getId() << endl;
	cout << w1.getId() << endl;

	cout << w2.getContents(2) << endl;
	cout << w3.getContents(2) << endl;
	//cout << w1.getContents(2) << endl;	// this one blows up

	cout << "TestMoveConstructor end" << endl;

}


void Tests::TestClock()
{
	cout << "TestClock begin" << endl;

	using namespace std::chrono;

	high_resolution_clock::time_point t1 = high_resolution_clock::now();

	cout << "printing out 1000 stars...\n";
	for (int i = 0; i<1000; ++i) 
		cout << "*";
	cout << std::endl;

	high_resolution_clock::time_point t2 = high_resolution_clock::now();

	duration<double> time_span = duration_cast<duration<double>>(t2 - t1);
	cout << "It took me " << time_span.count()  << " sseconds.";
	cout << std::endl;


	cout << "TestClock end" << endl;
}


template <typename T>
T addTwoNumbers(T a, T b)
{
	return a + b;
}


void Tests::TestGenericFunction()
{
	cout << "TestGenericFunction begin" << endl;

	int a = addTwoNumbers(6, 7);
	cout << a << endl;

	double d = addTwoNumbers(7.0, 5.6);
	cout << d << endl;

	// the following does not work because there is no possible
	//  addTwoNumbers(int, double) function
	//int e = addTwoNumbers(7, 5.6);
	//cout << e << endl;

	cout << "TestGenericFunction end" << endl;
}



void Tests::TestSetInsertAndEmplace()
{
	cout << "TestSetInsertAndEmplace end" << endl;
	set<Widget> wset;
	wset.insert(Widget(10));
	auto status = wset.insert(Widget(20));
	cout << " Result: " << status.second << endl;
		
	cout << "Emplace with created widget" << endl;
	wset.emplace(Widget(30));

	cout << "Emplace with ctr parameters" << endl;
	wset.emplace(40);

	cout << "Looks like less copying and destroying temporary objects with emplace" << endl;

	cout << "Set size " << wset.size() << endl;
	for (auto &w : wset)
	{
		cout << w.getId() << endl;
	}
	

	cout << "TestSetInsertAndEmplace end" << endl;
}