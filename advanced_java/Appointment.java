package model;

import java.time.LocalDateTime;
import java.util.List;

public class Appointment {
        private Patient patient;
        private LocalDateTime dateTime;
        public List<Integer> getDetails() {
			return details;
		}

		public void setDetails(List<Integer> details) {
			this.details = details;
		}

		public void setPatient(Patient patient) {
			this.patient = patient;
		}
		private List<Integer> details;

        public Appointment(Patient patient, List<Integer> details) {
            this.patient = patient;
            this.dateTime = LocalDateTime.now(); 
            this.details = details;
        }

        public Patient getPatient() { return patient; }
        public LocalDateTime getDateTime() { return dateTime; }
        public void setDateTime(LocalDateTime dateTime) { this.dateTime = dateTime; }
    }
