#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

void bingo(){
    system("cat ./flag");
}

void vuln(){
    char buffer[16] = {0};
    printf("Masukkan value ya..\n");
    read(0, buffer, 0x100);
}

void welcome(){
    printf("Halo selamat datang!\n");
}

int main(){
    setvbuf(stdout, NULL, _IOLBF, 0);
    welcome();
    vuln();
    return 0;
}
