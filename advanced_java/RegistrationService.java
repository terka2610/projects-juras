package model;

public class RegistrationService {
    
    public static boolean registerPatient(String name, String username, String password, 
                                        String email, String address, String telephone) {
        try {
            // Check if username is available
            if (!DatabaseUtil.isUsernameAvailable(username)) {
                throw new IllegalArgumentException("Username already exists");
            }
            
            // Create new patient
            Patient patient = new Patient(name, username, password, email, address, telephone);
            
            // Save to database
            return DatabaseUtil.savePatient(patient);
            
        } catch (IllegalArgumentException e) {
            System.err.println("Registration error: " + e.getMessage());
            return false;
        }
    }
    
    public static boolean registerEmployee(String name, String username, String password, String role) {
        try {
            // Check if username is available
            if (!DatabaseUtil.isUsernameAvailable(username)) {
                throw new IllegalArgumentException("Username already exists");
            }
            
            // Create new employee
            Employee employee = new Employee(name, username, password, role);
            
            // Save to database
            return DatabaseUtil.saveEmployee(employee);
            
        } catch (IllegalArgumentException e) {
            System.err.println("Registration error: " + e.getMessage());
            return false;
        }
    }
}
