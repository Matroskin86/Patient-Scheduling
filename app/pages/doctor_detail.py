import reflex as rx
from app.components.layout import layout
from app.states.doctor_state import DoctorState


def detail_content() -> rx.Component:
    doctor = DoctorState.current_doctor
    return rx.cond(
        doctor,
        rx.el.div(
            rx.el.div(
                rx.el.a("Home", href="/", class_name="hover:text-[#6b2d5b]"),
                rx.el.span("/", class_name="mx-2 text-gray-400"),
                rx.el.span("Doctor Details", class_name="text-gray-900"),
                class_name="flex items-center text-sm text-gray-500 mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.image(
                            src=doctor["image"],
                            class_name="w-32 h-32 rounded-full border-4 border-white shadow-lg mx-auto mb-4 bg-gray-100",
                        ),
                        rx.el.h1(
                            doctor["name"],
                            class_name="text-2xl font-bold text-gray-900 text-center mb-1",
                        ),
                        rx.el.div(
                            rx.el.span(
                                doctor["specialty"],
                                class_name="bg-purple-100 text-[#6b2d5b] px-4 py-1.5 rounded-full text-sm font-semibold",
                            ),
                            class_name="flex justify-center mb-6",
                        ),
                        rx.el.div(
                            rx.el.h3(
                                "About",
                                class_name="text-sm font-bold text-gray-900 uppercase tracking-wide mb-2",
                            ),
                            rx.el.p(
                                doctor["bio"],
                                class_name="text-gray-600 leading-relaxed mb-6",
                            ),
                            rx.el.h3(
                                "Skills",
                                class_name="text-sm font-bold text-gray-900 uppercase tracking-wide mb-3",
                            ),
                            rx.el.div(
                                rx.foreach(
                                    doctor["skills"],
                                    lambda skill: rx.el.span(
                                        skill,
                                        class_name="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm font-medium",
                                    ),
                                ),
                                class_name="flex flex-wrap gap-2 mb-6",
                            ),
                            rx.el.h3(
                                "Services",
                                class_name="text-sm font-bold text-gray-900 uppercase tracking-wide mb-3",
                            ),
                            rx.el.div(
                                rx.foreach(
                                    doctor["services"],
                                    lambda service: rx.el.div(
                                        rx.icon(
                                            "check",
                                            class_name="w-4 h-4 text-green-500 mr-2",
                                        ),
                                        rx.el.span(service, class_name="text-gray-700"),
                                        class_name="flex items-center",
                                    ),
                                ),
                                class_name="space-y-2 mb-6",
                            ),
                            class_name="bg-white rounded-2xl p-6 sm:p-8 shadow-sm border border-gray-200",
                        ),
                        class_name="space-y-6",
                    ),
                    class_name="lg:col-span-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Practice Location",
                                class_name="text-lg font-bold text-gray-900 mb-4",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "map-pin",
                                    class_name="w-5 h-5 text-[#6b2d5b] mt-1 mr-3 flex-shrink-0",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        doctor["address"],
                                        class_name="font-medium text-gray-900",
                                    ),
                                    rx.el.p(
                                        f"{doctor['city']}, {doctor['state']} {doctor['zip_code']}",
                                        class_name="text-gray-500",
                                    ),
                                ),
                                class_name="flex items-start mb-4",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "map", class_name="w-8 h-8 text-gray-400 mb-2"
                                    ),
                                    rx.el.span(
                                        "Map View Placeholder",
                                        class_name="text-gray-500 font-medium",
                                    ),
                                    class_name="flex flex-col items-center justify-center h-full",
                                ),
                                class_name="w-full h-48 bg-gray-100 rounded-xl border border-gray-200 mb-6",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.span(
                                        "Consultation Rate",
                                        class_name="text-gray-500 text-sm",
                                    ),
                                    rx.el.span(
                                        doctor["rates"],
                                        class_name="text-xl font-bold text-gray-900",
                                    ),
                                    class_name="flex justify-between items-center mb-6 pt-6 border-t border-gray-100",
                                ),
                                rx.el.a(
                                    rx.el.button(
                                        "Book Appointment Now",
                                        class_name="w-full bg-[#6b2d5b] hover:bg-[#5a254c] text-white font-bold py-3 px-6 rounded-xl transition-colors shadow-md",
                                    ),
                                    href=f"/book-appointment?doctor_id={doctor['id']}&doctor_name={doctor['name']}",
                                ),
                                class_name="",
                            ),
                            class_name="bg-white rounded-2xl p-6 shadow-sm border border-gray-200 sticky top-24",
                        )
                    ),
                    class_name="lg:col-span-1",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-8",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("user-x", class_name="w-16 h-16 text-gray-300 mb-4"),
                rx.el.h2(
                    "Doctor Not Found",
                    class_name="text-2xl font-bold text-gray-900 mb-2",
                ),
                rx.el.p(
                    "The doctor you are looking for does not exist or has been removed.",
                    class_name="text-gray-500 mb-6",
                ),
                rx.el.a(
                    rx.el.button(
                        "Back to Directory",
                        class_name="bg-[#6b2d5b] text-white px-6 py-2 rounded-lg hover:bg-[#5a254c]",
                    ),
                    href="/",
                ),
                class_name="flex flex-col items-center justify-center py-20",
            ),
            class_name="max-w-7xl mx-auto px-4",
        ),
    )


def doctor_detail_page() -> rx.Component:
    return layout(detail_content())