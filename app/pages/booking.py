import reflex as rx
from app.components.layout import layout
from app.states.appointment_state import AppointmentState
from app.states.auth_state import AuthState


def booking_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Book Appointment", class_name="text-2xl font-bold text-gray-900 mb-2"
            ),
            rx.el.p(
                f"Schedule a visit with {AppointmentState.booking_doctor_name}",
                class_name="text-gray-500 mb-8",
            ),
            rx.el.form(
                rx.el.input(
                    type="hidden",
                    name="doctor_id",
                    value=AppointmentState.booking_doctor_id,
                ),
                rx.el.input(
                    type="hidden",
                    name="doctor_name",
                    value=AppointmentState.booking_doctor_name,
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Date",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="date",
                            name="date",
                            required=True,
                            class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Time",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="time",
                            name="time",
                            required=True,
                            class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent",
                        ),
                        class_name="mb-4",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Duration",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.select(
                        rx.el.option("30 Minutes", value="30"),
                        rx.el.option("45 Minutes", value="45"),
                        rx.el.option("60 Minutes", value="60"),
                        name="duration",
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent bg-white",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Notes (Optional)",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.textarea(
                        name="notes",
                        placeholder="Briefly describe your symptoms or reason for visit...",
                        rows="4",
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Confirm Booking",
                        type="submit",
                        class_name="w-full bg-[#6b2d5b] text-white py-3 rounded-lg hover:bg-[#5a254c] font-bold shadow-md transition-colors",
                    ),
                    rx.el.a(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            class_name="w-full mt-3 bg-white text-gray-700 border border-gray-300 py-3 rounded-lg hover:bg-gray-50 font-medium transition-colors",
                        ),
                        href="/",
                    ),
                ),
                on_submit=AppointmentState.book_appointment,
                reset_on_submit=True,
            ),
            class_name="bg-white p-8 rounded-2xl shadow-sm border border-gray-200 max-w-2xl mx-auto",
        ),
        class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12",
    )


def booking_page() -> rx.Component:
    return layout(booking_form())