#include <stdio.h>
#include <stdlib.h>
// gcc srop.c -o srop -no-pie -fno-stack-protector
void syscall_(){
  asm("syscall; ret;");
}

void set_rax(){
  // asm(".intel_syntax noprefix");
  asm("mov eax, 0xf; ret;");
}

int main(){
    char buff[100];
    printf("Oopss buffer leak: %p, can you SROP?\n", buff);
    read(0, buff, 5000);
    return 0;
}