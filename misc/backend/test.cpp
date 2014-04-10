#include <iostream>
#include <stdlib.h>


int main(int argc, char** argv)
{
    int i, num;

    for(i = 1; i < argc; i++)
    {
        num = atoi(argv[i]);
        std::cout << num*num << " ";
    }

    std::cout << std::endl;
    return 0;
}
