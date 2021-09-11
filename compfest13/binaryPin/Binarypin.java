/*
 * Decompiled with CFR 0.150.
 * 
 * Could not load the following classes:
 *  PinButton
 *  ResetButton
 */
import java.awt.Component;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class Binarypin {
    private JFrame frame = new JFrame("Binary Pin");
    private JLabel output = new JLabel();

    Binarypin() {
        this.output.setBounds(20, 250, 360, 20);
        JLabel jLabel = new JLabel("Your data:");
        jLabel.setBounds(20, 235, 100, 20);
        this.frame.add(jLabel);
        this.frame.add(this.output);
        this.frame.add((Component)new PinButton(this, "0", 43, 10, 150, 150));
        this.frame.add((Component)new PinButton(this, "1", 198, 10, 150, 150));
        this.frame.add((Component)new ResetButton(this, 43, 165, 305, 50));
        this.frame.setSize(400, 350);
        this.frame.setLayout(null);
        this.frame.setVisible(true);
        this.frame.setDefaultCloseOperation(3);
    }

    public static void main(String[] arrstring) {
        new Binarypin();
    }

    public void clearOutput() {
        this.output.setText("");
    }

    public void updateOutput() {
        this.output.setText(Secret.getInstance().getData());
    }
}