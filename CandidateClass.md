Constraint: N = 3
Actors: Patient and Doctor

| Class | Evidence | Classification | Why |

| Patient | R1, R2, R4 | Explicit | Directly mentioned in the requirements. Views doctor availability, books appointments, and is subject to the maximum of three upcoming appointments. |
| Doctor | R1, R3 | Explicit | Directly mentioned in the requirements. Has available time slots and can accept or decline appointment requests. |
| Appointment | R2, R3, R4 | Explicit | Directly mentioned in the requirements. Represents a booking and its status, such as pending, accepted, or declined. It also supports counting upcoming appointments. |
| TimeSlot | R1, R2 | Explicit | Represents an available day and time during which a patient can book an appointment. |
| MedicalData | R5 | Explicit | Patient medical data is directly mentioned and must be protected from unauthorized access. |
| AccessControl | R5 | Inferred | Supports checking authorization before allowing access to medical data. It is needed to enforce the access restriction. |
| AppointmentLimitRule | R4, N = 3 | Rejected | The maximum of three upcoming appointments is a business rule, not necessarily a separate class. The booking process can validate this rule. |
| PerformanceMonitor | R6 | Rejected | R6 specifies a response-time target of two seconds, which is a non-functional requirement rather than a domain class. |
| MobileScreen | R7 | Rejected | R7 specifies mobile usability, which is a user-interface design concern rather than a domain class. |
| Payment | No supporting requirement | Rejected | Payment functionality is not specified. |
| Prescription | No supporting requirement | Rejected | Prescription functionality is not specified. |
| Billing | No supporting requirement | Rejected | Billing functionality is not specified. |
| Notification | No supporting requirement | Rejected | Notification functionality is not specified. |

Classification rules:
- Explicit: Classes directly mentioned in the requirements or use cases.
- Inferred: Classes needed to support the required system behavior.
- Rejected: Classes that are not justified as separate classes by the requirements.
