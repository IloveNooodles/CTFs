#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(){
  srand(0x13371337);
  int counter = 0;
  int loop = 0;
  printf("[");
  while(counter < 38){
  	int num = rand();
	if(num % 100 < 21){
		counter += 1;
		printf("%d,", loop);
	}
	else {
	  num = rand();
	}
  	loop += 1;
  }
  printf("]");
}
