// Hello world! Cplayground is an online sandbox that makes it easy to try out
// code.

#include <stdio.h>
#include <stdlib.h>
#include <cstdlib>
#include <iostream>
#include <time.h>

int main()
{
  srand(0x539);
  for (int i = 0; i < 5; i++)
  {
    int num = rand();
    printf("%d\n", num);
  }
}
