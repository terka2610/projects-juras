package model;

public class Person {
    protected static final int MIN_PASSWORD_LENGTH = 6;
    protected static final int MIN_USERNAME_LENGTH = 3;
	
	protected String name;
	protected String username;
	protected String password;
	
	
	public Person(String name, String username, String password) {
		super();
		this.name = name;
		this.username = username;
		this.password = password;
	}


	public String getName() {
		return name;
	}


	public void setName(String name) {
		this.name = name;
	}


	public String getUsername() {
		return username;
	}


	public void setUsername(String username) {
		this.username = username;
	}


	public String getPassword() {
		return password;
	}


	public void setPassword(String password) {
		if (password == null || password.length() < MIN_PASSWORD_LENGTH) {
			throw new IllegalArgumentException("Password must be at least " + MIN_PASSWORD_LENGTH + " characters long");
		}
		this.password = password;
	}


	@Override
	public String toString() {
		return "Person [name=" + name + ", username=" + username + ", password=" + password + "]";
	}
	
	
	


}
