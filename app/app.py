import reflex as rx
from app.pages.index import index
from app.pages.auth import login_page, register_page
from app.pages.doctor_detail import doctor_detail_page
from app.states.doctor_state import DoctorState

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.title("MediConnect - Patient Scheduling System"),
    ],
)
app.add_page(index, route="/")
app.add_page(login_page, route="/login")
app.add_page(register_page, route="/register")
app.add_page(
    doctor_detail_page, route="/doctor", on_load=DoctorState.load_doctor_detail
)
from app.pages.booking import booking_page
from app.pages.my_appointments import my_appointments_page
from app.pages.appointment_detail import appointment_detail_page
from app.pages.doctor_dashboard import doctor_dashboard_page
from app.states.appointment_state import AppointmentState

app.add_page(
    booking_page, route="/book-appointment", on_load=AppointmentState.load_booking_page
)
app.add_page(my_appointments_page, route="/my-appointments")
app.add_page(doctor_dashboard_page, route="/doctor-dashboard")
app.add_page(
    appointment_detail_page,
    route="/appointment",
    on_load=AppointmentState.load_appointment_detail,
)
from app.pages.my_documents import my_documents_page
from app.pages.my_prescriptions import my_prescriptions_page
from app.pages.messaging import messaging_page
from app.pages.admin_dashboard import admin_dashboard_page
from app.pages.doctor_profile import doctor_profile_page

app.add_page(my_documents_page, route="/my-documents")
app.add_page(my_prescriptions_page, route="/my-prescriptions")
app.add_page(messaging_page, route="/messages")
app.add_page(admin_dashboard_page, route="/admin")
app.add_page(doctor_profile_page, route="/doctor-profile")