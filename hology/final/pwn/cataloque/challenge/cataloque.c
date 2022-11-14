#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#define MAX_INT 256


void banner(){
    printf("===== Welcome to Waifu Appreciator Service =====\n");
    printf("Tell me your Waifu, and I will give you her picts\n");
}

int run() {
    FILE* ptr;
    struct stat buffer;
    char ch;
    char path[MAX_INT];
    char waifu[MAX_INT];

    banner();

    while (1)
    {
        printf("\n>> ");
        fgets(waifu, sizeof(waifu), stdin);
        strtok(waifu, "\n");
        snprintf(path, MAX_INT, "./%s/links.txt", waifu);
        ptr = fopen(path, "r");
        if (NULL == ptr || stat(path, &buffer)) {
            printf("I can't find your waifu \n");
            return 0;
        }
        do {
            ch = fgetc(ptr);
            printf("%c", ch);
        } while (ch != EOF);

        fclose(ptr);
    }
    return 0;
}


void init() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
}
 
int main() {
    init();
    run();
    return 0;
}