#include<stdio.h>
#include<stdlib.h>

void printMenu() {
    printf("1. Isi survei\n2. Lihat survei\n3. Keluar\n> ");
}

void isiSurvei(char survei[]) {
    scanf("%s", survei);
    printf("Survei berhasil disimpan di: %p\n", survei);
}

void lihatSurvei() {
    int p;
    printf("Survei manakah yang ingin dilihat: ");
    scanf("%lld", &p);
    char* x = (char *) p;
    printf("%s\n", x);
}

char flag[40];

int main(int argc, char const *argv[]) {
    setvbuf(stdout, NULL, _IONBF, 0);
    FILE *fp = fopen("flag.txt", "r");
    fgets(flag, 40, fp);
    char survei[3600];
    
    while (1) {
        printMenu();
        int choice;
        scanf("%d", &choice);
        if (choice == 1) {
            isiSurvei(survei);
        } else if (choice == 2) {
            lihatSurvei();
        } else {
            printf("Bye.\n");
            return 0;
        }
    }
}
