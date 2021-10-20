// gcc fstr1.c -o fstr1

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char flag[32];

void readFlag(char* flag) {
	FILE *fptr;
	fptr = fopen("flag.txt", "r");
	fread(flag, sizeof(char), 32, fptr);
}

void vuln() {
	char* flag_ptr;
	char name[256];
	flag_ptr = flag;
	readFlag(flag_ptr);
	puts("what's your name?");
	fgets(name, 256, stdin);
	printf("hello, ");
	printf(name);
}

int main() {
	setbuf(stdout, NULL);
	puts("hi, welcome to fstring!");
	vuln();
	return 0;
}