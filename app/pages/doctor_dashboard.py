import reflex as rx
from app.components.layout import layout
from app.states.appointment_state import AppointmentState
from app.states.prescription_state import PrescriptionState
from app.states.models import Appointment
from app.pages.my_appointments import status_badge


def doctor_appointment_row(appointment: Appointment) -> rx.Component:
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
                    appointment["patient_name"],
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
            rx.el.p(
                rx.cond(appointment["notes"], appointment["notes"][:30] + "...", "-"),
                class_name="text-sm text-gray-500 truncate max-w-xs",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.a(
                    rx.icon(
                        "eye", class_name="w-5 h-5 text-gray-400 hover:text-[#6b2d5b]"
                    ),
                    href=f"/appointment?id={appointment['id']}",
                    class_name="mr-3",
                    title="View Details",
                ),
                rx.cond(
                    appointment["status"] == "pending",
                    rx.el.button(
                        rx.icon(
                            "check",
                            class_name="w-5 h-5 text-green-500 hover:text-green-700",
                        ),
                        on_click=lambda: AppointmentState.update_status(
                            appointment["id"], "confirmed"
                        ),
                        title="Confirm",
                        class_name="mr-3",
                    ),
                ),
                rx.cond(
                    appointment["status"] == "confirmed",
                    rx.el.button(
                        rx.icon(
                            "circle_check_big",
                            class_name="w-5 h-5 text-blue-500 hover:text-blue-700",
                        ),
                        on_click=lambda: AppointmentState.update_status(
                            appointment["id"], "completed"
                        ),
                        title="Complete",
                        class_name="mr-3",
                    ),
                ),
                rx.cond(
                    (appointment["status"] == "pending")
                    | (appointment["status"] == "confirmed"),
                    rx.el.button(
                        rx.icon(
                            "x", class_name="w-5 h-5 text-red-400 hover:text-red-600"
                        ),
                        on_click=lambda: AppointmentState.cancel_appointment(
                            appointment["id"]
                        ),
                        title="Cancel",
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
    )


def dashboard_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Doctor Dashboard", class_name="text-2xl font-bold text-gray-900 mb-2"
            ),
            rx.el.p(
                "Manage your schedule and patient appointments.",
                class_name="text-gray-500 mb-8",
            ),
        ),
        rx.cond(
            AppointmentState.doctor_appointments.length() > 0,
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Date & Time",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Patient",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Notes",
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
                            AppointmentState.doctor_appointments, doctor_appointment_row
                        ),
                        class_name="bg-white divide-y divide-gray-200",
                    ),
                    class_name="min-w-full divide-y divide-gray-200",
                ),
                class_name="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden overflow-x-auto",
            ),
            rx.el.div(
                rx.icon("calendar-check", class_name="w-12 h-12 text-gray-300 mb-3"),
                rx.el.h3(
                    "No appointments found",
                    class_name="text-lg font-medium text-gray-900",
                ),
                rx.el.p(
                    "Your schedule is currently empty.", class_name="text-gray-500"
                ),
                class_name="flex flex-col items-center justify-center py-16 bg-white rounded-xl border border-gray-200 border-dashed",
            ),
        ),
        class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
    )


def prescription_form() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Issue Prescription", class_name="text-lg font-bold text-gray-900 mb-4"
        ),
        rx.el.div(
            rx.el.label(
                "Patient ID", class_name="block text-sm font-medium text-gray-700 mb-1"
            ),
            rx.el.input(
                placeholder="e.g. u1",
                on_change=PrescriptionState.set_issue_patient,
                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg mb-4",
                default_value=PrescriptionState.issue_patient_id,
            ),
            rx.el.label(
                "Medication", class_name="block text-sm font-medium text-gray-700 mb-1"
            ),
            rx.el.input(
                placeholder="Drug Name",
                on_change=PrescriptionState.set_issue_medication,
                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg mb-4",
                default_value=PrescriptionState.issue_medication,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Dosage",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        placeholder="e.g. 500mg",
                        on_change=PrescriptionState.set_issue_dosage,
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-lg mb-4",
                        default_value=PrescriptionState.issue_dosage,
                    ),
                    class_name="flex-1 mr-2",
                ),
                class_name="flex",
            ),
            rx.el.label(
                "Instructions",
                class_name="block text-sm font-medium text-gray-700 mb-1",
            ),
            rx.el.textarea(
                placeholder="Dosing instructions...",
                rows="3",
                on_change=PrescriptionState.set_issue_instructions,
                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg mb-4",
                default_value=PrescriptionState.issue_instructions,
            ),
            rx.el.button(
                "Issue Prescription",
                on_click=PrescriptionState.issue_prescription,
                class_name="w-full bg-[#6b2d5b] text-white py-2 rounded-lg hover:bg-[#5a254c] font-medium",
            ),
            class_name="bg-gray-50 p-6 rounded-xl border border-gray-200",
        ),
        class_name="mb-8",
    )


def doctor_dashboard_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(dashboard_content(), class_name="lg:col-span-2"),
            rx.el.div(
                prescription_form(),
                rx.el.div(
                    rx.el.h3(
                        "Quick Actions",
                        class_name="text-lg font-bold text-gray-900 mb-4",
                    ),
                    rx.el.a(
                        rx.el.button(
                            "Edit Profile",
                            class_name="w-full text-left px-4 py-2 rounded-lg hover:bg-gray-100 text-gray-700 font-medium mb-2",
                        ),
                        href="/doctor-profile",
                    ),
                    rx.el.a(
                        rx.el.button(
                            "Messages",
                            class_name="w-full text-left px-4 py-2 rounded-lg hover:bg-gray-100 text-gray-700 font-medium",
                        ),
                        href="/messages",
                    ),
                    class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
                ),
                class_name="lg:col-span-1",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
        )
    )