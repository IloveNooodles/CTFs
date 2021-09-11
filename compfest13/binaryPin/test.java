class Secret {
    private int cnt = 1;
    private int[] box;
    private int[] mydata = new int[]{0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0};
    private static Secret instance = new Secret();

    private Secret() {
        int n = this.mydata.length / 9;
        this.box = new int[n];
    }

    public static Secret getInstance() {
        return instance;
    }

    public void resetInstance() {
        instance = new Secret();
    }

    public void process(char c) {
        if (this.cnt > 9) {
            return;
        }
        int n = this.mydata.length / 9;
        for (int i = 1; i <= n; ++i) {
            int n2 = 9 * i - this.cnt;
            int n3 = this.box[i - 1] + this.mydata[n2];
            this.mydata[n2] = (n3 += c - 48) % 2;
            this.box[i - 1] = n3 >= 2 ? 1 : 0;
        }
        ++this.cnt;
    }

    private String misteri(int n) {
        String object = "";
        int n2 = 0;
        int n3 = 1;
        while (n > 0) {
            n2 |= (n & 1) << n3 % 8 - 1;
            n >>= 1;
            if (n3 % 8 == 0) {
                if (32 <= n2 && n2 < 128) {
                    object = (char)n2 + (String)object;
                }
                n2 = 0;
            }
            ++n3;
        }
        object = (char)n2 + (String)object;
        return object;
    }

    public String getData() {
        int n = this.mydata.length / 9;
        Object object = "";
        int n2 = 5;
        int n3 = 0;
        for (int i = 1; i <= n; ++i) {
            int n4 = 0;
            int n5 = 1;
            for (int j = 1; j <= 8; ++j) {
                n4 += this.mydata[9 * i - j] * n5;
                n5 <<= 1;
            }
            n3 = (int)((double)n3 + (double)(n4 - 33) * Math.pow(85.0, --n2));
            if (n2 != 0) continue;
            object = (String)object + this.misteri(n3);
            n3 = 0;
            n2 = 5;
        }
        while (n2 > 0) {
            n3 = (int)((double)n3 + 84.0 * Math.pow(85.0, --n2));
        }
        return (String)object + this.misteri(n3);
    }
}

public class test{
  public static void main(String args[]){
    Secret s = Secret.getInstance();
    System.out.println(s.getData());
  }
}