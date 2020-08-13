#pragma once

#include <vector>
#include <memory>
#include "Widget.h"

using namespace std;

class Tests
{
public:
	Tests(int i, int j);
	explicit Tests(int i, int j, int k);


	void Test_ExplicitConstructor_ExpectOnlyExactParameterMatch();
	void Test_MoveUniquePtr_ExpectOriginalPtrBecomesNull();
	void Test_VectorOfRawPointers_ExpectMemoryLeak();

	void Test_VectorOfSharedPointers_ExpectNoMemoryLeak();
	void Test_VectorOfUniquePointers_ExpectNoMemoryLeak();

	void Test_SetObject_ExpectAssignmentOperatorUsed();

	void Test_ContainerPushBackWithMemoryPreallocation_ExpectCopyConstructorUsed();
	void Test_ContainerPushBackWithNoMemoryPreallocation_ExpectCopyConstructorUsed();
	void Test_ContainerMovePushBackWithMemoryPreallocation_ExpectMoveConstructorUsed();
	void Test_ContainerMovePushBackWithNoMemoryPreallocation_ExpectMoveConstructorUsed();

	void Test_ContainerOfSmartPointers_ExpectSimpleObjectConstruction();

	void TestAlgoFindOnVector();
	void TestAlgoMakeHeapOnVector();
	void TestAlgoMakeHeapOnVectorOfInts();
	void TestAlgoMakeHeapOnVectorOfWidgets();
	void TestNewThreadWithFunction();
	void TestNewThreadWithLambdaFunction();
	void TestVectorPushback();
	void TestMoveConstructor();
	void TestGenericFunction();
	void TestSetInsertAndEmplace();

private:
	std::vector<std::shared_ptr<Widget>> GetVectorOfSharedWidgetPointers();
	std::vector<std::unique_ptr<Widget>> GetVectorOfUniqueWidgetPointers();
	int _constructorMethod;

	int  GetConstructorMethod() { return _constructorMethod; }
	void ResetMemoryState();

	void AssertNoLeakyMemory();
	void AssertLeakyMemory();
	void AssertAssignmentUsed(int expectedAssignmentsUsed);
	void AssertCopyConstructorUsed(int expectedCopyConstructorsUsed);
	void AssertMoveConstructorUsed(int expectedMoveConstructorsUsed);
	void AssertMoveConstructorUsedGreaterThan(int expectedMoveConstructorsUsed);


};