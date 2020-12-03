#pragma once

#include <memory>

class MemoryPacket {
public:
	MemoryPacket() {
		for (int i = 0; i < 100; i++) {
			m_cache[i] = 0;
		}
	}

private:
	int m_cache[100];
};


class TestInternals {
public:
	// enum class is the same as enum struct
	enum struct ConstructorMethod{ OneParam, TwoParams, CopyCtr, AssignOp, MoveCtr, MoveAssignOp };

	TestInternals(ConstructorMethod cm) : _ctorMethod(cm) {}

	ConstructorMethod ConstructionMethod() const {
		return _ctorMethod;
	}

private:
	ConstructorMethod _ctorMethod;
};


class Bear
{
public:
	Bear() : _i(0), _m(TestInternals::ConstructorMethod::OneParam) {};
	static int num_copied;
	static int num_assigned;

	// copy ctor
	Bear(const Bear& b) : _i(b._i), _m(TestInternals::ConstructorMethod::CopyCtr) {
		++num_copied;
	}

	// assignment operator
	const Bear& operator=(const Bear& b) {
		if (this != &b) {
			_i = b._i;
			_m = TestInternals(TestInternals::ConstructorMethod::AssignOp);
			++num_assigned;
		}
		return *this;
	}

	TestInternals::ConstructorMethod getm() const {
		return _m.ConstructionMethod();
	}

private:
	int _i;
	TestInternals _m;
};

typedef std::vector<Bear> BearVec;
typedef std::vector<Bear *> BearPtrVec;




class Cat
{
public:
	static int num_copied;
	static int num_assigned;
	static int num_move_ctr;
	static int num_move_assigned;

	Cat() : _i(0), 
			_m(TestInternals::ConstructorMethod::OneParam),
			_name(std::make_unique<std::string>("hello"))
	{
	};

	// copy ctor - remove it because cannot copy a unique ptr
	Cat(const Cat& c) = delete;

	// assignment operator - remove it because cannot reassign a unique ptr
	const Cat& operator=(const Cat& b) = delete;

	// move ctr
	Cat(Cat&& other) noexcept :
		_i(other._i),
		_m(TestInternals::ConstructorMethod::MoveCtr),
		_name(std::move(other._name))
	{
		++num_move_ctr;
	}

	// move assignment operator
	//
	// must guarantee noexcept because of container operations
	Cat& operator=(Cat&& other) noexcept {
		if (this != &other) {
			_i = other._i;
			_m = TestInternals::ConstructorMethod::MoveAssignOp;
			_name = std::move(other._name);
			++num_move_assigned;
		}
		return *this;
	}

	TestInternals::ConstructorMethod getm() const {
		return _m.ConstructionMethod();
	}

private:
	int _i;
	TestInternals _m;
	std::unique_ptr<std::string> _name;
};

typedef std::vector<Cat> CatVec;
typedef std::vector<Cat*> CatPtrVec;



class Widget
{
public:
	static int num_copied;
	static int num_assigned;
	static int num_move_ctr;
	static int num_move_assigned;

	explicit Widget(int i) : 
		_id(i), 
		_id2(-1),
		_ti(TestInternals::ConstructorMethod::OneParam) {
	}

	Widget(int i, int j) :
		_id(i),
		_id2(j),
		_ti(TestInternals::ConstructorMethod::TwoParams) {
		//_name = std::make_unique<std::string>("hello2");
	}

	// copy ctor
	Widget(const Widget& w) :
		_id(w._id),
		_id2(w._id2),
		_ti(TestInternals::ConstructorMethod::CopyCtr) {
		++num_copied;
	}

	// assignment operator
	const Widget& operator=(const Widget& other) {
		if (this != &other) {
			_id = other._id;
			_id2 = other._id2;
			_ti = TestInternals::ConstructorMethod::AssignOp;
			++num_assigned;
		}
		return *this;
	}

	// move ctor, no need to declare parameter const, but require noexcept
	//
	// An STL container can only use the move constructor in 
	// its resizing operation if that constructor does not break its 
	// strong exception safety guarantee. In more plain language, 
	// it wont use the move constructor of an object if that can 
	// throw an exception. This is because if an exception is 
	// thrown in the move then the data that was being processed could be 
	// lost, where as in a copy constructor the original will not be changed.
	Widget(Widget&& w) noexcept :
		_id(w._id),
		_id2(w._id2),
		_ti(TestInternals::ConstructorMethod::MoveCtr) {
		++num_move_ctr;
	}

	// move assignment operator
	//
	// must guarantee noexcept because of container operations
	Widget& operator=(Widget&& other) noexcept {
		if (this != &other) {
			this->_id = other._id;
			this->_id2 = other._id2;
			this->_ti = TestInternals::ConstructorMethod::MoveAssignOp;
			++num_move_assigned;
		}
		return *this;
	}

	virtual ~Widget() {
	};

	TestInternals::ConstructorMethod ConstructionMethod() {
		return _ti.ConstructionMethod();
	}

	int getId() const {
		return _id;
	}

private:
	int _id;
	int _id2;
	TestInternals _ti;
};

typedef std::vector<Widget> WidgetVec;
typedef std::vector<Widget*> WidgetPtrVec;
