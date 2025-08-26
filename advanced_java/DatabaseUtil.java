package model;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class DatabaseUtil {
    private static final String PATIENT_FILE = "src/data/patients.csv";
    private static final String EMPLOYEE_FILE = "src/data/employees.csv";
    
    // Read all patients from CSV file
    public static List<Patient> loadPatients() {
        List<Patient> patients = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(PATIENT_FILE))) {
            String line = reader.readLine(); // Skip header
            while ((line = reader.readLine()) != null) {
                String[] data = line.split(",");
                if (data.length >= 6) {
                    patients.add(new Patient(
                        data[0], // name
                        data[1], // username
                        data[2], // password
                        data[3], // email
                        data[4], // address
                        data[5]  // telephone
                    ));
                }
            }
        } catch (IOException e) {
            System.err.println("Error loading patients: " + e.getMessage());
        }
        return patients;
    }
    
    // Read all employees from CSV file
    public static List<Employee> loadEmployees() {
        List<Employee> employees = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(EMPLOYEE_FILE))) {
            String line = reader.readLine(); // Skip header
            while ((line = reader.readLine()) != null) {
                String[] data = line.split(",");
                if (data.length >= 4) {
                    employees.add(new Employee(
                        data[0], // name
                        data[1], // username
                        data[2], // password
                        data[3]  // role
                    ));
                }
            }
        } catch (IOException e) {
            System.err.println("Error loading employees: " + e.getMessage());
        }
        return employees;
    }
    
    // Save new patient to CSV file
    public static boolean savePatient(Patient patient) {
        try (FileWriter fw = new FileWriter(PATIENT_FILE, true);
             BufferedWriter writer = new BufferedWriter(fw)) {
            writer.newLine();
            writer.write(String.format("%s,%s,%s,%s,%s,%s",
                patient.getName(),
                patient.getUsername(),
                patient.getPassword(),
                patient.getEmail(),
                patient.getAddress(),
                patient.getTelephone()
            ));
            return true;
        } catch (IOException e) {
            System.err.println("Error saving patient: " + e.getMessage());
            return false;
        }
    }
    
    // Save new employee to CSV file
    public static boolean saveEmployee(Employee employee) {
        try (FileWriter fw = new FileWriter(EMPLOYEE_FILE, true);
             BufferedWriter writer = new BufferedWriter(fw)) {
            writer.newLine();
            writer.write(String.format("%s,%s,%s,%s",
                employee.getName(),
                employee.getUsername(),
                employee.getPassword(),
                employee.getRole()
            ));
            return true;
        } catch (IOException e) {
            System.err.println("Error saving employee: " + e.getMessage());
            return false;
        }
    }
    
    // Check if username already exists in either patients or employees
    public static boolean isUsernameAvailable(String username) {
        // Check patients
        for (Patient patient : loadPatients()) {
            if (patient.getUsername().equals(username)) {
                return false;
            }
        }
        // Check employees
        for (Employee employee : loadEmployees()) {
            if (employee.getUsername().equals(username)) {
                return false;
            }
        }
        return true;
    }
}
