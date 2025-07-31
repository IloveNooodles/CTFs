#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void init() {
    // You don't need to read this because it's just initialization
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
}

int main() {
    init();

    char pet_name[32] = {0};
    char path[128] = "/home/pwn/pet_sound.txt";

    printf("Your pet name?: ");
    scanf("%s", pet_name);

    FILE *fp = fopen(path, "r");
    if (fp) {
        char buf[256] = {0};
        if (fgets(buf, sizeof(buf), fp) != NULL) {
            printf("%s sound: %s\n", pet_name, buf);
        } else {
            puts("Failed to read the file.");
        }
        fclose(fp);
    } else {
        printf("File not found: %s\n", path);
    }
    return 0;
}