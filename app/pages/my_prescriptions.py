import reflex as rx
from app.components.layout import layout
from app.states.prescription_state import PrescriptionState
from app.states.models import Prescription


def prescription_row(rx_item: Prescription) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h4(
                    rx_item["medication"], class_name="text-lg font-bold text-gray-900"
                ),
                rx.el.span(
                    rx_item["dosage"],
                    class_name="ml-2 text-sm bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full font-medium",
                ),
                class_name="flex items-center mb-2",
            ),
            rx.el.p(rx_item["instructions"], class_name="text-gray-600 mb-4"),
            rx.el.div(
                rx.el.div(
                    rx.icon("user", class_name="w-4 h-4 text-gray-400 mr-2"),
                    rx.el.span(
                        rx_item["doctor_name"], class_name="text-sm text-gray-500"
                    ),
                    class_name="flex items-center mb-1",
                ),
                rx.el.div(
                    rx.icon("calendar", class_name="w-4 h-4 text-gray-400 mr-2"),
                    rx.el.span(
                        f"Prescribed: {rx_item['date']}",
                        class_name="text-sm text-gray-500",
                    ),
                    class_name="flex items-center",
                ),
                class_name="mb-4",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span("Status:", class_name="text-sm text-gray-500 mr-2"),
                rx.match(
                    rx_item["status"],
                    (
                        "Active",
                        rx.el.span(
                            "Active", class_name="text-green-600 font-medium text-sm"
                        ),
                    ),
                    (
                        "Refill Requested",
                        rx.el.span(
                            "Refill Requested",
                            class_name="text-yellow-600 font-medium text-sm",
                        ),
                    ),
                    rx.el.span(
                        rx_item["status"],
                        class_name="text-gray-600 font-medium text-sm",
                    ),
                ),
                class_name="flex items-center justify-end mb-4",
            ),
            rx.cond(
                rx_item["status"] == "Active",
                rx.el.button(
                    "Request Refill",
                    on_click=lambda: PrescriptionState.request_refill(rx_item["id"]),
                    class_name="w-full border border-[#6b2d5b] text-[#6b2d5b] hover:bg-purple-50 px-4 py-2 rounded-lg text-sm font-medium transition-colors",
                ),
                rx.el.button(
                    "Refill Pending",
                    disabled=True,
                    class_name="w-full bg-gray-100 text-gray-400 px-4 py-2 rounded-lg text-sm font-medium cursor-not-allowed",
                ),
            ),
            class_name="flex flex-col justify-between h-full border-t border-gray-100 pt-4 mt-2",
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200 flex flex-col justify-between h-full",
    )


def my_prescriptions_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "My Prescriptions", class_name="text-2xl font-bold text-gray-900 mb-2"
            ),
            rx.el.p(
                "Manage your medications and refills.", class_name="text-gray-500 mb-8"
            ),
        ),
        rx.cond(
            PrescriptionState.my_prescriptions.length() > 0,
            rx.el.div(
                rx.foreach(PrescriptionState.my_prescriptions, prescription_row),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
            rx.el.div(
                rx.icon("pill", class_name="w-12 h-12 text-gray-300 mb-3"),
                rx.el.h3(
                    "No prescriptions found",
                    class_name="text-lg font-medium text-gray-900",
                ),
                rx.el.p(
                    "Your active medications will appear here.",
                    class_name="text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center py-16 bg-white rounded-xl border border-gray-200 border-dashed",
            ),
        ),
        class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
    )


def my_prescriptions_page() -> rx.Component:
    return layout(my_prescriptions_content())