#include <stdio.h>

// int check(int a, int b){
//   int c;
//   int d;
//   c = b * 10 & 0xFF;
//   d = (c + 0x539)*10;
  
// }

int main(){
  int a = 5;
  int b = 15;
  int c;
  int d;
  c = b * 10 & 0xFF; // <= 255;
  d = (c + 1337)*10; // <= 15920
  int e = d*c; // d / c == 0
  int f = c^d^b;
  int g = (e + f)^a;
  printf("%d %d %d", e, f, g);
  // 0 = b * 10 % 255;p
  // printf("%d", (3*5)^1);
}