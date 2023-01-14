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
    char name[8];
    int isAdmin = false;
    logo();
    puts("Hello! welcome to TCP1P!");
    puts("What is your name?");
    fgets(name, 16, stdin);
    if (isAdmin == true){
        puts("wellcome admin!");
        flag();
    } else {
        puts("good bye!");
    }
}

int main()
{
    Setup();
    vuln();
}