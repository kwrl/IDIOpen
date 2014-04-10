#include <stdio.h>
#include <stdlib.h>


int main(int argc, char** argv)
{
    int i, num;

    for(i = 1; i < argc; i++)
    {
        num = atoi(argv[i]);
        printf("%d ", num*num);
    }

    printf("\n");
    return 0;
}
