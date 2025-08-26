package model;

import javax.swing.*;
import java.awt.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

//GUI version of the Appointment Management System
public class AppointmentSystemGUI extends JFrame {
    private static final DateTimeFormatter FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm");
    private Calendar calendar;

    public AppointmentSystemGUI() {
        super("Appointment Management System");
        calendar = new Calendar();
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setSize(500, 400);
        setLocationRelativeTo(null);
        showMainMenu();
    }

    private void showMainMenu() {
        getContentPane().removeAll();
        setLayout(new GridLayout(5, 1, 10, 10));

        JButton btnPatientLogin = new JButton("Patient Login");
        JButton btnEmployeeLogin = new JButton("Employee Login");
        JButton btnPatientReg = new JButton("Patient Registration");
        JButton btnEmployeeReg = new JButton("Employee Registration");
        JButton btnExit = new JButton("Exit");

        btnPatientLogin.addActionListener(e -> patientLogin());
        btnEmployeeLogin.addActionListener(e -> employeeLogin());
        btnPatientReg.addActionListener(e -> patientRegistration());
        btnEmployeeReg.addActionListener(e -> employeeRegistration());
        btnExit.addActionListener(e -> System.exit(0));

        add(btnPatientLogin);
        add(btnEmployeeLogin);
        add(btnPatientReg);
        add(btnEmployeeReg);
        add(btnExit);

        revalidate();
        repaint();
    }

    private void patientLogin() {
        JTextField usernameField = new JTextField();
        JPasswordField passwordField = new JPasswordField();
        Object[] message = {"Username:", usernameField, "Password:", passwordField};

        int option = JOptionPane.showConfirmDialog(this, message, "Patient Login", JOptionPane.OK_CANCEL_OPTION);
        if (option == JOptionPane.OK_OPTION) {
            Patient p = calendar.authenticatePatient(usernameField.getText(), new String(passwordField.getPassword()));
            if (p != null) {
                JOptionPane.showMessageDialog(this, "Welcome " + p.getName());
                showPatientMenu(p);
            } else {
                JOptionPane.showMessageDialog(this, "Invalid credentials!", "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void employeeLogin() {
        JTextField usernameField = new JTextField();
        JPasswordField passwordField = new JPasswordField();
        Object[] message = {"Username:", usernameField, "Password:", passwordField};

        int option = JOptionPane.showConfirmDialog(this, message, "Employee Login", JOptionPane.OK_CANCEL_OPTION);
        if (option == JOptionPane.OK_OPTION) {
            Employee e = calendar.authenticateEmployee(usernameField.getText(), new String(passwordField.getPassword()));
            if (e != null) {
                JOptionPane.showMessageDialog(this, "Welcome " + e.getName() + " (" + e.getRole() + ")");
                showEmployeeMenu();
            } else {
                JOptionPane.showMessageDialog(this, "Invalid credentials!", "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void patientRegistration() {
        JTextField name = new JTextField();
        JTextField username = new JTextField();
        JPasswordField password = new JPasswordField();
        JTextField email = new JTextField();
        JTextField address = new JTextField();
        JTextField telephone = new JTextField();

        Object[] fields = {"Name:", name, "Username:", username, "Password:", password,
                "Email:", email, "Address:", address, "Telephone:", telephone};

        int option = JOptionPane.showConfirmDialog(this, fields, "Register Patient", JOptionPane.OK_CANCEL_OPTION);
        if (option == JOptionPane.OK_OPTION) {
            if (RegistrationService.registerPatient(name.getText(), username.getText(),
                    new String(password.getPassword()), email.getText(), address.getText(), telephone.getText())) {
                calendar = new Calendar(); // reload
                JOptionPane.showMessageDialog(this, "Patient registered successfully!");
            } else {
                JOptionPane.showMessageDialog(this, "Registration failed!", "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void employeeRegistration() {
        JTextField name = new JTextField();
        JTextField username = new JTextField();
        JPasswordField password = new JPasswordField();
        JTextField role = new JTextField();

        Object[] fields = {"Name:", name, "Username:", username, "Password:", password,
                "Role:", role};

        int option = JOptionPane.showConfirmDialog(this, fields, "Register Employee", JOptionPane.OK_CANCEL_OPTION);
        if (option == JOptionPane.OK_OPTION) {
            if (RegistrationService.registerEmployee(name.getText(), username.getText(),
                    new String(password.getPassword()), role.getText())) {
                calendar = new Calendar();
                JOptionPane.showMessageDialog(this, "Employee registered successfully!");
            } else {
                JOptionPane.showMessageDialog(this, "Registration failed!", "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void showPatientMenu(Patient patient) {
        String[] options = {"View My Appointments", "Add Appointment", "Cancel Appointment", "My Profile", "Back"};
        while (true) {
            int choice = JOptionPane.showOptionDialog(this, "Patient Menu", "Patient Menu",
                    JOptionPane.DEFAULT_OPTION, JOptionPane.PLAIN_MESSAGE, null, options, options[0]);

            if (choice == 0) { // view appointments
                List<Appointment> list = calendar.getAppointments();
                StringBuilder sb = new StringBuilder();
                for (Appointment a : list) {
                    if (a.getPatient().equals(patient)) {
                        sb.append(a.getDateTime().format(FORMATTER)).append("\n");
                    }
                }
                JOptionPane.showMessageDialog(this, sb.length() == 0 ? "No appointments" : sb.toString());
            } else if (choice == 1) {
                LocalDateTime dt = CalendarGUI.showDialog(this, LocalDateTime.now().plusDays(1).withMinute(0));
                if (dt != null) {
                    if (dt.isBefore(LocalDateTime.now())) {
                        javax.swing.JOptionPane.showMessageDialog(this, "Time must be in the future");
                    } else {
                        java.util.List<Integer> details = new java.util.ArrayList<>();
                        details.add(1);
                        if (calendar.addAppointment(patient, dt, details)) {
                            javax.swing.JOptionPane.showMessageDialog(this, "Added!");
                        } else {
                            javax.swing.JOptionPane.showMessageDialog(this, "Failed to add");
                        }
                    }
                }
            } else if (choice == 2) { // cancel
                String dateStr = JOptionPane.showInputDialog(this, "Enter datetime to cancel:");
                try {
                    LocalDateTime dt = LocalDateTime.parse(dateStr, FORMATTER);
                    if (calendar.removeAppointment(patient, dt)) {
                        JOptionPane.showMessageDialog(this, "Cancelled!");
                    } else {
                        JOptionPane.showMessageDialog(this, "No matching appointment");
                    }
                } catch (Exception ex) {
                    JOptionPane.showMessageDialog(this, "Invalid format");
                }
            } else if (choice == 3) { // profile
                JOptionPane.showMessageDialog(this, patient.toString());
            } else {
                return;
            }
        }
    }

    private void showEmployeeMenu() {
        String[] options = {"View All Patients", "View All Appointments", "Back"};
        while (true) {
            int choice = JOptionPane.showOptionDialog(this, "Employee Menu", "Employee Menu",
                    JOptionPane.DEFAULT_OPTION, JOptionPane.PLAIN_MESSAGE, null, options, options[0]);
            if (choice == 0) {
                StringBuilder sb = new StringBuilder();
                for (Patient p : calendar.getPatientList()) {
                    sb.append(p.getName()).append(" - ").append(p.getEmail()).append("\n");
                }
                JOptionPane.showMessageDialog(this, sb.length() == 0 ? "No patients" : sb.toString());
            } else if (choice == 1) {
                StringBuilder sb = new StringBuilder();
                for (Appointment a : calendar.getAppointments()) {
                    sb.append(a.getPatient().getName()).append(" - ").append(a.getDateTime().format(FORMATTER)).append("\n");
                }
                JOptionPane.showMessageDialog(this, sb.length() == 0 ? "No appointments" : sb.toString());
            } else {
                return;
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new AppointmentSystemGUI().setVisible(true));
    }
}
