public class Main {
  public static int rcr(int n) {
    int n2 = -1;
    for (int i = 0; i < 4; ++i) {
      n2 ^= n >> i * 8;
      for (int j = 0; j < 8; ++j) {
        if ((n2 & 0x1) == 0x1) {
          n2 = (n2 >> 1 ^ 0xEDB88320);
        } else {
          n2 >>= 1;
        }
      }
    }
    // System.out.println(n2);
    return n2;
  }

  public static void main(String[] args) {
    System.out.println(rcr(23));
    // System.out.println(rcr(rcr(0x21cb61a) ^ 35436058));
  }
}
