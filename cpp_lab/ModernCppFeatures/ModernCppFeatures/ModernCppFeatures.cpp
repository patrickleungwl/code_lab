// ModernCppFeatures.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "FeatureTests.h"

int main()
{
	FeatureTests tester(1, 2);

	// Explicit keyword with constructor
	FeatureTests::Test_ExplicitConstructor_ExpectOnlyExactParameterMatch();

	// Smart pointers
	tester.Test_VectorOfRawPointers_ExpectMemoryLeak();
	tester.Test_VectorOfSharedPointers_ExpectNoMemoryLeak();
	tester.Test_VectorOfUniquePointers_ExpectNoMemoryLeak();
	tester.Test_SetObject_ExpectAssignmentOperatorUsed();
	tester.Test_ContainerOfSmartPointers_ExpectSimpleObjectConstruction();

	// Move semantics
	tester.Test_MoveOperator_ExpectMoveOperatorUsed();
	tester.Test_MoveUniquePtr_ExpectOriginalPtrBecomesNull();
	tester.Test_ContainerPushBackWithNoMemoryPreallocation_ExpectCopyConstructorUsed();
	tester.Test_ContainerMovePushBackWithNoMemoryPreallocation_ExpectMoveConstructorUsed();
	tester.Test_ContainerPushBackWithMemoryPreallocation_ExpectCopyConstructorUsed();
	tester.Test_ContainerMovePushBackWithMemoryPreallocation_ExpectMoveConstructorUsed();

	// Lambdas
	tester.Test_VectorForEachAlgorithmWithNamedLambda_ExpectIterationToWork();
	tester.Test_MapForEachAlgorithmWithNamedLambda_ExpectIterationToWork();
	tester.Test_VectorForIfAlgorithmWithAnonLambda_ExpectToFindItem();

	tester.Test_MakeHeapAlgorithm_ExpectMaxNodeAtRoot();

	/*
	tester.TestAlgoMakeHeapOnVector();
	tester.TestAlgoMakeHeapOnVectorOfInts();
	tester.TestAlgoMakeHeapOnVectorOfWidgets();
	tester.TestNewThreadWithFunction();
	tester.TestNewThreadWithLambdaFunction();
	tester.TestForEachCopies();
	tester.TestMoveConstructor();
	tester.TestGenericFunction();
	tester.TestSetInsertAndEmplace();
	*/

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

