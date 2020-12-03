#include "pch.h"
#include "Widget.h"


int Bear::num_copied;
int Bear::num_assigned;
int Cat::num_copied;
int Cat::num_assigned;
int Cat::num_move_ctr;
int Cat::num_move_assigned;
int Widget::num_copied;
int Widget::num_assigned;
int Widget::num_move_ctr;
int Widget::num_move_assigned;

static void ResetDebugCounts() {
	Bear::num_copied = 0;
	Bear::num_assigned = 0;
	Cat::num_copied = 0;
	Cat::num_assigned = 0;
	Cat::num_move_ctr = 0;
	Cat::num_move_assigned = 0;
	Widget::num_copied = 0;
	Widget::num_assigned = 0;
	Widget::num_move_ctr = 0;
	Widget::num_move_assigned = 0;
}


TEST(Widget, Constructor_TraditionalConstructor) {
	// This calls Constructor with two parameters
	Widget w2(1, 2);
	EXPECT_EQ(w2.ConstructionMethod(), TestInternals::ConstructorMethod::TwoParams);
}


TEST(Widget, Constructor_InitialiserList) {
	// This calls Constructor with two parameters using implicit conversion.
	Widget w2{ 1, 2 };
	EXPECT_EQ(w2.ConstructionMethod(), TestInternals::ConstructorMethod::TwoParams);
}


TEST(Widget, Constructor_ExplicitKeywordPreventsImplicitConstruction) {

	Widget w1(1);
	EXPECT_EQ(w1.ConstructionMethod(), TestInternals::ConstructorMethod::OneParam);

	// Compile error below!
	//
	// explicit keyword in Widget constructor for one parameter prevents this type of 
	// implicit conversion

	// Widget w2 = 2;
}


TEST(Widget, CopyConstructor_ExpectCopyConstruction) {

	Widget w1(1);
	Widget w2 = w1;
	EXPECT_EQ(w2.ConstructionMethod(), TestInternals::ConstructorMethod::CopyCtr);
}


TEST(Widget, AssignmentOperator_ExpectAssignment) {

	Widget w1(1);
	Widget w2(2);
	w2 = w1;
	EXPECT_EQ(w2.ConstructionMethod(), TestInternals::ConstructorMethod::AssignOp);
}


TEST(Widget, MoveConstructor_ExpectMoveConstruction) {

	Widget w1(1);
	Widget w2(std::move(w1)); // move operator makes a left value into a right value
	EXPECT_EQ(w2.ConstructionMethod(), TestInternals::ConstructorMethod::MoveCtr);	
}


TEST(Widget, MoveAssignmentOperator_ExpectMoveAssignment) {

	Widget w1(1);
	Widget w2(2);
	w2 = std::move(w1);	// move operator makes a left value into a right value
	EXPECT_EQ(w2.ConstructionMethod(), TestInternals::ConstructorMethod::MoveAssignOp);
}


TEST(Widget, MoveUniquePtr_ExpectNullPointer) {

	auto w1 = std::make_unique<Widget>(1);
	auto w2 = std::move(w1);

	EXPECT_EQ(w1, nullptr);
	EXPECT_EQ(w2->getId(), 1);
}



TEST(Widget, OldClassWithNoUserDesignedMoves_CopyAndAssignmentDemo_GuessOperation) {

	BearVec v;			// vector of Bear objects

	Bear b1;
	v.push_back(b1);	// vector contains a copy of b1

	Bear c1;			// make c1
	// c1 already exists at this point
	// if c1 doesn't exist, then the follow line is a copyctr
	// but because c1 already exists, then it is an assignment instead
	c1 = v[0];			// now reassign c1 to v[0]

	EXPECT_EQ(b1.getm(), TestInternals::ConstructorMethod::OneParam);	// original ctr
	EXPECT_EQ(v[0].getm(), TestInternals::ConstructorMethod::CopyCtr);	// copy ctr
	EXPECT_EQ(c1.getm(), TestInternals::ConstructorMethod::AssignOp);	// assignment op
}


TEST(Widget, OldClassWithNoUserDesignedMoves_AtToSmallContainer_NumberCopiedNotExpected) {

	BearVec v;	// vector of Bear objects
				// vector not pre-allocated space
				// the container size doubles with each re-allocation
				// 0, 1, 2, 4...
	Bear b1;
	Bear b2;

	ResetDebugCounts();
	v.push_back(b1);	// vector contains a copy of b1
	v.push_back(b2);	// vector contains a copy of b2

	// if container gets memory reallocated, the container items get recopied
	// which explains why there are more number of copies than expected
	EXPECT_EQ(Bear::num_copied, 3);
	EXPECT_EQ(Bear::num_assigned, 0);
}



TEST(Widget, OldClassWithNoUserDesignedMoves_AtToPreAllocatedContainer_NumberCopiedExpected) {

	BearVec v;		// vector of Bear objects
	v.reserve(100); // allocate a vector of 100 Bears

	Bear b1;
	Bear b2;

	ResetDebugCounts();
	v.push_back(b1);	// vector contains a copy of b1
	v.push_back(b2);	// vector contains a copy of b2

	// container had memory pre-allocated, so there was no need to reshuffle contained items	
	// this explains there are exactly two copy operations 
	EXPECT_EQ(Bear::num_copied, 2);
	EXPECT_EQ(Bear::num_assigned, 0);
}


TEST(Widget, OldClassWithNoUserDesignedMoves_AddToContainerNewItem_ExpectTwoCopyOps) {

	BearVec v;		// vector of Bear objects
	v.reserve(100); // allocate a vector of 100 Bears

	ResetDebugCounts();
	v.push_back(*(new Bear));	// vector contains a copy of new Bear (right value, but no move funct)

	EXPECT_EQ(Bear::num_copied, 1);	// expect only 1 copy of the newed Bear item into container
	EXPECT_EQ(Bear::num_assigned, 0);
}


TEST(Widget, OldClassWithNoUserDesignedMoves_AddToContainer_ExpectCopyOps) {

	BearVec v;			// vector of Bear objects
	v.reserve(100);		// allocate a vector of 100 Bears

	Bear b1;
	Bear b2;
	EXPECT_EQ(b1.getm(), TestInternals::ConstructorMethod::OneParam);
	EXPECT_EQ(b2.getm(), TestInternals::ConstructorMethod::OneParam);

	v.push_back(b1);	// this makes a copy, but no move function provided
	v.push_back(b2);	// so stl container use the copy ctr instead

	ResetDebugCounts();

	for (BearVec::iterator iter = v.begin(); iter != v.end(); iter++) {
		EXPECT_EQ((*iter).getm(), TestInternals::ConstructorMethod::CopyCtr);
	}

	// the copy operations were made at during the vector push_back
	// not during the container iteration
	EXPECT_EQ(Bear::num_copied, 0);
	EXPECT_EQ(Bear::num_assigned, 0);
}


TEST(Widget, OldClassWithNoUserDesignedMoves_AddToContainerOfPtrs_ExpectNoCopyOps) {

	BearPtrVec v;		// vector of Bear pointers
	v.reserve(100);		// allocate a vector of 100 Bears pointers

	Bear* b1 = new Bear;
	Bear* b2 = new Bear;
	EXPECT_EQ(b1->getm(), TestInternals::ConstructorMethod::OneParam);
	EXPECT_EQ(b2->getm(), TestInternals::ConstructorMethod::OneParam);
	v.push_back(b1);
	v.push_back(b2);
	EXPECT_EQ(b1->getm(), TestInternals::ConstructorMethod::OneParam);
	EXPECT_EQ(b2->getm(), TestInternals::ConstructorMethod::OneParam);
	EXPECT_EQ(v[0]->getm(), TestInternals::ConstructorMethod::OneParam);
	EXPECT_EQ(v[1]->getm(), TestInternals::ConstructorMethod::OneParam);

	ResetDebugCounts();
	for (BearPtrVec::iterator iter = v.begin(); iter != v.end(); ++iter) {
		EXPECT_EQ((*iter)->getm(), TestInternals::ConstructorMethod::OneParam);
	}

	// there were no copies made at any time- during container push_back or iteration
	EXPECT_EQ(Bear::num_copied, 0);
	EXPECT_EQ(Bear::num_assigned, 0);
}


TEST(Widget, OldClassWithNoUserDesignedMoves_IterateWithAutoRef_ExpectNoCopyOps) {

	BearPtrVec v;		// vector of Bear pointers
	v.reserve(100);		// allocate a vector of 100 Bears pointers

	Bear* b1 = new Bear;
	Bear* b2 = new Bear;
	EXPECT_EQ(b1->getm(), TestInternals::ConstructorMethod::OneParam);
	EXPECT_EQ(b2->getm(), TestInternals::ConstructorMethod::OneParam);
	v.push_back(b1);
	v.push_back(b2);
	EXPECT_EQ(b1->getm(), TestInternals::ConstructorMethod::OneParam);
	EXPECT_EQ(b2->getm(), TestInternals::ConstructorMethod::OneParam);
	EXPECT_EQ(v[0]->getm(), TestInternals::ConstructorMethod::OneParam);
	EXPECT_EQ(v[1]->getm(), TestInternals::ConstructorMethod::OneParam);

	ResetDebugCounts();	
	for (auto b : v) {	// auto here is equivalent to Bear *, it is whatever is in the container
		EXPECT_EQ(b->getm(), TestInternals::ConstructorMethod::OneParam);
	}

	// there were no copies made at any time- during container push_back or iteration
	EXPECT_EQ(Bear::num_copied, 0);
	EXPECT_EQ(Bear::num_assigned, 0);
}


TEST(Widget, OldClassWithNoUserDesignedMoves_DumbIterateWithAuto_ExpectCopyOps) {

	BearVec v;			// vector of Bear objects
	v.reserve(100);		// allocate a vector of 100 Bears

	Bear b1;
	Bear b2;
	EXPECT_EQ(b1.getm(), TestInternals::ConstructorMethod::OneParam);
	EXPECT_EQ(b2.getm(), TestInternals::ConstructorMethod::OneParam);
	v.push_back(b1);	// this makes a copy, but no move function provided
	v.push_back(b2);	// so stl container use the copy ctr instead
	// this test shows the items in the container were copied over
	EXPECT_EQ(v[0].getm(), TestInternals::ConstructorMethod::CopyCtr);
	EXPECT_EQ(v[1].getm(), TestInternals::ConstructorMethod::CopyCtr);

	ResetDebugCounts();	
	for (auto b : v) { // auto here is equivalent to Bear, it is whatever is in the container
		EXPECT_EQ(b.getm(), TestInternals::ConstructorMethod::CopyCtr);
	}

	// during iteration, there were additional copies made- again
	EXPECT_EQ(Bear::num_copied, 2);
	EXPECT_EQ(Bear::num_assigned, 0);
}


TEST(Widget, OldClassWithNoUserDesignedMoves_SmartIterateWithAuto_ExpectNoCopyOps) {

	BearVec v;			// vector of Bear objects
	v.reserve(100);		// allocate a vector of 100 Bears

	Bear b1;
	Bear b2;
	EXPECT_EQ(b1.getm(), TestInternals::ConstructorMethod::OneParam);
	EXPECT_EQ(b2.getm(), TestInternals::ConstructorMethod::OneParam);
	v.push_back(b1);	// this makes a copy, but no move function provided
	v.push_back(b2);	// so stl container use the copy ctr instead
	// this test shows the items in the container were copied over
	EXPECT_EQ(v[0].getm(), TestInternals::ConstructorMethod::CopyCtr);
	EXPECT_EQ(v[1].getm(), TestInternals::ConstructorMethod::CopyCtr);

	ResetDebugCounts();

	// auto& here is equivalent to Bear &, it is whatever is in the container
	for (auto& b : v) {
		EXPECT_EQ(b.getm(), TestInternals::ConstructorMethod::CopyCtr);
	}

	// during iteration, there were additional copies made- again
	EXPECT_EQ(Bear::num_copied, 0);
	EXPECT_EQ(Bear::num_assigned, 0);
}


TEST(Widget, OldClassWithNoUserDesignedMoves_SmartConstIterateWithAuto_ExpectNoCopyOps) {

	BearVec v;			// vector of Bear objects
	v.reserve(100);		// allocate a vector of 100 Bears

	Bear b1;
	Bear b2;
	EXPECT_EQ(b1.getm(), TestInternals::ConstructorMethod::OneParam);
	EXPECT_EQ(b2.getm(), TestInternals::ConstructorMethod::OneParam);
	v.push_back(b1);	// this makes a copy, but no move function provided
	v.push_back(b2);	// so stl container use the copy ctr instead
	// this test shows the items in the container were copied over
	EXPECT_EQ(v[0].getm(), TestInternals::ConstructorMethod::CopyCtr);
	EXPECT_EQ(v[1].getm(), TestInternals::ConstructorMethod::CopyCtr);

	ResetDebugCounts();

	// auto& here is equivalent to Bear &, it is whatever is in the container
	for (const auto& b : v) {
		EXPECT_EQ(b.getm(), TestInternals::ConstructorMethod::CopyCtr);
	}

	// during iteration, there were additional copies made- again
	EXPECT_EQ(Bear::num_copied, 0);
	EXPECT_EQ(Bear::num_assigned, 0);
}


TEST(Widget, ModernClass_AddLValueToContainer_ExpectCopyCtr) {

	WidgetVec v;		// vector of Widget objects
	v.reserve(100);		// allocate a vector of 100 Widgets

	Widget w1(1);
	EXPECT_EQ(w1.ConstructionMethod(), TestInternals::ConstructorMethod::OneParam);

	ResetDebugCounts();

	v.push_back(w1);	// this makes a copy, but we have a move function 
						// so stl container should use the move ctr 

	EXPECT_EQ(v[0].ConstructionMethod(), TestInternals::ConstructorMethod::CopyCtr);
	EXPECT_EQ(Widget::num_copied, 1);
	EXPECT_EQ(Widget::num_assigned, 0);
	EXPECT_EQ(Widget::num_move_ctr, 0);
	EXPECT_EQ(Widget::num_move_assigned, 0);
}


TEST(Widget, ModernClass_AddRValueToContainer_ExpectMoveCtr) {

	WidgetVec v;		// vector of Widget objects
	v.reserve(100);		// allocate a vector of 100 Widgets

	ResetDebugCounts();

	v.push_back(Widget(1));	// this makes a copy, but we have a move function 
							// so stl container should use the move ctr 

	EXPECT_EQ(v[0].ConstructionMethod(), TestInternals::ConstructorMethod::MoveCtr);
	EXPECT_EQ(Widget::num_copied, 0);
	EXPECT_EQ(Widget::num_assigned, 0);
	EXPECT_EQ(Widget::num_move_ctr, 1);
	EXPECT_EQ(Widget::num_move_assigned, 0);
}



TEST(Widget, ModernClass_MoveCtrUniquePtr_ExpectMoveCtr) {

	ResetDebugCounts();

	// we want a move ctr
	// we create c1 from a nameless Cat object, so we call move ctr
	Cat c1(std::move(Cat()));
	
	EXPECT_EQ(c1.getm(), TestInternals::ConstructorMethod::MoveCtr);
	EXPECT_EQ(Cat::num_copied, 0);
	EXPECT_EQ(Cat::num_assigned, 0);
	EXPECT_EQ(Cat::num_move_ctr, 1);
	EXPECT_EQ(Cat::num_move_assigned, 0);
}


TEST(Widget, ModernClass_MoveAssignmentUniquePtr_ExpectMoveAssignment) {

	ResetDebugCounts();

	// we want a move assignment
	// first construct an existing Cat, then reassign it

	Cat c1;
	c1 = Cat();		// reassign existing Cat to new Cat- this moves assign

	EXPECT_EQ(c1.getm(), TestInternals::ConstructorMethod::MoveAssignOp);
	EXPECT_EQ(Cat::num_copied, 0);
	EXPECT_EQ(Cat::num_assigned, 0);
	EXPECT_EQ(Cat::num_move_ctr, 0);
	EXPECT_EQ(Cat::num_move_assigned, 1);
}