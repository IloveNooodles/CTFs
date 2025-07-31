#include <stdio.h>
#include <unistd.h>

int vuln() {
	char message[0x30];

	printf("Welcome to the second pivot game!\n");

	printf("> ");
	read(0, message, sizeof(message) + 0x10);

	printf("Message: %s\n", message);

	return 0;
}

int main() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	alarm(120);

	vuln();
}
