package com.combind;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class SwingBasics {
	private JButton buttonMsg;
	private JPanel panelMain;

	public SwingBasics() {
		buttonMsg.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				JOptionPane.showMessageDialog(null, "Hello from SWING");
			}
		});
	}

	public static void main(String[] args) {
		JFrame frame = new JFrame("SwingBasics");
		frame.setContentPane(new SwingBasics().panelMain);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.pack();
		frame.setVisible(true);
	}
}
