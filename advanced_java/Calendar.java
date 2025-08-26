package model;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

public class Calendar {
    private List<Appointment> appointmentList = new ArrayList<>();
    private List<Patient> patientList = new ArrayList<>();
    private List<Employee> employeeList = new ArrayList<>();
    private Hashtable<Integer, String> appointmentPatient = new Hashtable<>();

    public List<Patient> getPatientList() {
        return new ArrayList<>(patientList); 
    }
    public List<Appointment> getAppointmentList() {
		return appointmentList;
	}
	public void setAppointmentList(List<Appointment> appointmentList) {
		this.appointmentList = appointmentList;
	}
	public List<Employee> getEmployeeList() {
		return employeeList;
	}
	public void setEmployeeList(List<Employee> employeeList) {
		this.employeeList = employeeList;
	}
	public Hashtable<Integer, String> getAppointmentPatient() {
		return appointmentPatient;
	}
	public void setAppointmentPatient(Hashtable<Integer, String> appointmentPatient) {
		this.appointmentPatient = appointmentPatient;
	}
	public void setPatientList(List<Patient> patientList) {
		this.patientList = patientList;
	}
	public List<Appointment> getAppointments() {
        return new ArrayList<>(appointmentList);
    }
    public boolean removeAppointment(Patient patient, LocalDateTime dateTime) {
        return appointmentList.removeIf(appointment ->
            appointment.getPatient().equals(patient) && appointment.getDateTime().equals(dateTime));
    }

    public boolean addPatient(Patient patient) {
        if (patient != null && !patientList.contains(patient)) {
            patientList.add(patient);
            if (patient.getId() != null && patient.getName() != null) {
                appointmentPatient.put((Integer) patient.getId(), patient.getName());
            }
            return true;
        }
        return false;
    }

    public boolean addAppointment(Patient patient, List<Integer> appointmentDetails) {
        if (patient != null && appointmentDetails != null) {
            Appointment appointment = new Appointment(patient, appointmentDetails);
            appointmentList.add(appointment);
            return true;
        }
        return false;
    }

    public boolean updateDateTime(Patient patient, LocalDateTime oldDateTime, LocalDateTime newDateTime) {
        for (Appointment appointment : appointmentList) {
            if (appointment.getPatient().equals(patient) && appointment.getDateTime().equals(oldDateTime)) {
                appointment.setDateTime(newDateTime);
                return true;
            }
        }
        return false;
    }

}