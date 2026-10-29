System: Clinic Appointment Booking System

1. Use Case Table

UC | Name | Actor | Requirement | Use Case Text ("As Actor I do")
UC1 | View doctor availability | Patient | R1 | As a Patient, I view the days and times when a doctor is available.
UC2 | Book appointment | Patient | R2 | As a Patient, I select an available time slot and submit an appointment request.
UC3 | Accept or decline appointment request | Doctor | R3 | As a Doctor, I review an appointment request and accept or decline it.
UC4 | Check upcoming appointment limit | System | R4 | As the System, I check the patient's number of upcoming appointments and prevent another booking if the patient has already reached the limit of 3.
UC5 | Notify patient of declined appointment | System | R3 | As the System, I notify the patient when the doctor declines an appointment request.

2. UC2 — Book Appointment

Primary Actor: Patient
Requirement: R2
Precondition: The patient can access the Clinic Appointment Booking System.

Main Flow:
1. The patient views the doctor's available days and times using UC1.
2. The patient selects a doctor and an available time slot.
3. The patient submits an appointment request for the selected time slot.
4. The system invokes UC4 to check the patient's number of upcoming appointments.
5. If the patient has fewer than 3 upcoming appointments, the system allows the request to proceed to the doctor.
6. The doctor reviews the request using UC3.
7. The doctor accepts the appointment request.
8. The appointment is booked and counted as an upcoming appointment for the patient.

3. Alternative Flows

Alternative Flow 1 — Patient Has Reached the Appointment Limit
Extension point: Step 4 of the main flow.
1. The system checks the patient's number of upcoming appointments.
2. The system determines that the patient already has 3 upcoming appointments.
3. The system prevents the patient from booking another appointment.
4. The request does not proceed to the doctor, and the use case ends.

Result: The patient cannot exceed the maximum of 3 upcoming appointments.

Alternative Flow 2 — Doctor Declines the Appointment Request
Extension point: Step 7 of the main flow.
1. The doctor declines the appointment request.
2. The system invokes UC5.
3. The system notifies the patient that the appointment request was declined.
4. The requested appointment is not booked, and the use case ends.

Result: The patient is notified of the declined request, and no appointment is booked from that request.




flowchart LR
    P([Patient])
    D([Doctor])

    subgraph CAS["Clinic Appointment Booking System"]
        UC1[UC1 View doctor availability]
        UC2[UC2 Book appointment]
        UC3[UC3 Accept or decline appointment request]
        UC4[UC4 Check upcoming appointment limit]
        UC5[UC5 Notify patient of declined appointment]
    end

    P --- UC1
    P --- UC2
    UC3 --- D

    UC2 -.->|"«include»"| UC4
    UC5 -.->|"«extend»"| UC3