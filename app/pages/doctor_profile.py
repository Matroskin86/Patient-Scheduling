import reflex as rx
from app.components.layout import layout
from app.states.doctor_state import DoctorState


def doctor_profile_form() -> rx.Component:
    doctor = DoctorState.current_doctor
    return rx.cond(
        doctor,
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Edit Profile", class_name="text-2xl font-bold text-gray-900 mb-2"
                ),
                rx.el.p(
                    "Update your professional information visible to patients.",
                    class_name="text-gray-500 mb-8",
                ),
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Specialty",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="specialty",
                            default_value=doctor["specialty"],
                            class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Consultation Rate",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="rates",
                            default_value=doctor["rates"],
                            class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent",
                        ),
                        class_name="mb-4",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Bio", class_name="block text-sm font-medium text-gray-700 mb-1"
                    ),
                    rx.el.textarea(
                        name="bio",
                        default_value=doctor["bio"],
                        rows="4",
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Skills (comma separated)",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="skills",
                        default_value=doctor["skills"].join(", "),
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Services (comma separated)",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="services",
                        default_value=doctor["services"].join(", "),
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Address",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="address",
                        default_value=doctor["address"],
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent",
                    ),
                    class_name="mb-8",
                ),
                rx.el.button(
                    "Save Changes",
                    type="submit",
                    class_name="bg-[#6b2d5b] text-white px-6 py-2 rounded-lg hover:bg-[#5a254c] font-medium shadow-sm",
                ),
                on_submit=DoctorState.update_profile,
            ),
            class_name="bg-white p-8 rounded-2xl shadow-sm border border-gray-200 max-w-3xl mx-auto",
        ),
        rx.el.div(
            "Profile not found or you are not a doctor.",
            class_name="text-center py-20 text-gray-500",
        ),
    )


def doctor_profile_page() -> rx.Component:
    return layout(
        rx.el.div(
            doctor_profile_form(),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
        )
    )