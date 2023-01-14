#include <iostream>
#include <fstream>
#include <cstdio>

void Setup()
{
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

void flag(char *txt)
{
    std::ifstream file("./flag.txt");
    if (file.is_open())
    {
        file >> txt;
    }
    else
    {
        puts("flag not found!");
    }
    for (int i = 0; i < 100; i++)
    {
        if (txt[i] == '_')
        {
            txt[i] = '\0';
        }
    }
}

void usrinput(char *s)
{
    char c, i;
    do
    {
        c = getchar();
        if (c == '\n')
        {
            break;
        }
        s[i] = c;
        i++;
    } while (i != 100);
}

void vuln()
{
    char mflag[100];
    flag(mflag);
    char name[32];
    logo();
    puts("Hello! welcome to TCP1P!");
    puts("What is your name?");
    usrinput(name);
    printf("hello %s", name);
}

int main()
{
    Setup();
    vuln();
}