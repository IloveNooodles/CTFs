#include <stdio.h>
#include <string.h>

int main(){
  char *a = "eb_si_ss_si_sssuts_esuebtsi_rettiri_retteug_h_gn";
  char final[128] = "\0";
  char final2[128] = "\0";
  char inter_1[128] = "\0";
  char inter_2[128] = "\0";
  char inter_3[128] = "\0";
  char inter_4[128] = "\0";
  char inter_5[128] = "\0";
  memset(final, 0, 128);
  memset(final2, 0, 128);
  memset(inter_1, 0, 128);
  memset(inter_2, 0, 128);
  memset(inter_3, 0, 128);
  memset(inter_4, 0, 128);
  memset(inter_5, 0, 128);

  strncpy(inter_2, a, 10);
  strncpy(inter_3, a+10, 10);
  strncpy(inter_1, a+20, 10);
  strcat(final, inter_1);
  strcat(final, inter_2);
  strcat(final, inter_3);
  

  strncpy(inter_2, final, 6);
  strncpy(inter_5, final+6, 6);
  strncpy(inter_3, final+12, 6);
  strncpy(inter_1, final+18, 6);
  strncpy(inter_4, final+24, 6);

  strcat(final2, inter_1);
  strcat(final2, inter_2);
  strcat(final2, inter_3);
  strcat(final2, inter_4);
  strcat(final2, inter_5);

  printf("%s %s %s %s %s\n", inter_1, inter_2, inter_3, inter_4, inter_5);
  printf("%s\n", final);
  printf("%s", final2);

}


// void strcpy(long dest,long source){
//   int iVar1;
//   int i;
  
//   i = 0;
//   while(1) {
//     iVar1 = strlen(source);
//     if (iVar1 <= i) break;
//     *(dest + i) = *(source + i);
//     i = i + 1;
//   }
//   iVar1 = strlen(source);
//   *(iVar1 + dest) = 0;
//   return;
// }