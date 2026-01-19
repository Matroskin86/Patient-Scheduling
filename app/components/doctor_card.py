import reflex as rx
from app.states.doctor_state import DoctorState
from app.states.models import Doctor


def doctor_card(doctor: Doctor) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=doctor["image"],
                    class_name="w-24 h-24 rounded-full border-4 border-white shadow-md bg-gray-100 object-cover mx-auto sm:mx-0 sm:mr-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            doctor["name"],
                            class_name="text-lg font-bold text-gray-900 mb-1 text-center sm:text-left",
                        ),
                        rx.el.span(
                            doctor["specialty"],
                            class_name="bg-indigo-50 text-indigo-700 text-xs px-2 py-1 rounded-full font-medium inline-block mb-2",
                        ),
                    ),
                    rx.el.div(
                        rx.icon("map-pin", class_name="w-4 h-4 text-gray-400 mr-1"),
                        rx.el.span(
                            f"{doctor['city']}, {doctor['state']}",
                            class_name="text-sm text-gray-500",
                        ),
                        class_name="flex items-center justify-center sm:justify-start mb-3",
                    ),
                    rx.el.p(
                        doctor["bio"][:100] + "...",
                        class_name="text-sm text-gray-600 leading-relaxed mb-4 text-center sm:text-left",
                    ),
                    class_name="flex-1",
                ),
                class_name="flex flex-col sm:flex-row items-center sm:items-start",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Consultation Rate:", class_name="text-xs text-gray-500 block"
                    ),
                    rx.el.span(
                        doctor["rates"], class_name="font-semibold text-gray-900"
                    ),
                    class_name="text-center sm:text-left mb-4 sm:mb-0",
                ),
                rx.el.div(
                    rx.el.a(
                        rx.el.button(
                            "View Profile",
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors mr-2",
                        ),
                        href=f"/doctor?id={doctor['id']}",
                    ),
                    rx.el.a(
                        rx.el.button(
                            "Book Appointment",
                            class_name="px-4 py-2 bg-[#6b2d5b] text-white text-sm font-medium rounded-lg hover:bg-[#5a254c] transition-colors shadow-sm",
                        ),
                        href=f"/book-appointment?doctor_id={doctor['id']}&doctor_name={doctor['name']}",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex flex-col sm:flex-row items-center justify-between border-t border-gray-100 pt-4 mt-2",
            ),
            class_name="p-6",
        ),
        class_name="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300 border border-gray-200 overflow-hidden",
    )