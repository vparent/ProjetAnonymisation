#include <iostream>

#include "tests.hpp"

int main()
{
    if (test_dataframe()) std::cerr << "test_dataframe() failed" << std::endl;
    //if (test_anonymisation()) { return 1; }

    return 0;
}
