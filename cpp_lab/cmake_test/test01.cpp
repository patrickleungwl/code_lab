#include <iostream>
#include <functional>

int main()
{
    [out = std::ref(std::cout << "hello")](){out.get() << " world\n";}();
}
