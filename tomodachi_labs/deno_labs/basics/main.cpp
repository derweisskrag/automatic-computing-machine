#include <iostream>
#include <string>
#include <vector>

#if __cplusplus >= 202002L
#include <print>
#endif

int main() {
    #if __cplusplus >= 202002L
    std::print("Hello, world from C++20!\n");
    #else
    std::cout << "Hello, world from C++17 or earlier!" << std::endl;
    #endif

    return 0;
}