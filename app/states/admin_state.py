import reflex as rx
from app.states.auth_state import AuthState
from app.states.appointment_state import AppointmentState


class AdminState(rx.State):
    @rx.var
    async def total_users(self) -> int:
        auth_state = await self.get_state(AuthState)
        return len(auth_state.users)

    @rx.var
    async def total_appointments(self) -> int:
        appt_state = await self.get_state(AppointmentState)
        return len(appt_state.appointments)

    @rx.var
    async def recent_appointments(self) -> list:
        appt_state = await self.get_state(AppointmentState)
        return sorted(appt_state.appointments, key=lambda x: x["date"], reverse=True)[
            :5
        ]

    @rx.event
    async def delete_user(self, user_id: str):
        auth_state = await self.get_state(AuthState)
        auth_state.users = [u for u in auth_state.users if u["id"] != user_id]