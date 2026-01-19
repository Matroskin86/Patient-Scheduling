import reflex as rx
from app.components.layout import layout
from app.states.admin_state import AdminState
from app.states.auth_state import AuthState


def stat_card(title: str, value: str, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(title, class_name="text-sm font-medium text-gray-500 mb-1"),
                rx.el.h3(value, class_name="text-2xl font-bold text-gray-900"),
            ),
            rx.el.div(
                rx.icon(icon, class_name=f"w-6 h-6 {color}"),
                class_name="p-3 bg-gray-50 rounded-lg",
            ),
            class_name="flex items-center justify-between",
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200",
    )


def user_row(user: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.span(user["name"], class_name="font-medium text-gray-900"),
                rx.el.p(user["email"], class_name="text-xs text-gray-500"),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                user["role"].capitalize(),
                class_name="px-2 py-1 text-xs font-semibold rounded-full bg-blue-50 text-blue-700",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.button(
                "Delete",
                on_click=lambda: AdminState.delete_user(user["id"]),
                class_name="text-red-600 hover:text-red-900 text-sm font-medium",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
    )


def admin_dashboard_content() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Admin Dashboard", class_name="text-2xl font-bold text-gray-900 mb-8"),
        rx.el.div(
            stat_card(
                "Total Users",
                AdminState.total_users.to_string(),
                "users",
                "text-blue-500",
            ),
            stat_card(
                "Appointments",
                AdminState.total_appointments.to_string(),
                "calendar",
                "text-purple-500",
            ),
            stat_card("Revenue (Est.)", "$12,450", "dollar-sign", "text-green-500"),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "User Management", class_name="text-lg font-bold text-gray-900 mb-4"
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "User",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase",
                                ),
                                rx.el.th(
                                    "Role",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase",
                                ),
                                rx.el.th(
                                    "Actions",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase",
                                ),
                            ),
                            class_name="bg-gray-50",
                        ),
                        rx.el.tbody(
                            rx.foreach(AuthState.users, user_row),
                            class_name="bg-white divide-y divide-gray-200",
                        ),
                        class_name="min-w-full divide-y divide-gray-200",
                    ),
                    class_name="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden",
                ),
                class_name="lg:col-span-2",
            ),
            class_name="grid grid-cols-1 gap-8",
        ),
        class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
    )


def admin_dashboard_page() -> rx.Component:
    return layout(admin_dashboard_content())