#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

struct Pet;
void speak_flag(struct Pet *p);
void speak_sound(struct Pet *p);
void visualize_heap(struct Pet *a, struct Pet *b);

struct Pet {
    void (*speak)(struct Pet *p);
    char sound[32];
};

int main() {
    struct Pet *pet_A, *pet_B;

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);

    puts("--- Pet Hijacking ---");
    puts("Your mission: Make Pet speak the secret FLAG!\n");
    printf("[hint] The secret action 'speak_flag' is at: %p\n", speak_flag);

    pet_A = malloc(sizeof(struct Pet));
    pet_B = malloc(sizeof(struct Pet));

    pet_A->speak = speak_sound;
    strcpy(pet_A->sound, "wan...");
    pet_B->speak = speak_sound;
    strcpy(pet_B->sound, "wan...");

    printf("[*] Pet A is allocated at: %p\n", pet_A);
    printf("[*] Pet B is allocated at: %p\n", pet_B);
    
    puts("\n[Initial Heap State]");
    visualize_heap(pet_A, pet_B);

    printf("\n");
    printf("Input a new cry for Pet A > ");
    read(0, pet_A->sound, 0x32);

    puts("\n[Heap State After Input]");
    visualize_heap(pet_A, pet_B);

    pet_A->speak(pet_A);
    pet_B->speak(pet_B);

    free(pet_A);
    free(pet_B);
    return 0;
}

void speak_flag(struct Pet *p) {
    char flag[64] = {0};
    FILE *f = fopen("flag.txt", "r");
    if (f == NULL) {
        puts("\nPet seems to want to say something, but can't find 'flag.txt'...");
        return;
    }
    fgets(flag, sizeof(flag), f);
    fclose(f);
    flag[strcspn(flag, "\n")] = '\0';

    puts("\n**********************************************");
    puts("* Pet suddenly starts speaking flag.txt...!? *");
    printf("* Pet: \"%s\" *\n", flag);
    puts("**********************************************");
    exit(0);
}

void speak_sound(struct Pet *p) {
    printf("Pet says: %s\n", p->sound);
}

void visualize_heap(struct Pet *a, struct Pet *b) {
    unsigned long long *ptr = (unsigned long long *)a;
    puts("\n--- Heap Layout Visualization ---");
    for (int i = 0; i < 12; i++, ptr++) {
        printf("0x%016llx: 0x%016llx", (unsigned long long)ptr, *ptr);
        if (ptr == (unsigned long long *)&a->speak) printf(" <-- pet_A->speak");
        if (ptr == (unsigned long long *)a->sound)   printf(" <-- pet_A->sound");
        if (ptr == (unsigned long long *)&b->speak) printf(" <-- pet_B->speak (TARGET!)");
        if (ptr == (unsigned long long *)b->sound)   printf(" <-- pet_B->sound");
        puts("");
    }
    puts("---------------------------------");
}
