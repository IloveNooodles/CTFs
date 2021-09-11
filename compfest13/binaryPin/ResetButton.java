/*
 * Decompiled with CFR 0.150.
 */
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;

class ResetButton
extends JButton
implements ActionListener {
    private Binarypin app;

    ResetButton(Binarypin binarypin, int n, int n2, int n3, int n4) {
        super("Reset");
        this.app = binarypin;
        this.addActionListener(this);
        this.setBounds(n, n2, n3, n4);
    }

    @Override
    public void actionPerformed(ActionEvent actionEvent) {
        Secret.getInstance().resetInstance();
        this.app.clearOutput();
    }
}