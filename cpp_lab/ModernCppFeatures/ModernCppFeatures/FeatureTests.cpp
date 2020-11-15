#include <iostream>
#include <memory>
#include <vector>
#include <cstdlib>
#include <algorithm>
#include <thread>
#include <chrono>
#include <set>
#include <assert.h>
#include "Widget.h"
#include "FeatureTests.h"

using namespace std::chrono;

// set Widget global count to 0
int Widget::widgetCount = 0;
int Widget::assignmentCount = 0;
int Widget::copyConstructorCount = 0;
int Widget::moveConstructorCount = 0;

static int testFlag = 0;

void testFunction(int i);

void testFunction(int i)
{
	testFlag = i;
}


FeatureTests::FeatureTests(int i, int j) : _constructorMethod{ 2 }
{
}

FeatureTests::FeatureTests(int i, int j, int k) : _constructorMethod { 3 }
{
}


void FeatureTests::ResetMemoryState()
{
	Widget::widgetCount = 0;
	Widget::assignmentCount = 0;
	Widget::copyConstructorCount = 0;
	Widget::moveConstructorCount = 0;
}



// AssertNoLeakyMemory
//

void FeatureTests::AssertNoLeakyMemory()
{
	assert(Widget::widgetCount == 0);
}


// AssertLeakyMemory
//

void FeatureTests::AssertLeakyMemory()
{
	assert(Widget::widgetCount > 0);
}


// AssertAssignmentUsed
//

void FeatureTests::AssertAssignmentUsed(int expectedAssignmentsUsed)
{
	assert(Widget::assignmentCount == expectedAssignmentsUsed);
}


// AssertCopyConstructorUsed
//

void FeatureTests::AssertCopyConstructorUsed(int expectedCopyConstructorsUsed)
{
	assert(Widget::copyConstructorCount == expectedCopyConstructorsUsed);
}


// AssertMoveConstructorUsed
//

void FeatureTests::AssertMoveConstructorUsed(int expectedMoveConstructorsUsed)
{
	assert(Widget::moveConstructorCount == expectedMoveConstructorsUsed);
}



// AssertMoveConstructorUsedGreaterThan
//

void FeatureTests::AssertMoveConstructorUsedGreaterThan(int expectedMoveConstructorsUsed)
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
// explicit Tests(int i, int j, int k);Test_VectorForEachAlgorithmWithNamedLambda_ExpectIterationToWork
//

void FeatureTests::Test_ExplicitConstructor_ExpectOnlyExactParameterMatch()
{
	// This is calling the first constructor explicitly
	FeatureTests tester1(1, 2);
	assert(tester1.GetConstructorMethod() == 2);
	
	// This is calling the second constructor explicitly
	FeatureTests tester2(1, 2, 3);
	assert(tester2.GetConstructorMethod() == 3);

	// This is calling the first constructor explicitly using new initializer
	FeatureTests tester3{ 1,2 };
	assert(tester3.GetConstructorMethod() == 2);

	// This is calling the second constructor explicitly using new initializer
	FeatureTests tester4{ 1,2,3 };
	assert(tester4.GetConstructorMethod() == 3);

	// This is calling the first constructor implicitly
	FeatureTests tester5 = { 1,2 };
	assert(tester5.GetConstructorMethod() == 2);

	// This is calling the secondconstructor implicitly and does not work
	// Tests tester6 = { 1,2,3 };
}


void FeatureTests::Test_MoveOperator_ExpectMoveOperatorUsed()
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

void FeatureTests::Test_MoveUniquePtr_ExpectOriginalPtrBecomesNull()
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

void FeatureTests::Test_VectorOfRawPointers_ExpectMemoryLeak()
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


std::vector<int> FeatureTests::GetVectorOfInts()
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

std::vector<std::unique_ptr<Widget>> FeatureTests::GetVectorOfWidgetUniquePointers()
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

std::vector<std::shared_ptr<Widget>> FeatureTests::GetVectorOfWidgetSharedPointers()
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

std::map<int, std::shared_ptr<Widget>> FeatureTests::GetMapOfWidgetSharedPointers()
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

void FeatureTests::Test_VectorOfSharedPointers_ExpectNoMemoryLeak()
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

void FeatureTests::Test_VectorOfUniquePointers_ExpectNoMemoryLeak()
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

void FeatureTests::Test_SetObject_ExpectAssignmentOperatorUsed()
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

void FeatureTests::Test_ContainerPushBackWithMemoryPreallocation_ExpectCopyConstructorUsed()
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
		std::cout << "Test_ContainerPushBackWithMemoryPreallocation_ExpectCopyConstructorUsed: ";
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

void FeatureTests::Test_ContainerPushBackWithNoMemoryPreallocation_ExpectCopyConstructorUsed()
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
		std::cout << "Test_ContainerPushBackWithNoMemoryPreallocation_ExpectCopyConstructorUsed: ";
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

void FeatureTests::Test_ContainerMovePushBackWithMemoryPreallocation_ExpectMoveConstructorUsed()
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
		std::cout << "Test_ContainerMovePushBackWithMemoryPreallocation_ExpectMoveConstructorUsed: ";
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

void FeatureTests::Test_ContainerMovePushBackWithNoMemoryPreallocation_ExpectMoveConstructorUsed()
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
		std::cout << "Test_ContainerMovePushBackWithNoMemoryPreallocation_ExpectMoveConstructorUsed: ";
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

void FeatureTests::Test_ContainerOfSmartPointers_ExpectSimpleObjectConstruction()
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

void FeatureTests::Test_VectorForEachAlgorithmWithNamedLambda_ExpectForEachExecutesLambda()
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

void FeatureTests::Test_MapForEachAlgorithmWithNamedLambda_ExpectForEachExecutesLambda()
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

void FeatureTests::Test_VectorForIfAlgorithmWithAnonLambda_ExpectToFindItem()
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

void FeatureTests::Test_MakeHeapAlgorithm_ExpectMaxNodeAtRoot()
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



// Test_JoinStdThread_ExpectWaitUntilFunctionInThreadCompletes
//
// Thread can pass constructor parameters 
//

void FeatureTests::Test_JoinStdThread_ExpectWaitUntilFunctionInThreadCompletes()
{
	assert(testFlag == 0);
	thread test_thread(testFunction, 10);
	test_thread.join();
	assert(testFlag == 10);
}


// Test_JoinStdThreadwithLambda_ExpectWaitUntilLambdaFunctionInThreadCompletes

void FeatureTests::Test_JoinStdThreadwithLambda_ExpectWaitUntilLambdaFunctionInThreadCompletes()
{
	thread test_thread([](int i) {
		testFlag = i;
	}, 8);
	test_thread.join();
	assert(testFlag == 8);
}



// Test_ReuseGenericFunctionWithDifferentTypes_ExpectFunctionReuse

template <typename T>
T addTwoNumbers(T a, T b)
{
	return a + b;
}

void FeatureTests::Test_ReuseGenericFunctionWithDifferentTypes_ExpectFunctionReuse()
{
	int a = addTwoNumbers(6, 7);
	assert(a == 13);

	double d = addTwoNumbers(7.0, 5.6);
	assert(d == 12.6);
}


// Test_SetInsertAndEmplace_ExpectWidgetsInserted
//
// Insert takes as argument an object of the container's type.
// Emplace takes as argument the container's type's arguments- for constructing
//  a dummy object to insert into the container.
//
// The return result of an insert or emplace operation is a pair
// the first item being the iterator to the inserted item
// the second item being a true/false status of the operation
//

void FeatureTests::Test_SetInsertAndEmplace_ExpectWidgetsInserted()
{
	set<Widget> wset;
	auto status = wset.insert(Widget(10));
	assert(status.second == true);
		
	status = wset.emplace(Widget(30));
	assert(status.second == true);

	status = wset.emplace(40);
	assert(status.second == true);

	assert(wset.size() == 3);
}


// Test_SetInsert_ExpectSetOrderedByValue
//
// Set, standard container
// - does not contain duplicate elements
// - can contain any specified type specified in template
// - stores elements in balanced binary tree
// - by default set uses the operator < for sorting and finding 
//

void FeatureTests::Test_SetInsert_ExpectSetOrderedByValue()
{
	set<int> mySet;

	for (int i = 0; i < 10; i++) {
		int r = rand() % 10000;  // 0 to 9999
		mySet.insert(r);
	}

	int prevNum = -1;
	for (auto s : mySet) {
		assert(s >= prevNum);
		prevNum = s;
	}
}


// Test_SetFindUsesLessThanOperator_ExpectToFindItemInSet
//

void FeatureTests::Test_SetFindUsesLessThanOperator_ExpectToFindItemInSet()
{
	set<Widget> mySet;

	mySet.insert(Widget(20000));
	for (int i = 0; i < 10; i++) {
		int r = rand() % 10000;  // 0 to 9999
		mySet.insert(Widget(r));
	}

	Widget target(20000);
	auto iter = mySet.find(target);
	assert(iter != mySet.end());
	assert(iter->getId() == target.getId());
}


// Test_SetOrderByStdSortWithCustomOperator_ExpectSortByCustomOperator
// 
// Use a custom functor to sort a set's items.
//

void FeatureTests::Test_SetOrderByStdSortWithCustomOperator_ExpectSortByCustomOperator()
{
	set<Widget, Comparators> mySet;

	for (int i = 0; i < 10; i++) {
		int r = rand() % 10000;  // 0 to 9999
		mySet.insert(Widget(r));
	}

	for (auto s : mySet) {
		std::cout << s.getId() << std::endl;
	}

}


void FeatureTests::Test_Constness_ExpectConst()
{
	// these are just bad programming examples
	// do not use for real
	int tmp = 10;
	int tmp2 = 20;

	// Read from right to left.
	// For example- int* const p
	// Reading this from right to left gives us
	// p is a const pointer to an int
	//
	// On the other hand,
	// int const* p
	// will read as 
	// p is a pointer to a const int

	// pointer to integer
	int *p0 = &tmp;
	*p0 = 3;	// this compiles

	const int* p1 = &tmp;
	// *p = 5;		does not compile

	int* const p2 = &tmp;
	//p2 = new int[10]; // DOES NOT COMPILE

}


// Test_DeclType_ExpectUsageExample
//
// decltype returns the type of the variable or function or template
//

void FeatureTests::Test_DeclType_ExpectUsageExample()
{
	int a = 1;
	decltype(a) b = a;

	assert(b == a);
}