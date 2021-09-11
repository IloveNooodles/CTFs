#include <bits/stdc++.h>
using namespace std;

string misteri(int n){
  string object = "";
      int n2 = 0;
      int n3 = 1;
      while (n > 0) {
          n2 |= (n & 1) << n3 % 8 - 1;
          n >>= 1;
            if (n3 % 8 == 0) {
              if (32 <= n2 && n2 < 128) {
                  object = char(n2) + object;
              }
              n2 = 0;
            }
          ++n3;
        }
      object = char(n2) + object;
      return object;
}

int main(){
  cout << misteri(55);
}