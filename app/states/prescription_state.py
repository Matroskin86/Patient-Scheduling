import reflex as rx
from app.states.models import Prescription
from app.states.auth_state import AuthState
import datetime


class PrescriptionState(rx.State):
    prescriptions: list[Prescription] = [
        {
            "id": "rx1",
            "patient_id": "u1",
            "patient_name": "John Doe",
            "doctor_id": "d1",
            "doctor_name": "Dr. Sarah Smith",
            "medication": "Amoxicillin",
            "dosage": "500mg",
            "instructions": "Take one capsule three times a day for 7 days.",
            "date": "2024-11-10",
            "status": "Active",
        },
        {
            "id": "rx2",
            "patient_id": "u1",
            "patient_name": "John Doe",
            "doctor_id": "d3",
            "doctor_name": "Dr. Emily Chen",
            "medication": "Hydrocortisone Cream",
            "dosage": "1%",
            "instructions": "Apply to affected area twice daily.",
            "date": "2024-11-20",
            "status": "Refill Requested",
        },
    ]
    issue_patient_id: str = ""
    issue_medication: str = ""
    issue_dosage: str = ""
    issue_instructions: str = ""

    @rx.var
    async def my_prescriptions(self) -> list[Prescription]:
        auth_state = await self.get_state(AuthState)
        if not auth_state.current_user:
            return []
        return [
            p
            for p in self.prescriptions
            if p["patient_id"] == auth_state.current_user["id"]
        ]

    @rx.var
    async def doctor_prescriptions(self) -> list[Prescription]:
        auth_state = await self.get_state(AuthState)
        if not auth_state.current_user or auth_state.current_user["role"] != "doctor":
            return []
        return [
            p
            for p in self.prescriptions
            if p["doctor_name"] == auth_state.current_user["name"]
        ]

    @rx.event
    def request_refill(self, rx_id: str):
        for p in self.prescriptions:
            if p["id"] == rx_id:
                p["status"] = "Refill Requested"
                rx.toast.info("Refill requested sent to doctor.")
                break

    @rx.event
    def set_issue_patient(self, value: str):
        self.issue_patient_id = value

    @rx.event
    def set_issue_medication(self, value: str):
        self.issue_medication = value

    @rx.event
    def set_issue_dosage(self, value: str):
        self.issue_dosage = value

    @rx.event
    def set_issue_instructions(self, value: str):
        self.issue_instructions = value

    @rx.event
    async def issue_prescription(self):
        auth_state = await self.get_state(AuthState)
        from app.states.auth_state import AuthState as AuthStateClass

        patient_name = "Unknown Patient"
        all_users = auth_state.users
        for u in all_users:
            if u["id"] == self.issue_patient_id:
                patient_name = u["name"]
                break
        new_rx: Prescription = {
            "id": f"rx{len(self.prescriptions) + 1}",
            "patient_id": self.issue_patient_id,
            "patient_name": patient_name,
            "doctor_id": auth_state.current_user["id"],
            "doctor_name": auth_state.current_user["name"],
            "medication": self.issue_medication,
            "dosage": self.issue_dosage,
            "instructions": self.issue_instructions,
            "date": datetime.date.today().isoformat(),
            "status": "Active",
        }
        self.prescriptions.insert(0, new_rx)
        self.issue_medication = ""
        self.issue_dosage = ""
        self.issue_instructions = ""
        return rx.toast.success("Prescription issued successfully.")

    @rx.event
    def approve_refill(self, rx_id: str):
        for p in self.prescriptions:
            if p["id"] == rx_id:
                p["status"] = "Active"
                rx.toast.success("Refill approved.")
                break