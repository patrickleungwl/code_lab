// Testcpp01.cpp : Defines the entry point for the console application.
//

#include "pch.h"
#include <iostream>
#include <vector>
#include <memory>
#include "Widget.h"
#include "Tests.h"

using namespace std;


int main()
{

	Tests tester;
	tester.TestUniquePtr();
	tester.TestVectorOfWidgetPointers();
	tester.TestVectorIteration();
	tester.TestLambdaOnVector();
	tester.TestAlgoFindOnVector();
	tester.TestAlgoMakeHeapOnVector();
	tester.TestAlgoMakeHeapOnVectorOfInts();
	tester.TestAlgoMakeHeapOnVectorOfWidgets();

	// Let user check memory usage before exiting
	int i;
	cin >> i;

	return 0;
}