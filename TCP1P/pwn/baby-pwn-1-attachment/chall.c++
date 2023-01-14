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
    std::ifstream file("./logo");
    if (file.is_open())
    {
        std::cout << file.rdbuf();
    }
    file.close();
    putchar('\n');
}

__attribute__((used, hot, noinline)) void flag()
{
    std::ifstream file("./flag.txt");
    if (file.is_open())
    {
        std::cout << file.rdbuf();
    }
    file.close();
    putchar('\n');
}

void vuln()
{
    Setup();
    char name[0x64];
    int c, i = 0;

    logo();
    puts("Hello! welcome to TCP1P!");
    puts("What is your name?");
    do
    {
        c = getchar();
        if (c == '\n')
        {
            break;
        }
        name[i] = c;
        i++;
    } while (i != 121);
}

int main()
{
    bool showflag = false;
    vuln();
    if (showflag){
        flag();
    }
}