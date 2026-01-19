import reflex as rx
from app.components.layout import layout
from app.states.appointment_state import AppointmentState
from app.states.auth_state import AuthState
from app.pages.my_appointments import status_badge


def detail_content() -> rx.Component:
    appointment = AppointmentState.current_appointment
    return rx.cond(
        appointment,
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    "Back to My Appointments",
                    href="/my-appointments",
                    class_name="text-sm text-gray-500 hover:text-[#6b2d5b] mb-6 inline-block",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h1(
                                "Appointment Details",
                                class_name="text-2xl font-bold text-gray-900",
                            ),
                            status_badge(appointment["status"]),
                            class_name="flex justify-between items-center mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.span(
                                    "Date & Time",
                                    class_name="block text-sm font-medium text-gray-500 mb-1",
                                ),
                                rx.el.p(
                                    f"{appointment['date']} at {appointment['start_time']}",
                                    class_name="text-lg font-medium text-gray-900",
                                ),
                                class_name="mb-6",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Doctor",
                                    class_name="block text-sm font-medium text-gray-500 mb-1",
                                ),
                                rx.el.p(
                                    appointment["doctor_name"],
                                    class_name="text-lg font-medium text-gray-900",
                                ),
                                class_name="mb-6",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Patient",
                                    class_name="block text-sm font-medium text-gray-500 mb-1",
                                ),
                                rx.el.p(
                                    appointment["patient_name"],
                                    class_name="text-lg font-medium text-gray-900",
                                ),
                                class_name="mb-6",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Reason for Visit",
                                    class_name="block text-sm font-medium text-gray-500 mb-1",
                                ),
                                rx.el.p(
                                    appointment["notes"] | "No notes provided.",
                                    class_name="text-gray-700 bg-gray-50 p-4 rounded-lg",
                                ),
                                class_name="mb-8",
                            ),
                            class_name="",
                        ),
                        rx.el.div(
                            rx.cond(
                                (appointment["status"] != "cancelled")
                                & (appointment["status"] != "completed"),
                                rx.el.div(
                                    rx.cond(
                                        AuthState.current_user["role"] == "doctor",
                                        rx.el.div(
                                            rx.el.button(
                                                "Complete Appointment",
                                                on_click=lambda: AppointmentState.update_status(
                                                    appointment["id"], "completed"
                                                ),
                                                class_name="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 font-medium mr-4",
                                            ),
                                            rx.el.button(
                                                "Cancel Appointment",
                                                on_click=lambda: AppointmentState.cancel_appointment(
                                                    appointment["id"]
                                                ),
                                                class_name="bg-white text-red-600 border border-red-200 px-4 py-2 rounded-lg hover:bg-red-50 font-medium",
                                            ),
                                            class_name="flex",
                                        ),
                                        rx.el.button(
                                            "Cancel Appointment",
                                            on_click=lambda: AppointmentState.cancel_appointment(
                                                appointment["id"]
                                            ),
                                            class_name="bg-white text-red-600 border border-red-200 px-4 py-2 rounded-lg hover:bg-red-50 font-medium",
                                        ),
                                    ),
                                    class_name="border-t border-gray-100 pt-6",
                                ),
                            ),
                            class_name="",
                        ),
                        class_name="bg-white rounded-2xl p-8 shadow-sm border border-gray-200",
                    ),
                    class_name="max-w-3xl mx-auto",
                ),
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
        ),
        rx.el.div("Loading...", class_name="text-center py-10 text-gray-500"),
    )


def appointment_detail_page() -> rx.Component:
    return layout(detail_content())