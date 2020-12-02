#pragma once


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
private:
	int _i;
	TestInternals _m;
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
};

typedef std::vector<Bear> BearVec;
typedef std::vector<Bear *> BearPtrVec;


class Widget
{
public:
	explicit Widget(int i) : 
		_id(i), 
		_id2(-1),
		_ti(TestInternals::ConstructorMethod::OneParam) {
	}

	Widget(int i, int j) :
		_id(i),
		_id2(j),
		_ti(TestInternals::ConstructorMethod::TwoParams) {
	}

	// copy ctor
	Widget(const Widget& w) :
		_id(w._id),
		_id2(w._id2),
		_ti(TestInternals::ConstructorMethod::CopyCtr) {
	}

	// assignment operator
	const Widget& operator=(const Widget& other) {
		if (this != &other) {
			_id = other._id;
			_id2 = other._id2;
			_ti = TestInternals::ConstructorMethod::AssignOp;
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
	}

	// move assignment operator
	//
	// must guarantee noexcept because of container operations
	Widget& operator=(Widget&& other) noexcept {
		if (this != &other) {
			this->_id = other._id;
			this->_id2 = other._id2;
			this->_ti = TestInternals::ConstructorMethod::MoveAssignOp;
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

