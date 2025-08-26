package model;

public class Main {
    public static void main(String[] args) {
        System.out.println("Starting Appointment Management System...");
        System.out.println("========================================");

        try {
            // Start GUI application
            javax.swing.SwingUtilities.invokeLater(() -> {
                new AppointmentSystemGUI().setVisible(true);
            });
        } catch (Exception e) {
            System.err.println("Error starting the GUI: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}
