## Cpp 11 Features

### Static Assertions

Static Assertions are intended to catch errors at compile time. 

Example:

~~~
constexpr double myval = 3.2;
static_assert(myval<10, "myval is unexpected");
~~~


### Constant Expressions

There are two streams of immutability in C++.  

* **const** means 'this value will not change'.  This is primarily used
for declaring interfaces.
* **constexpr** means 'the compiler will evaluate this at compile time'. 

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

Also, function can be made constexpr.  Constant expression functions
will be evaluated at compile time.  The only constraint on constexpr
functions is that they do not have any side effects.  In C++ 11, 
they also cannot have any loops although this restriction was removed
in C++ 14.

Examples:

~~~
constexpr int const8 = 8;

struct structA {
   static constexpr char name[] = "myname";
   ...
};

~~~

Constexpr functions have interesting dual-use features.  When constexpr
functions are passed compile-time constants, they get evaluated at compile
time.  When constexpr functions are called with parameters not known 
at compile-time, they act like regular functions and get evaluated at runtime.
