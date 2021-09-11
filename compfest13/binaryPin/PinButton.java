/*
 * Decompiled with CFR 0.150.
 */
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;

class PinButton
extends JButton
implements ActionListener {
    Binarypin app;

    PinButton(Binarypin binarypin, String string, int n, int n2, int n3, int n4) {
        super(string);
        this.app = binarypin;
        this.addActionListener(this);
        this.setBounds(n, n2, n3, n4);
    }

    @Override
    public void actionPerformed(ActionEvent actionEvent) {
        Secret.getInstance().process(this.getText().charAt(0));
        this.app.updateOutput();
    }
}