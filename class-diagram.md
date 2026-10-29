## Class Diagram

mermaid
classDiagram
    direction LR

    class Patient {
        +patientId: int
        +name: str
        +viewDoctorAvailability(doctor: Doctor) List~TimeSlot~
        +bookAppointment(slot: TimeSlot) Appointment
        +countUpcomingAppointments() int
    }

    class Doctor {
        +doctorId: int
        +name: str
        +getAvailableTimeSlots() List~TimeSlot~
        +acceptAppointment(appointment: Appointment) bool
        +declineAppointment(appointment: Appointment) bool
    }

    class TimeSlot {
        +slotId: int
        +day: date
        +startTime: time
        +endTime: time
        +isAvailable: bool
        +isAvailableForBooking() bool
    }

    class Appointment {
        +appointmentId: int
        +status: str
        +isUpcoming() bool
    }

    class MedicalData {
        +medicalDataId: int
        -record: str
        +readFor(staffId: int, patient: Patient, accessControl: AccessControl) str
    }

    class AccessControl {
        -authorizedStaffIds: Set~int~
        +isAuthorized(staffId: int, patient: Patient) bool
    }

    Patient "1" --> "0..*" Appointment : books
    Doctor "1" --> "0..*" Appointment : reviews
    Doctor "1" --> "0..*" TimeSlot : defines availability
    Appointment "0..*" --> "1" TimeSlot : requests slot
    Patient "1" *-- "0..1" MedicalData : owns
    MedicalData ..> AccessControl : checks authorization before reading