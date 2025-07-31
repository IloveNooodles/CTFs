#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void gift_set_first_arg() {
	asm volatile("pop %rdi");
	asm volatile("ret");
}

void gift_call_system() {
	system("echo \"Here's your gift!\"");
}

int main() {
	char message[0x30];

	printf("Welcome to the pivot game!\n");
	printf("Here's the pointer to message: %p\n", message);

	printf("> ");
	read(0, message, sizeof(message) + 0x10);

	printf("Message: %s\n", message);

	return 0;
}


__attribute__((constructor)) void init() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(120);
}

