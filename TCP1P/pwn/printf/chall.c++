#include <iostream>
#include <fstream>

#define MAXBUFF 8

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

char *flag(char *txt)
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
    return txt;
}

void vuln()
{
    char v_1[MAXBUFF];
    char vflag[0x100];
    flag(vflag);
    logo();
    puts("Hello! welcome to TCP1P!");
    puts("What's that?");

    fgets(v_1, MAXBUFF, stdin);
    printf("what? ");
    printf(v_1);
}

int main()
{
    Setup();
    vuln();
}