package model;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Scanner;

public class PatientMenu {
    private Scanner scanner;
    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm");

    public PatientMenu() {
        this.scanner = new Scanner(System.in);
    }

    public void menuP(Patient patient, Calendar calendar) {
        while (true) {
            System.out.println("\n=== Patient Menu ===");
            System.out.println("1. View My Appointments");
            System.out.println("2. Cancel Appointment");
            System.out.println("3. View My Profile");
            System.out.println("4. Exit");
            System.out.print("Enter your choice: ");

            int choice = scanner.nextInt();
            scanner.nextLine(); // Consume newline

            switch (choice) {
                case 1:
                    myAppointments(calendar, patient);
                    break;
                case 2:
                    cancelAppointment(calendar, patient);
                    break;
                case 3:
                    showProfile(patient);
                    break;
                case 4:
                    return;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        }
    }

    public void myAppointments(Calendar calendar, Patient patient) {
        List<Appointment> appointments = calendar.getAppointments();
        boolean hasAppointments = false;

        System.out.println("\n=== My Appointments ===");
        for (Appointment appointment : appointments) {
            if (appointment.getPatient().equals(patient)) {
                System.out.println("Date/Time: " + appointment.getDateTime().format(formatter));
                System.out.println("------------------------");
                hasAppointments = true;
            }
        }

        if (!hasAppointments) {
            System.out.println("You have no appointments scheduled.");
        }
    }

    public void cancelAppointment(Calendar calendar, Patient patient) {
        List<Appointment> appointments = calendar.getAppointments();
        boolean hasAppointments = false;

        System.out.println("\n=== Your Appointments ===");
        for (Appointment appointment : appointments) {
            if (appointment.getPatient().equals(patient)) {
                System.out.println("Date/Time: " + appointment.getDateTime().format(formatter));
                hasAppointments = true;
            }
        }

        if (!hasAppointments) {
            System.out.println("You have no appointments to cancel.");
            return;
        }

        System.out.print("Enter appointment date/time to cancel (yyyy-MM-dd HH:mm): ");
        String dateTimeStr = scanner.nextLine();
        try {
            LocalDateTime dateTime = LocalDateTime.parse(dateTimeStr, formatter);
            boolean appointmentFound = appointments.stream()
                .anyMatch(a -> a.getPatient().equals(patient) && a.getDateTime().equals(dateTime));
            if (appointmentFound) {
                if (calendar.removeAppointment(patient, dateTime)) {
                    System.out.println("Appointment cancelled successfully.");
                } else {
                    System.out.println("Failed to cancel appointment. Please try again.");
                }
            } else {
                System.out.println("No matching appointment found for the given date and time.");
            }
        } catch (Exception e) {
            System.out.println("Invalid date/time format. Please use yyyy-MM-dd HH:mm (e.g., 2025-08-12 21:49).");
        }
    }

    private void showProfile(Patient patient) {
        System.out.println("\n=== My Profile ===");
        System.out.println("Name: " + patient.getName());
        System.out.println("Email: " + patient.getEmail());
        System.out.println("Address: " + patient.getAddress());
        System.out.println("Telephone: " + patient.getTelephone());
    }
}
