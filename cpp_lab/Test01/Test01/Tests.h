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
	Tests(int i, int j);
	explicit Tests(int i, int j, int k);

	void TestExplicitKeyword();
	void TestForEachCopies();
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
	void TestNewThreadWithFunction();
	void TestNewThreadWithLambdaFunction();
	void TestAssignmentOperator();
	void TestVectorPushback();
	void TestMoveConstructor();
	void TestClock();
	void TestGenericFunction();
	void TestSetInsertAndEmplace();
};