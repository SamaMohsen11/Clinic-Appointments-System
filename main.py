import threading

N = 3


class Patient:
    def __init__(self, patient_id, name, medical_data=""):
        self.patient_id = patient_id
        self.name = name
        self.__medical_data = medical_data

    def getMedicalData(self, requester):
        if not getattr(requester, "is_authorized_staff", False):
            print("Access denied: only authorized staff can view patient medical data.")
            return None

        return self.__medical_data


class Doctor:
    def __init__(self, doctor_id, name, available_slots, authorized_staff=False):
        self.doctor_id = doctor_id
        self.name = name
        self.available_slots = list(available_slots)
        self.reserved_slots = set()
        self.is_authorized_staff = authorized_staff
        self._slot_lock = threading.Lock()

    def getAvailableSlots(self):
        with self._slot_lock:
            return [
                slot for slot in self.available_slots
                if slot not in self.reserved_slots
            ]

    def isSlotAvailable(self, selectedSlot):
        with self._slot_lock:
            return (
                selectedSlot in self.available_slots
                and selectedSlot not in self.reserved_slots
            )

    def reserveSlot(self, selectedSlot):
        with self._slot_lock:
            if (
                selectedSlot not in self.available_slots
                or selectedSlot in self.reserved_slots
            ):
                return False

            self.reserved_slots.add(selectedSlot)
            return True

    def releaseSlot(self, selectedSlot):
        with self._slot_lock:
            self.reserved_slots.discard(selectedSlot)

    def respondToRequest(self, appointmentRequest, decision, bookingSystem):
        if appointmentRequest.doctor is not self:
            print("This appointment request belongs to another doctor.")
            return False

        return bookingSystem.respondToRequest(
            appointmentRequest, decision, self
        )


class Appointment:
    def __init__(self, patient, doctor, selectedSlot):
        self.patient = patient
        self.doctor = doctor
        self.selected_slot = selectedSlot
        self.status = "Pending"

    @classmethod
    def createRequest(cls, patient, doctor, selectedSlot):
        return cls(patient, doctor, selectedSlot)

    def accept(self):
        if self.status != "Pending":
            return False

        self.status = "Accepted"
        return True

    def decline(self):
        if self.status != "Pending":
            return False

        self.status = "Declined"
        return True


class AppointmentBookingSystem:
    def __init__(self):
        self.appointments = []
        self._booking_lock = threading.RLock()

    def viewAvailableDaysAndTimes(self, doctor):
        availableSlots = doctor.getAvailableSlots()

        print(f"Available days and times for {doctor.name}:")

        if not availableSlots:
            print("  No available slots.")
        else:
            for slot in availableSlots:
                print(f"  {slot}")

        return availableSlots

    def countUpcomingAppointments(self, patient):
        with self._booking_lock:
            return sum(
                appointment.patient is patient
                and appointment.status in ("Pending", "Accepted")
                for appointment in self.appointments
            )

    def requestAppointment(self, patient, doctor, selectedSlot):
        with self._booking_lock:
            if not doctor.isSlotAvailable(selectedSlot):
                self.showSlotUnavailable(doctor, selectedSlot)
                return None

            if self.countUpcomingAppointments(patient) >= N:
                self.showAppointmentLimitReached(patient)
                return None

            # Reserve the slot immediately, including while the request is pending.
            # This prevents another patient from requesting the same time slot.
            if not doctor.reserveSlot(selectedSlot):
                self.showSlotUnavailable(doctor, selectedSlot)
                return None

            appointmentRequest = Appointment.createRequest(
                patient, doctor, selectedSlot
            )
            self.appointments.append(appointmentRequest)

        self.sendAppointmentRequest(appointmentRequest)
        return appointmentRequest

    def sendAppointmentRequest(self, appointmentRequest):
        print(
            f"Request sent to {appointmentRequest.doctor.name} for "
            f"{appointmentRequest.patient.name} at "
            f"{appointmentRequest.selected_slot}."
        )
        print(f"Appointment status: {appointmentRequest.status}.")

    def respondToRequest(self, appointmentRequest, decision, doctor):
        with self._booking_lock:
            if appointmentRequest not in self.appointments:
                print("Appointment request was not found.")
                return False

            if appointmentRequest.doctor is not doctor:
                print("Only the assigned doctor can respond to this request.")
                return False

            if appointmentRequest.status != "Pending":
                print("This appointment request has already been answered.")
                return False

            decision = decision.strip().lower()

            if decision == "accept":
                if appointmentRequest.accept():
                    self.bookingConfirmed(appointmentRequest)
                    return True

            elif decision == "decline":
                if appointmentRequest.decline():
                    doctor.releaseSlot(appointmentRequest.selected_slot)
                    self.bookingDeclined(appointmentRequest)
                    return True

            else:
                print("Invalid decision. Choose 'accept' or 'decline'.")

            return False

    def showSlotUnavailable(self, doctor, selectedSlot):
        print(
            f"Slot unavailable: {selectedSlot} is not available "
            f"with {doctor.name}."
        )

    def showAppointmentLimitReached(self, patient):
        print(
            f"Appointment limit reached: {patient.name} already has "
            f"{N} upcoming appointments."
        )

    def bookingConfirmed(self, appointmentRequest):
        print(
            f"Booking confirmed for {appointmentRequest.patient.name}: "
            f"{appointmentRequest.selected_slot}. "
            f"Status: {appointmentRequest.status}."
        )

    def bookingDeclined(self, appointmentRequest):
        print(
            f"Booking declined for {appointmentRequest.patient.name}: "
            f"{appointmentRequest.selected_slot}. "
            f"Status: {appointmentRequest.status}."
        )


def main():
    print("=== Doctor Appointment Booking System ===")

    doctor = Doctor(
        "D1",
        "Dr. Ahmed",
        [
            "Monday 09:00",
            "Monday 10:00",
            "Tuesday 09:00",
            "Tuesday 10:00",
            "Wednesday 09:00",
            "Wednesday 10:00",
        ],
        authorized_staff=True,
    )

    patient1 = Patient("P1", "Mona", "Sample medical history for Mona")
    patient2 = Patient("P2", "Omar", "Sample medical history for Omar")
    patient3 = Patient("P3", "Salma", "Sample medical history for Salma")

    system = AppointmentBookingSystem()

    print("\n1. View the doctor's available days and times")
    system.viewAvailableDaysAndTimes(doctor)

    print("\n2. Create a request, then try to book its reserved slot again")
    first_request = system.requestAppointment(
        patient1, doctor, "Monday 09:00"
    )

    system.requestAppointment(patient2, doctor, "Monday 09:00")

    if first_request is not None:
        doctor.respondToRequest(first_request, "accept", system)

    print("\n3. The doctor declines another request, releasing that slot")
    declined_request = system.requestAppointment(
        patient2, doctor, "Monday 10:00"
    )

    if declined_request is not None:
        doctor.respondToRequest(declined_request, "decline", system)

    print("\n4. Another patient can request the released slot")
    released_slot_request = system.requestAppointment(
        patient3, doctor, "Monday 10:00"
    )

    if released_slot_request is not None:
        doctor.respondToRequest(released_slot_request, "accept", system)

    print(f"\n5. Fill {patient1.name}'s upcoming appointments up to N = {N}")

    for slot in ("Tuesday 09:00", "Tuesday 10:00"):
        appointmentRequest = system.requestAppointment(patient1, doctor, slot)

        if appointmentRequest is not None:
            doctor.respondToRequest(appointmentRequest, "accept", system)

    print("\n6. Try another available slot after the limit has been reached")
    system.requestAppointment(patient1, doctor, "Wednesday 09:00")

    print("\n7. Check medical-data access")

    unauthorized_data = patient1.getMedicalData(patient2)
    print("Unauthorized access blocked:", unauthorized_data is None)

    authorized_data = patient1.getMedicalData(doctor)
    print("Authorized doctor access:", authorized_data)

    print(
        "\nNote: This console demonstration does not verify the "
        "2-second display target (R6) or mobile usability (R7)."
    )


if __name__ == "__main__":
    main()