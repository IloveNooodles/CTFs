public class Cloud
{
    public int x;
    public int y;
    public int rad1;
    public int rad2;
    
    public Cloud(final int x, final int y) {
        this.x = x;
        this.y = y;
        this.rad1 = 10 + (int)(Math.random() * 40.0 + 1.0);
        this.rad2 = 5 + (int)(Math.random() * 10.0 + 1.0);
    }
}
