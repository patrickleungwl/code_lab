## Modern Cpp Features

const_cast
static_cast
reinterpret_cast
dynamic_cast

* lambda expressions
* hashed containers- unordered_map
* thread, mutex, lock
* future, promise, async
* unique_ptr
* shared_ptr

### Lambda Expressions

A lambda expression is an anonymous function object (a closure) 
for passing an operation as an argument to an algorithm or asynchornous
methods.  The notation for defining a lambda consists of- 

* capture list- list of variables to use inside lambda and whether by 
   copy or by reference
  * [] empty capture list
  * [&] use all local variables by reference
  * [=] use all local variables by value
  * [names] use all named variables by reference & or by value
  * [&, names] use all local variables by reference except for those named
  * [=, names] use all local variables by value except for those named
* parameter list (optional)- parameters in the lambda
* mutable (optional), rarely used modifier to allow updating the state
   of the closure (updating the external variables)
* noexcept (optional)
* return type (optional)
* body- the lambda logic


### Static Assertions

Static Assertions are intended to catch errors at compile time. 

Example:

~~~
constexpr double myval = 3.2;
static_assert(myval<10, "myval is unexpected");
~~~


### Constant Expressions

There are two streams of immutability in C++.  

+ const means 'this value will not change'.  This is primarily used
for declaring interfaces.
+ constexpr means 'the compiler will evaluate this at compile time'. 

Examples:

~~~
const int cwidth = 100;
int clength = 90;
constexpr double cmax = 2.0 * myfunc(cwidth)	// OK
constexpr double clen = 2.0 * myfunc(clength)	// Error
~~~

Const expressions evaluate expressions to product constant
values at compile time.  It is like template metaprogramming but 
uses familiar C++ syntax and is therefore easier to maintain. 

The benefits are that constant expressions produces constants at 
compile time instead of at runtime.  This minimizes runtime 
execution time costs- and generated code.  This follows our 
development philosophy that it is best to catch errors as early
as possible- in this case- during compile time instead of at runtime.

Furthermore, constexpr functions tell the compiler that it only
returns constant literal types.  Consider the following:

~~~
const int getArraySize() { return 42; }

int main() {
    int myArray[getArraySize()];  // this fails to compile
    return 0;
}
~~~~

But with constexpr, the compiler sees getArraySize() as returning a 
constant at compile time:

~~~
constexpr int getArraySize() { return 42; }

int main() {
    int myArray[getArraySize()];  // OK
    return 0;
}
~~~~

Because a compiler has to evaluate a function at compile time, a 
constexpr has a lot of restrictions- basically it must be a simple
function.   Here are some restrictions:

* cannot throw exceptions, no try-catch blocks, no gotos
* no calls to other constexpr functions
* the return type must be a literal type, no void.
* cannot be a virtual constexpr member function
* all arguments must be literal types
* no new, delete, or dynamic_casts

**Literal types** are types that can be determined at compile time.  All 
built-in types and some user-defined types are literal types- provided 
they have const data members and a trivial destructor. 

**Interesting trivia!**

A data member of a struct or class **cannot** be constexpr.  It can
only be *static constexpr*.  The reason is because a process can only
create an instance of a struct or class at runtime.  The compiler does
not know the value of the data member at compile time unless there is 
only one (static) instance of that data member. 


