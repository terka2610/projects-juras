package model;

import java.util.regex.Pattern;

public class Patient extends Person{
	private static final Pattern EMAIL_PATTERN = Pattern.compile(
		"^[A-Za-z0-9+_.-]+@(.+)$");
	private static final Pattern PHONE_PATTERN = Pattern.compile(
		"^\\d{10}$");
	
	private String email;
	private String address;
	private String telephone;
	
	
	public Patient(String name, String username, String password, String email, String address, String telephone) {
		super(name, username, password);
		this.email = email;
		this.address = address;
		this.telephone = telephone;
	}


	public String getEmail() {
		return email;
	}


	public void setEmail(String email) {
		if (email == null || !EMAIL_PATTERN.matcher(email).matches()) {
			throw new IllegalArgumentException("Invalid email format");
		}
		this.email = email;
	}


	public String getAddress() {
		return address;
	}


	public void setAddress(String address) {
		this.address = address;
	}


	public String getTelephone() {
		return telephone;
	}


	public void setTelephone(String telephone) {
		if (telephone == null || !PHONE_PATTERN.matcher(telephone).matches()) {
			throw new IllegalArgumentException("Phone number must be 10 digits");
		}
		this.telephone = telephone;
	}


	@Override
	public String toString() {
		return "Patient [name=" + name + ", username=" + username + ", password=" + password + 
			   ", email=" + email + ", address=" + address + ", telephone=" + telephone + "]";
	}


    public Object getId() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getId'");
    }
	
	
	
	

}
