// ModernCppFeatures.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "FeatureTests.h"

int main()
{
	// Explicit keyword with constructor
	FeatureTests::Test_ExplicitConstructor_ExpectOnlyExactParameterMatch();

	// Let's start our tests 
	FeatureTests tester(1, 2);

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
	tester.Test_VectorForEachAlgorithmWithNamedLambda_ExpectForEachExecutesLambda();
	tester.Test_MapForEachAlgorithmWithNamedLambda_ExpectForEachExecutesLambda();
	tester.Test_VectorForIfAlgorithmWithAnonLambda_ExpectToFindItem();

	tester.Test_MakeHeapAlgorithm_ExpectMaxNodeAtRoot();

	// Threads
	tester.Test_JoinStdThread_ExpectWaitUntilFunctionInThreadCompletes();
	tester.Test_JoinStdThreadwithLambda_ExpectWaitUntilLambdaFunctionInThreadCompletes();

	// Generics
	tester.Test_ReuseGenericFunctionWithDifferentTypes_ExpectFunctionReuse();

	// Set container
	tester.Test_SetInsertAndEmplace_ExpectWidgetsInserted();
	tester.Test_SetInsert_ExpectSetOrderedByValue();
	tester.Test_SetOrderByStdSortWithCustomOperator_ExpectSortByCustomOperator();

	tester.Test_Constness_ExpectConst();
	tester.Test_DeclType_ExpectUsageExample();

	return 0;
}

