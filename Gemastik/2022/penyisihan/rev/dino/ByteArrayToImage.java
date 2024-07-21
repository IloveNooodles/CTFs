import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.OutputStream;
import java.awt.image.RenderedImage;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import javax.imageio.ImageIO;
import java.io.FileInputStream;

// 
// Decompiled by Procyon v0.5.36
// 

public class ByteArrayToImage
{
    public static void main(final String[] array) throws Exception {
        final BufferedImage removeBG = removeBG(ImageIO.read(new FileInputStream("./build/im/Big4.png")));
        final ByteArrayOutputStream output = new ByteArrayOutputStream();
        ImageIO.write(removeBG, "png", output);
        final byte[] byteArray = output.toByteArray();
        for (int i = 0; i < byteArray.length; ++i) {
            System.out.print(invokedynamic(makeConcatWithConstants:(B)Ljava/lang/String;, byteArray[i]));
        }
    }
    
    public static BufferedImage removeBG(final BufferedImage bufferedImage) {
        final BufferedImage bufferedImage2 = new BufferedImage(bufferedImage.getWidth(), bufferedImage.getHeight(), 2);
        Color obj = new Color(bufferedImage.getRGB(0, 0));
        if (bufferedImage.getWidth() == 59) {
            obj = new Color(bufferedImage.getRGB(6, 0));
        }
        final Color obj2 = new Color(bufferedImage.getRGB(4, 0));
        for (int i = 0; i < bufferedImage.getWidth(); ++i) {
            for (int j = 0; j < bufferedImage.getHeight(); ++j) {
                final Color color = new Color(bufferedImage.getRGB(i, j));
                if (!color.equals(obj) && !color.equals(obj2)) {
                    bufferedImage2.setRGB(i, j, color.getRGB());
                }
            }
        }
        return bufferedImage2;
    }
}
