// gcc fstr4.c -o fstr4

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void readFlag() {
	char flag[32];
	FILE *fptr;
	fptr = fopen("flag.txt", "r");
	fread(flag, sizeof(char), 32, fptr);
	puts(flag);
}

void vuln() {
	char name[64];
	char message[64];
	puts("what's your name?");
	fgets(name, 64, stdin);
	printf("hello, ");
	printf(name);
	puts("anything you wanna say?");
	gets(message);
	puts("bye!");
}

int main() {
	setbuf(stdout, NULL);
	puts("hi, welcome to fstring, now with bof!");
	vuln();
	return 0;
}