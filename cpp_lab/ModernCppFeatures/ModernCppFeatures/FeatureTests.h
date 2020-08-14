#pragma once

#include <vector>
#include <map>
#include <memory>
#include "Widget.h"

using namespace std;

class FeatureTests
{
public:
	FeatureTests(int i, int j);
	explicit FeatureTests(int i, int j, int k);

	// Explicit keyword with constructor
	void Test_ExplicitConstructor_ExpectOnlyExactParameterMatch();

	// Smart pointers
	void Test_VectorOfRawPointers_ExpectMemoryLeak();
	void Test_VectorOfSharedPointers_ExpectNoMemoryLeak();
	void Test_VectorOfUniquePointers_ExpectNoMemoryLeak();
	void Test_SetObject_ExpectAssignmentOperatorUsed();
	void Test_ContainerOfSmartPointers_ExpectSimpleObjectConstruction();

	// Move semantics
	void Test_MoveOperator_ExpectMoveOperatorUsed();
	void Test_MoveUniquePtr_ExpectOriginalPtrBecomesNull();
	void Test_ContainerPushBackWithMemoryPreallocation_ExpectCopyConstructorUsed();
	void Test_ContainerPushBackWithNoMemoryPreallocation_ExpectCopyConstructorUsed();
	void Test_ContainerMovePushBackWithMemoryPreallocation_ExpectMoveConstructorUsed();
	void Test_ContainerMovePushBackWithNoMemoryPreallocation_ExpectMoveConstructorUsed();

	// Lambdas
	void Test_VectorForEachAlgorithmWithNamedLambda_ExpectIterationToWork();
	void Test_MapForEachAlgorithmWithNamedLambda_ExpectIterationToWork();
	void Test_VectorForIfAlgorithmWithAnonLambda_ExpectToFindItem();

	void Test_MakeHeapAlgorithm_ExpectMaxNodeAtRoot();

	void TestAlgoMakeHeapOnVectorOfWidgets();
	void TestNewThreadWithFunction();
	void TestNewThreadWithLambdaFunction();
	void TestMoveConstructor();
	void TestGenericFunction();
	void TestSetInsertAndEmplace();

private:
	std::vector<int> GetVectorOfInts();
	std::vector<std::shared_ptr<Widget>> GetVectorOfWidgetSharedPointers();
	std::vector<std::unique_ptr<Widget>> GetVectorOfWidgetUniquePointers();
	std::map<int, std::shared_ptr<Widget>> GetMapOfWidgetSharedPointers();
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