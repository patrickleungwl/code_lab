#include "pch.h"
#include <iostream>
#include <memory>
#include <vector>
#include <algorithm>
#include <thread>
#include <chrono>
#include <set>
#include "Tests.h"
#include "Widget.h"
#include <assert.h>

using namespace std::chrono;

// set Widget global count to 0
int Widget::widgetCount = 0;
int Widget::assignmentCount = 0;
int Widget::copyConstructorCount = 0;
int Widget::moveConstructorCount = 0;

void test_function();

void test_function()
{
	std::cout << "test_function called" << std::endl;
}


Tests::Tests(int i, int j) : _constructorMethod{ 2 }
{
}

Tests::Tests(int i, int j, int k) : _constructorMethod { 3 }
{
}


void Tests::ResetMemoryState()
{
	Widget::widgetCount = 0;
	Widget::assignmentCount = 0;
	Widget::copyConstructorCount = 0;
	Widget::moveConstructorCount = 0;
}



// AssertNoLeakyMemory
//

void Tests::AssertNoLeakyMemory()
{
	assert(Widget::widgetCount == 0);
}


// AssertLeakyMemory
//

void Tests::AssertLeakyMemory()
{
	assert(Widget::widgetCount > 0);
}


// AssertAssignmentUsed
//

void Tests::AssertAssignmentUsed(int expectedAssignmentsUsed)
{
	assert(Widget::assignmentCount == expectedAssignmentsUsed);
}


// AssertCopyConstructorUsed
//

void Tests::AssertCopyConstructorUsed(int expectedCopyConstructorsUsed)
{
	assert(Widget::copyConstructorCount == expectedCopyConstructorsUsed);
}


// AssertMoveConstructorUsed
//

void Tests::AssertMoveConstructorUsed(int expectedMoveConstructorsUsed)
{
	assert(Widget::moveConstructorCount == expectedMoveConstructorsUsed);
}



// AssertMoveConstructorUsedGreaterThan
//

void Tests::AssertMoveConstructorUsedGreaterThan(int expectedMoveConstructorsUsed)
{
	assert(Widget::moveConstructorCount > expectedMoveConstructorsUsed);
}



// Test_ExplicitConstructor_ExpectOnlyExactParameterMatch
// 
// The Tests class has two constructors, 
//	one with two paramters and
//  one with three parameters.
// The constructor with three parameters contains an explicit keyword
// so we do expect it to work with only explicit constructor.
//
// Tests(int i, int j);
// explicit Tests(int i, int j, int k);
//

void Tests::Test_ExplicitConstructor_ExpectOnlyExactParameterMatch()
{
	// This is calling the first constructor explicitly
	Tests tester1(1, 2);
	assert(tester1.GetConstructorMethod() == 2);
	
	// This is calling the second constructor explicitly
	Tests tester2(1, 2, 3);
	assert(tester2.GetConstructorMethod() == 3);

	// This is calling the first constructor explicitly using new initializer
	Tests tester3{ 1,2 };
	assert(tester3.GetConstructorMethod() == 2);

	// This is calling the second constructor explicitly using new initializer
	Tests tester4{ 1,2,3 };
	assert(tester4.GetConstructorMethod() == 3);

	// This is calling the first constructor implicitly
	Tests tester5 = { 1,2 };
	assert(tester5.GetConstructorMethod() == 2);

	// This is calling the secondconstructor implicitly and does not work
	// Tests tester6 = { 1,2,3 };
}


void Tests::Test_MoveOperator_ExpectMoveOperatorUsed()
{
	ResetMemoryState();
	{
		Widget foo(10);
		Widget bar(foo);
		AssertCopyConstructorUsed(1);
		AssertMoveConstructorUsed(0);
	}

	ResetMemoryState();
	{
		Widget foo(10);
		Widget bar(std::move(foo));  

		// std::move transforms named variable into a rvalue
		// this forces the compiler to look for a move constructor
		//
		// This is fast!  No new memory allocation when creating
		// bar.  But what happened to the memory in the original 
		// object foo? 
		AssertCopyConstructorUsed(0);
		AssertMoveConstructorUsed(1);
	}
}



// Test_MoveUniquePtr_ExpectOriginalPtrBecomesNull
//
//	A unique_ptr is a smart pointer that owns and managers
//	another object through a pointer and disposes of that object when
//	the unique_ptr goes out of scope.
//
//	We can initialise a unique_ptr by either
//	- wrapping a raw pointer  or by
//	- using make_unique utility

void Tests::Test_MoveUniquePtr_ExpectOriginalPtrBecomesNull()
{
	ResetMemoryState();

	{
		std::unique_ptr<Widget> foo(new Widget(10));
		std::unique_ptr<Widget> bar = make_unique<Widget>(20);

		assert(foo->getId() == 10);
		assert(bar->getId() == 20);

		// We can also use auto to make code more readable
		auto widget1 = std::make_unique<Widget>(9);

		// unique_ptrs cannot be copied, only moved.
		// There is only one single owner of a unique_ptr.
		// Once ownership moved between owners, the original owner 
		// is null.

		auto widget2 = move(widget1);
		assert(widget2->getId() == 9);
		assert(widget1 == nullptr);

		// All widgets should get destroyed at end of this scope
	}	

	AssertNoLeakyMemory();
}


// Test_VectorOfRawPointers_ExpectMemoryLeak
// 
// Using raw pointers is usually a bad idea because
// we have to ensure their memory allocations get cleaned up.
//

void Tests::Test_VectorOfRawPointers_ExpectMemoryLeak()
{
	ResetMemoryState();
	{
		vector<Widget*> tools;
		for (int i = 0; i < 10; i++)
		{
			tools.push_back(new Widget(i));
		}
		// This is a memory leak.
	}
	AssertLeakyMemory();
}


std::vector<int> Tests::GetVectorOfInts()
{
	std::vector<int> vec;
	for (int i = 0; i < 10; i++)
	{
		vec.push_back(i);
	}
	return vec;
}


// GetVectorOfWidgetUniquePointers
//
//

std::vector<std::unique_ptr<Widget>> Tests::GetVectorOfWidgetUniquePointers()
{
	std::vector<std::unique_ptr<Widget>> tools;
	for (int i = 0; i < 10; i++)
	{
		tools.push_back(make_unique<Widget>(i));
	}
	return tools;
}



// GetVectorOfWidgetSharedPointers
//
//	Initialize a vector of 10 shared pointers of widgets
//

std::vector<std::shared_ptr<Widget>> Tests::GetVectorOfWidgetSharedPointers()
{
	std::vector<std::shared_ptr<Widget>> tools;
	for (int i = 0; i < 10; i++)
	{
		tools.push_back(std::make_shared<Widget>(i));
	}
	return tools;
}


// GetMapOfWidgetSharedPointers
//
// Initialise a map of 10 integers to unique pointers
//

std::map<int, std::shared_ptr<Widget>> Tests::GetMapOfWidgetSharedPointers()
{
	std::map<int, std::shared_ptr<Widget>> tmpDict;
	for (int i = 0; i < 10; i++)
	{
		tmpDict[i] = std::make_shared<Widget>(i);
	}
	return tmpDict;
}



// Test_VectorOfSharedPointers_ExpectNoMemoryLeak
//
//   Initialise a vector of 10 shared ptrs of widgets
//	 Assert that all shared ptrs are valid
//

void Tests::Test_VectorOfSharedPointers_ExpectNoMemoryLeak()
{
	ResetMemoryState();
	{
		auto tools = GetVectorOfWidgetSharedPointers();
		int i = 0;
		for (auto iter = tools.begin(); iter != tools.end(); iter++)
		{
			auto tmp = *iter;
			assert(tmp->getId() == i++);
		}
	}
	AssertNoLeakyMemory();
}


// Test_VectorOfUniquePointers_ExpectNoMemoryLeak
//
//   Initialise a vector of 10 unique ptrs of widgets
//	 Assert that all unique ptrs are valid
//

void Tests::Test_VectorOfUniquePointers_ExpectNoMemoryLeak()
{
	ResetMemoryState();
	{
		auto tools = GetVectorOfWidgetUniquePointers();
		int i = 0;
		for (auto iter = tools.begin(); iter != tools.end(); iter++)
		{
			// Cannot assign unique_ptr iterator to something else
			// otherwise, the original iterator gets wiped
			// auto tmp = *iter;

			assert((*iter)->getId() == i++);
		}
	}
	AssertNoLeakyMemory();
}


// Test_SetObject_ExpectAssignmentOperatorUsed
//

void Tests::Test_SetObject_ExpectAssignmentOperatorUsed()
{
	ResetMemoryState();
	{
		Widget foo(10);
		Widget bar(20);

		// This uses the assignment operator
		foo = bar;

		assert(foo.getId() == 20);
		assert(bar.getId() == 20);
	}
	AssertNoLeakyMemory();
	AssertAssignmentUsed(1);
	AssertCopyConstructorUsed(0);
}


// Test_ContainerPushBackWithMemoryPreallocation_ExpectCopyConstructorUsed
//
// When copying an object into a container, the object has a name- and so it is
// a lvalue, not an rvalue, and so the copy operation uses a regular copy constructor
// when copying into a container.
//

void Tests::Test_ContainerPushBackWithMemoryPreallocation_ExpectCopyConstructorUsed()
{
	ResetMemoryState();
	{
		vector<Widget> tools;

		high_resolution_clock::time_point t1 = high_resolution_clock::now();
		tools.reserve(10000);
		for (int i = 0; i < 1000; i++)
		{
			Widget r(i);
			tools.push_back(r);
		}
		high_resolution_clock::time_point t2 = high_resolution_clock::now();

		duration<double> testTimeSpan = duration_cast<duration<double>>(t2 - t1);
		std::cout << "TestCopyConstructorWithContainerPreallocation: ";
		std::cout << testTimeSpan.count() << " seconds." << std::endl;
	}
	AssertNoLeakyMemory();
	AssertCopyConstructorUsed(1000);
}


// Test_ContainerPushBackWithNoMemoryPreallocation_ExpectCopyConstructorUsed
//
// When copying an object into a container, the object has a name- and so it is
// a lvalue, not an rvalue, and so the copy operation uses a regular copy constructor
// when copying into a container.
//

void Tests::Test_ContainerPushBackWithNoMemoryPreallocation_ExpectCopyConstructorUsed()
{
	ResetMemoryState();
	{
		vector<Widget> tools;

		high_resolution_clock::time_point t1 = high_resolution_clock::now();
		for (int i = 0; i < 1000; i++)
		{
			Widget r(i);
			tools.push_back(r);
		}
		high_resolution_clock::time_point t2 = high_resolution_clock::now();

		duration<double> testTimeSpan = duration_cast<duration<double>>(t2 - t1);
		std::cout << "TestCopyConstructorWithNoContainerPreallocation: ";
		std::cout << testTimeSpan.count() << " seconds." << std::endl;
	}
	AssertNoLeakyMemory();
	AssertCopyConstructorUsed(1000);
}


// Test_ContainerMovePushBackWithMemoryPreallocation_ExpectMoveConstructorUsed
//
// When copying an object into a container, the object is a temporary, has no name
// and is an rvalue.  This copy operation uses a move constructor
// when copying into a container.
//
// The container's memory preallocation cuts down on the amount of thrashing
// when adding new container members.
//

void Tests::Test_ContainerMovePushBackWithMemoryPreallocation_ExpectMoveConstructorUsed()
{
	ResetMemoryState();
	{
		vector<Widget> tools;

		high_resolution_clock::time_point t1 = high_resolution_clock::now();
		tools.reserve(10000);
		for (int i = 0; i < 1000; i++)
		{
			tools.push_back(Widget(i));
		}
		high_resolution_clock::time_point t2 = high_resolution_clock::now();

		duration<double> testTimeSpan = duration_cast<duration<double>>(t2 - t1);
		std::cout << "TestMoveConstructorWithContainerPreallocation: ";
		std::cout << testTimeSpan.count() << " seconds." << std::endl;
	}
	AssertNoLeakyMemory();
	AssertCopyConstructorUsed(0);
	AssertMoveConstructorUsed(1000);
}


// Test_ContainerMovePushBackWithNoMemoryPreallocation_ExpectMoveConstructorUsed
//
// When copying an object into a container, the object is a temporary, has no name
// and is an rvalue.  This copy operation uses a move constructor
// when copying into a container.
//

void Tests::Test_ContainerMovePushBackWithNoMemoryPreallocation_ExpectMoveConstructorUsed()
{
	ResetMemoryState();
	{
		vector<Widget> tools;

		high_resolution_clock::time_point t1 = high_resolution_clock::now();
		for (int i = 0; i < 1000; i++)
		{
			tools.push_back(Widget(i));
		}
		high_resolution_clock::time_point t2 = high_resolution_clock::now();

		duration<double> testTimeSpan = duration_cast<duration<double>>(t2 - t1);
		std::cout << "TestMoveConstructorWithNoContainerPreallocation: ";
		std::cout << testTimeSpan.count() << " seconds." << std::endl;
	}
	AssertNoLeakyMemory();
	AssertCopyConstructorUsed(0);
	AssertMoveConstructorUsedGreaterThan(3000);
	// container makes additional moves because of container memory reallocation
}


// Test_ContainerOfSmartPointers_ExpectSimpleObjectConstruction
//
// The container of smart pointers just - add in copies of the smart pointer.
// The widgets get constructed simply once- via copy construction.
// 
// So the compiled program never calls the Widget objects' copy or move constructors.
//

void Tests::Test_ContainerOfSmartPointers_ExpectSimpleObjectConstruction()
{
	ResetMemoryState();
	{
		std::vector<std::shared_ptr<Widget>> tools;
		for (int i = 0; i < 10; i++)
		{
			tools.push_back(std::make_shared<Widget>(i));
		}
	}
	AssertNoLeakyMemory();
	AssertCopyConstructorUsed(0);
	AssertMoveConstructorUsed(0);
}


// Test_VectorForEachAlgorithmWithNamedLambda_ExpectIterationToWork
// 
// Example of lambda usage on a vector of widgets
// We also explore getting a copy of the widget smart ptr by reference
// or by value (copy).  But since they are both copies of the widget ptr, 
// there is no performance difference- in this case.
//

void Tests::Test_VectorForEachAlgorithmWithNamedLambda_ExpectIterationToWork()
{
	auto widgetsVec = GetVectorOfWidgetSharedPointers();

	auto updateWidgetPtrByRefInVec = [](std::shared_ptr<Widget> const &w) { 
		w->updateId(w->getId() + 10); 
	};

	auto updateWidgetPtrByCopyInVec = [](std::shared_ptr<Widget> const w) {
		w->updateId(w->getId() - 10);
	};

	for_each(widgetsVec.begin(), widgetsVec.end(), updateWidgetPtrByRefInVec);
	for_each(widgetsVec.begin(), widgetsVec.end(), updateWidgetPtrByCopyInVec);

	int i = 0;
	for (auto w : widgetsVec) {
		assert(w->getId() == i);
		++i;
	}
}



// Test_MapForEachAlgorithmWithNamedLambda_ExpectIterationToWork
// 
// Example of lambda usage on a map of widgets
//

void Tests::Test_MapForEachAlgorithmWithNamedLambda_ExpectIterationToWork()
{
	auto widgetsMap = GetMapOfWidgetSharedPointers();

	auto checkWidgetInMap = [](std::pair<int, std::shared_ptr<Widget>> w) {
		auto val = w.second; val->updateId(val->getId() + 10); };

	for_each(widgetsMap.begin(), widgetsMap.end(), checkWidgetInMap);

	int i = 0;
	for (auto w : widgetsMap) {
		assert(w.second->getId() == (i + 10));
		++i;
	}
}


// Test_VectorForIfAlgorithmWithAnonLambda_ExpectToFindItem
//

void Tests::Test_VectorForIfAlgorithmWithAnonLambda_ExpectToFindItem()
{
	auto widgetsVec = GetVectorOfWidgetSharedPointers();

	auto witer = find_if(
		widgetsVec.begin(),
		widgetsVec.end(),
		[](shared_ptr<Widget> const& w) {
			return w->getId() == 5;
		}
	);

	// found or not?
	assert(witer != widgetsVec.end());
	assert((*witer)->getId() == 5);
}


// Test_MakeHeapAlgorithm_ExpectMaxNodeAtRoot
// 
// Transforms a vector of integers into a 
// heap of integers. 
//
// A heap is a loosely ordered tree structure- 
// where each node has smaller left and right nodes.  
//

void Tests::Test_MakeHeapAlgorithm_ExpectMaxNodeAtRoot()
{
	auto vec = GetVectorOfInts();

	// get max value from vector
	auto maxItem = std::max_element(vec.begin(), vec.end());
	int maxValue = *maxItem;

	// make a heap out of vector
	std::make_heap(vec.begin(), vec.end());

	// ensure front of vector contains the item with max value
	int frontItem = vec.front();
	assert(frontItem == maxValue);
}





void Tests::TestNewThreadWithFunction()
{
	std::cout << "TestNewThreadWithFunction begin" << std::endl;
	thread test_thread(test_function);
	test_thread.join();
	std::cout << "TestNewThreadWithFunction end" << std::endl;
}



void Tests::TestNewThreadWithLambdaFunction()
{
	std::cout << "TestNewThreadWithLambdaFunction begin" << std::endl;
	thread test_thread([](int maxcount) {
		for (int i = 0; i < maxcount; i++)
		{
			std::cout << i << std::endl;
		}
	}, 8);
	test_thread.join();
	std::cout << "TestNewThreadWithLambdaFunction end" << std::endl;
}


void Tests::TestMoveConstructor()
{
	std::cout << "TestMoveConstructor begin" << std::endl;
	Widget w1(10);
	Widget w2(w1);		// this calls regular copy constructor
						// the original widget remains intact
	Widget w3(move(w1));	// this calls move contructor
							// the move ctr sets m1 contents to null 
							// this means the original widget is unusable

	std::cout << w2.getId() << std::endl;
	std::cout << w3.getId() << std::endl;
	std::cout << w1.getId() << std::endl;

	std::cout << w2.getContents(2) << std::endl;
	std::cout << w3.getContents(2) << std::endl;
	//std::cout << w1.getContents(2) << std::endl;	// this one blows up

	std::cout << "TestMoveConstructor end" << std::endl;

}



template <typename T>
T addTwoNumbers(T a, T b)
{
	return a + b;
}


void Tests::TestGenericFunction()
{
	std::cout << "TestGenericFunction begin" << std::endl;

	int a = addTwoNumbers(6, 7);
	std::cout << a << std::endl;

	double d = addTwoNumbers(7.0, 5.6);
	std::cout << d << std::endl;

	// the following does not work because there is no possible
	//  addTwoNumbers(int, double) function
	//int e = addTwoNumbers(7, 5.6);
	//std::cout << e << std::endl;

	std::cout << "TestGenericFunction end" << std::endl;
}



void Tests::TestSetInsertAndEmplace()
{
	std::cout << "TestSetInsertAndEmplace end" << std::endl;
	set<Widget> wset;
	wset.insert(Widget(10));
	auto status = wset.insert(Widget(20));
	std::cout << " Result: " << status.second << std::endl;
		
	std::cout << "Emplace with created widget" << std::endl;
	wset.emplace(Widget(30));

	std::cout << "Emplace with ctr parameters" << std::endl;
	wset.emplace(40);

	std::cout << "Looks like less copying and destroying temporary objects with emplace" << std::endl;

	std::cout << "Set size " << wset.size() << std::endl;
	for (auto &w : wset)
	{
		std::cout << w.getId() << std::endl;
	}
	

	std::cout << "TestSetInsertAndEmplace end" << std::endl;
}