import reflex as rx
from app.components.layout import layout
from app.states.appointment_state import AppointmentState
from app.states.models import Appointment


def status_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "confirmed",
            rx.el.span(
                "Confirmed",
                class_name="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full font-medium",
            ),
        ),
        (
            "pending",
            rx.el.span(
                "Pending",
                class_name="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full font-medium",
            ),
        ),
        (
            "completed",
            rx.el.span(
                "Completed",
                class_name="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full font-medium",
            ),
        ),
        (
            "cancelled",
            rx.el.span(
                "Cancelled",
                class_name="bg-red-100 text-red-800 text-xs px-2 py-1 rounded-full font-medium",
            ),
        ),
        rx.el.span(
            status,
            class_name="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded-full font-medium",
        ),
    )


def appointment_row(appointment: Appointment) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.p(appointment["date"], class_name="font-medium text-gray-900"),
                rx.el.p(
                    f"{appointment['start_time']} - {appointment['end_time']}",
                    class_name="text-sm text-gray-500",
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    appointment["doctor_name"],
                    class_name="text-sm font-medium text-gray-900",
                )
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            status_badge(appointment["status"]),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.a(
                    rx.el.button(
                        "View Details",
                        class_name="text-[#6b2d5b] hover:text-[#5a254c] text-sm font-medium mr-4",
                    ),
                    href=f"/appointment?id={appointment['id']}",
                ),
                rx.cond(
                    (appointment["status"] == "pending")
                    | (appointment["status"] == "confirmed"),
                    rx.el.button(
                        "Cancel",
                        on_click=lambda: AppointmentState.cancel_appointment(
                            appointment["id"]
                        ),
                        class_name="text-red-600 hover:text-red-900 text-sm font-medium",
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
    )


def my_appointments_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "My Appointments", class_name="text-2xl font-bold text-gray-900 mb-2"
            ),
            rx.el.p(
                "Manage your upcoming and past medical appointments.",
                class_name="text-gray-500 mb-8",
            ),
            class_name="mb-8",
        ),
        rx.cond(
            AppointmentState.patient_appointments.length() > 0,
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Date & Time",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Doctor",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Actions",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                        ),
                        class_name="bg-gray-50",
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            AppointmentState.patient_appointments, appointment_row
                        ),
                        class_name="bg-white divide-y divide-gray-200",
                    ),
                    class_name="min-w-full divide-y divide-gray-200",
                ),
                class_name="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden overflow-x-auto",
            ),
            rx.el.div(
                rx.icon("calendar", class_name="w-12 h-12 text-gray-300 mb-3"),
                rx.el.h3(
                    "No appointments found",
                    class_name="text-lg font-medium text-gray-900",
                ),
                rx.el.p(
                    "You haven't booked any appointments yet.",
                    class_name="text-gray-500 mb-6",
                ),
                rx.el.a(
                    rx.el.button(
                        "Find a Doctor",
                        class_name="bg-[#6b2d5b] text-white px-6 py-2 rounded-lg hover:bg-[#5a254c]",
                    ),
                    href="/",
                ),
                class_name="flex flex-col items-center justify-center py-16 bg-white rounded-xl border border-gray-200 border-dashed",
            ),
        ),
        class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
    )


def my_appointments_page() -> rx.Component:
    return layout(my_appointments_content())