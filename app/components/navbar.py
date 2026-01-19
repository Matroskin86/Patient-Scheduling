import reflex as rx
from app.states.auth_state import AuthState


def navbar_link(text: str, url: str, icon: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, class_name="w-4 h-4 mr-2 opacity-80"),
            rx.el.span(text),
            class_name="flex items-center",
        ),
        href=url,
        class_name="text-white/90 hover:text-white hover:bg-white/10 px-3 py-2 rounded-lg transition-colors text-sm font-medium",
    )


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.icon("activity", class_name="w-8 h-8 text-white mr-2"),
                        rx.el.span(
                            "MediConnect",
                            class_name="text-xl font-bold text-white tracking-tight",
                        ),
                        class_name="flex items-center",
                    ),
                    href="/",
                ),
                rx.el.div(
                    navbar_link("Home", "/", "home"),
                    rx.cond(
                        AuthState.current_user["role"] == "doctor",
                        navbar_link(
                            "Dashboard", "/doctor-dashboard", "layout-dashboard"
                        ),
                    ),
                    navbar_link("My Appointments", "/my-appointments", "calendar"),
                    navbar_link("My Documents", "/my-documents", "file-text"),
                    navbar_link("My Prescriptions", "/my-prescriptions", "pill"),
                    navbar_link("Messages", "/messages", "message-square"),
                    rx.cond(
                        AuthState.current_user["role"] == "admin",
                        navbar_link("Admin", "/admin", "shield-check"),
                    ),
                    class_name="hidden md:flex items-center space-x-2 ml-8",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                AuthState.user_initials,
                                class_name="text-xs font-bold text-[#6b2d5b]",
                            ),
                            class_name="w-8 h-8 rounded-full bg-white flex items-center justify-center border-2 border-white/20 shadow-sm",
                        ),
                        rx.el.div(
                            rx.el.p(
                                AuthState.current_user["name"],
                                class_name="text-sm font-medium text-white",
                            ),
                            rx.el.p(
                                AuthState.current_user["role"].capitalize(),
                                class_name="text-xs text-white/70",
                            ),
                            class_name="hidden sm:block text-right mr-3",
                        ),
                        rx.el.button(
                            rx.icon("log-out", class_name="w-4 h-4"),
                            on_click=AuthState.handle_logout,
                            class_name="p-2 text-white/80 hover:text-white hover:bg-white/10 rounded-full transition-colors",
                            title="Sign Out",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.div(
                        rx.el.a(
                            "Log In",
                            href="/login",
                            class_name="text-white hover:text-white/80 font-medium text-sm mr-4 transition-colors",
                        ),
                        rx.el.a(
                            "Register",
                            href="/register",
                            class_name="bg-white text-[#6b2d5b] hover:bg-gray-100 px-4 py-2 rounded-lg text-sm font-bold transition-all shadow-sm",
                        ),
                        class_name="flex items-center",
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16",
        ),
        class_name="bg-[#6b2d5b] shadow-md sticky top-0 z-50 w-full",
    )