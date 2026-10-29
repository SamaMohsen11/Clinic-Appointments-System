sequenceDiagram
    actor Patient
    participant System as Appointment Booking System
    actor Doctor
    participant Appointment

    Patient->>System: viewAvailableDaysAndTimes(doctor)
    System->>Doctor: getAvailableSlots()
    Doctor-->>System: availableSlots
    System-->>Patient: displayAvailableSlots(availableSlots)
    Note over Patient,System: R6: Available appointment times shall be displayed within 2 seconds.

    Patient->>System: requestAppointment(doctor, selectedSlot)
    System->>Doctor: isSlotAvailable(selectedSlot)
    Doctor-->>System: slotAvailable
    System->>System: countUpcomingAppointments(patient)
    System-->>System: upcomingAppointments

    alt Slot is unavailable
        System-->>Patient: showSlotUnavailable()
    else Patient has reached the appointment limit (upcomingAppointments >= 3)
        System-->>Patient: showAppointmentLimitReached()
    else Slot is available and upcomingAppointments < 3
        System->>Appointment: createRequest(patient, doctor, selectedSlot)
        Appointment-->>System: appointmentRequest
        System-->>Doctor: sendAppointmentRequest(appointmentRequest)
        Doctor->>System: respondToRequest(appointmentRequest, decision)
        alt Doctor accepts
            System->>Appointment: accept()
            Appointment-->>System: status = Accepted
            System-->>Patient: bookingConfirmed()
        else Doctor declines
            System->>Appointment: decline()
            Appointment-->>System: status = Declined
            System-->>Patient: bookingDeclined()
        end
    end