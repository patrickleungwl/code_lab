## Cpp 11 Features

### Static Asserts

static_assert why? how?


### Constant Expressions

Constant expressions evaluate expressions to product constant
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

Constant expressions must be static in structures


