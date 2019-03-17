#pragma once

#include <vector>
#include <memory>
#include "Widget.h"

using namespace std;

class Tests
{
private:
	vector<shared_ptr<Widget>> GetVectorOfSharedWidgetPointers();

public:
	void TestUniquePtr();
	void TestVectorContainerUsage();
	void TestVectorOfWidgetPointers();
	void TestVectorOfSharedWidgetPointers();
	void TestVectorIteration();
	void TestLambdaOnVector();
	void TestAlgoFindOnVector();
	void TestAlgoMakeHeapOnVector();
	void TestAlgoMakeHeapOnVectorOfInts();
	void TestAlgoMakeHeapOnVectorOfWidgets();
};