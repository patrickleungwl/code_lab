// Testcpp01.cpp : Defines the entry point for the console application.
//

#include "pch.h"
#include <iostream>
#include <memory>
#include "Widget.h"
#include "Tests.h"

using namespace std;


int main()
{
	
	Tests tester(1, 2);
	
	tester.TestExplicitKeyword();
	tester.TestUniquePtr();
	tester.TestVectorIteration();
	tester.TestVectorOfWidgetPointers();
	tester.TestLambdaOnVector();
	tester.TestAlgoFindOnVector();
	tester.TestAlgoMakeHeapOnVector();
	tester.TestAlgoMakeHeapOnVectorOfInts();
	tester.TestAlgoMakeHeapOnVectorOfWidgets();
	tester.TestNewThreadWithFunction();
	tester.TestNewThreadWithLambdaFunction();
	tester.TestForEachCopies();
	tester.TestAssignmentOperator();
	tester.TestVectorContainerUsage();
	tester.TestVectorPushback();
	tester.TestVectorOfSharedWidgetPointers();
	tester.TestMoveConstructor();
	tester.TestClock();
	tester.TestGenericFunction();
	tester.TestSetInsertAndEmplace();

	int tmp = 10;
	int tmp2 = 40;
	//const int const *p = &tmp;
	
	//int * const pi = &tmp;
	//pi = &tmp2;

	// Let user check memory usage before exiting
	//int i;
	//cin >> i;

	return 0;
}

