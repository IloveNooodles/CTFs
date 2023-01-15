#include <iostream>
#include <fstream>
#include <cstdio>

void Setup() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
}

void logo()
{
    std::ifstream file("/app/logo");
    if (file.is_open())
    {
        std::cout << file.rdbuf();
    }
    file.close();
    putchar('\n');
}

void vuln()
{
    char name[0x32];

    logo();
    puts("Hello! welcome to TCP1P!");
    puts("What are you doing?");
    printf("ups leak! %lX\n", (void *)fgets);
    printf("ups leak! %lX\n", (void *)printf);
    printf("ups leak! %lX\n", (void *)puts);
    fgets(name, 1000, stdin);
}

int main()
{
    Setup();
    vuln();
}