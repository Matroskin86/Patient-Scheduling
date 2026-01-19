import reflex as rx
from typing import Optional
from app.states.models import Appointment
from app.states.auth_state import AuthState
from app.states.doctor_state import DoctorState
import datetime
import logging


class AppointmentState(rx.State):
    appointments: list[Appointment] = [
        {
            "id": "a1",
            "patient_id": "u1",
            "patient_name": "John Doe",
            "doctor_id": "d1",
            "doctor_name": "Dr. Sarah Smith",
            "date": "2024-11-15",
            "start_time": "09:00",
            "end_time": "09:30",
            "duration": 30,
            "notes": "Regular checkup",
            "status": "confirmed",
        },
        {
            "id": "a2",
            "patient_id": "u1",
            "patient_name": "John Doe",
            "doctor_id": "d3",
            "doctor_name": "Dr. Emily Chen",
            "date": "2024-11-20",
            "start_time": "14:00",
            "end_time": "14:45",
            "duration": 45,
            "notes": "Skin rash consultation",
            "status": "pending",
        },
    ]
    booking_doctor_id: str = ""
    booking_doctor_name: str = ""
    current_appointment_id: str = ""

    @rx.var
    async def patient_appointments(self) -> list[Appointment]:
        auth_state = await self.get_state(AuthState)
        if not auth_state.current_user:
            return []
        user_id = auth_state.current_user["id"]
        return [a for a in self.appointments if a["patient_id"] == user_id]

    @rx.var
    async def doctor_appointments(self) -> list[Appointment]:
        auth_state = await self.get_state(AuthState)
        doctor_state = await self.get_state(DoctorState)
        if not auth_state.current_user or auth_state.current_user["role"] != "doctor":
            return []
        current_doc = next(
            (
                d
                for d in doctor_state.doctors
                if d["user_id"] == auth_state.current_user["id"]
            ),
            None,
        )
        if not current_doc:
            return []
        return [a for a in self.appointments if a["doctor_id"] == current_doc["id"]]

    @rx.var
    def current_appointment(self) -> Optional[Appointment]:
        return next(
            (a for a in self.appointments if a["id"] == self.current_appointment_id),
            None,
        )

    @rx.event
    def set_booking_doctor(self, doctor_id: str, doctor_name: str):
        self.booking_doctor_id = doctor_id
        self.booking_doctor_name = doctor_name

    @rx.event
    def load_booking_page(self):
        doctor_id = self.router.url.query_parameters.get("doctor_id")
        doctor_name = self.router.url.query_parameters.get("doctor_name")
        if doctor_id:
            self.booking_doctor_id = doctor_id
        if doctor_name:
            self.booking_doctor_name = doctor_name

    @rx.event
    def load_appointment_detail(self):
        self.current_appointment_id = self.router.url.query_parameters.get("id") or ""

    @rx.event
    async def book_appointment(self, form_data: dict):
        auth_state = await self.get_state(AuthState)
        if not auth_state.current_user:
            return rx.redirect("/login")
        doctor_id = form_data.get("doctor_id")
        date = form_data.get("date")
        time = form_data.get("time")
        duration = int(form_data.get("duration", "30"))
        notes = form_data.get("notes", "")
        doctor_name = form_data.get("doctor_name")
        try:
            h, m = map(int, time.split(":"))
            total_minutes = h * 60 + m + duration
            end_h = total_minutes // 60
            end_m = total_minutes % 60
            end_time = f"{end_h:02d}:{end_m:02d}"
        except Exception as e:
            logging.exception(f"Error calculating end time: {e}")
            end_time = time
        new_appointment: Appointment = {
            "id": f"a{len(self.appointments) + 1}",
            "patient_id": auth_state.current_user["id"],
            "patient_name": auth_state.current_user["name"],
            "doctor_id": doctor_id,
            "doctor_name": doctor_name,
            "date": date,
            "start_time": time,
            "end_time": end_time,
            "duration": duration,
            "notes": notes,
            "status": "pending",
        }
        self.appointments.append(new_appointment)
        return rx.redirect("/my-appointments")

    @rx.event
    def cancel_appointment(self, appointment_id: str):
        for appointment in self.appointments:
            if appointment["id"] == appointment_id:
                appointment["status"] = "cancelled"
                break

    @rx.event
    def update_status(self, appointment_id: str, new_status: str):
        for appointment in self.appointments:
            if appointment["id"] == appointment_id:
                appointment["status"] = new_status
                break