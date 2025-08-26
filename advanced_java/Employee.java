package model;

import java.util.Arrays;
import java.util.List;

public class Employee extends Person {
    private static final List<String> VALID_ROLES = Arrays.asList(
        "dentist", "assistant", "receptionist", "administrator"
    );
    private String role;

    public Employee(String name, String username, String password, String role) {
        super(name, username, password);
        this.role = role;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        if (role == null || !VALID_ROLES.contains(role.toLowerCase())) {
            throw new IllegalArgumentException("Invalid role. Valid roles are: " + 
                String.join(", ", VALID_ROLES));
        }
        this.role = role.toLowerCase();
    }

    @Override
    public String toString() {
        return super.toString() + ", Role: " + role;
    }
}