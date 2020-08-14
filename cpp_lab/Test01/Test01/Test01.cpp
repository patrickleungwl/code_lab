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

	// Explicit keyword with constructor
	tester.Test_ExplicitConstructor_ExpectOnlyExactParameterMatch();

	// Smart pointers
	tester.Test_VectorOfRawPointers_ExpectMemoryLeak();
	tester.Test_VectorOfSharedPointers_ExpectNoMemoryLeak();
	tester.Test_VectorOfUniquePointers_ExpectNoMemoryLeak();
	tester.Test_SetObject_ExpectAssignmentOperatorUsed();
	tester.Test_ContainerOfSmartPointers_ExpectSimpleObjectConstruction();

	// Move semantics
	tester.Test_MoveUniquePtr_ExpectOriginalPtrBecomesNull();
	tester.Test_ContainerPushBackWithNoMemoryPreallocation_ExpectCopyConstructorUsed();
	tester.Test_ContainerMovePushBackWithNoMemoryPreallocation_ExpectMoveConstructorUsed();
	tester.Test_ContainerPushBackWithMemoryPreallocation_ExpectCopyConstructorUsed();
	tester.Test_ContainerMovePushBackWithMemoryPreallocation_ExpectMoveConstructorUsed();

	// Lambdas
	tester.Test_VectorForEachAlgorithmWithNamedLambda_ExpectIterationToWork();
	tester.Test_MapForEachAlgorithmWithNamedLambda_ExpectIterationToWork();
	tester.Test_VectorForIfAlgorithmWithAnonLambda_ExpectToFindItem();

	tester.TestAlgoMakeHeapOnVectorOfInts();

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

