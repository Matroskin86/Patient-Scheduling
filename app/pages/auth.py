import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Welcome Back",
                    class_name="text-2xl font-bold text-gray-900 text-center mb-2",
                ),
                rx.el.p(
                    "Sign in to access your dashboard",
                    class_name="text-gray-500 text-center mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Email Address",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="email",
                            placeholder="you@example.com",
                            on_change=AuthState.set_login_email,
                            class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent outline-none transition-all",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Password",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="password",
                            placeholder="••••••••",
                            on_change=AuthState.set_login_password,
                            class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent outline-none transition-all",
                        ),
                        class_name="mb-6",
                    ),
                    rx.cond(
                        AuthState.login_error != "",
                        rx.el.div(
                            rx.icon("cigarette", class_name="w-4 h-4 mr-2"),
                            AuthState.login_error,
                            class_name="bg-red-50 text-red-600 px-4 py-3 rounded-lg mb-6 flex items-center text-sm",
                        ),
                    ),
                    rx.el.button(
                        "Sign In",
                        on_click=AuthState.handle_login,
                        class_name="w-full bg-[#6b2d5b] text-white py-2 rounded-lg hover:bg-[#5a254c] font-medium transition-colors shadow-sm",
                    ),
                ),
                rx.el.div(
                    rx.el.span("Don't have an account? ", class_name="text-gray-600"),
                    rx.el.a(
                        "Create one now",
                        href="/register",
                        class_name="text-[#6b2d5b] font-medium hover:underline",
                    ),
                    class_name="mt-6 text-center text-sm",
                ),
                class_name="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100",
            ),
            class_name="flex flex-col items-center justify-center min-h-screen px-4",
        ),
        class_name="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50",
    )


def register_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Create Account",
                    class_name="text-2xl font-bold text-gray-900 text-center mb-2",
                ),
                rx.el.p(
                    "Join MediConnect today",
                    class_name="text-gray-500 text-center mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Full Name",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="text",
                            placeholder="John Doe",
                            on_change=AuthState.set_reg_name,
                            class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent outline-none transition-all",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Email Address",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="email",
                            placeholder="you@example.com",
                            on_change=AuthState.set_reg_email,
                            class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent outline-none transition-all",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Password",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="password",
                            placeholder="••••••••",
                            on_change=AuthState.set_reg_password,
                            class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent outline-none transition-all",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "I am a...",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Patient",
                                on_click=lambda: AuthState.set_reg_role("patient"),
                                class_name=rx.cond(
                                    AuthState.reg_role == "patient",
                                    "flex-1 py-2 px-4 rounded-lg bg-[#6b2d5b] text-white text-sm font-medium shadow-sm transition-colors",
                                    "flex-1 py-2 px-4 rounded-lg bg-gray-100 text-gray-600 text-sm font-medium hover:bg-gray-200 transition-colors",
                                ),
                            ),
                            rx.el.button(
                                "Doctor",
                                on_click=lambda: AuthState.set_reg_role("doctor"),
                                class_name=rx.cond(
                                    AuthState.reg_role == "doctor",
                                    "flex-1 py-2 px-4 rounded-lg bg-[#6b2d5b] text-white text-sm font-medium shadow-sm transition-colors",
                                    "flex-1 py-2 px-4 rounded-lg bg-gray-100 text-gray-600 text-sm font-medium hover:bg-gray-200 transition-colors",
                                ),
                            ),
                            class_name="flex gap-2 p-1 bg-gray-50 rounded-xl border border-gray-200",
                        ),
                        class_name="mb-6",
                    ),
                    rx.cond(
                        AuthState.reg_error != "",
                        rx.el.div(
                            rx.icon("cigarette", class_name="w-4 h-4 mr-2"),
                            AuthState.reg_error,
                            class_name="bg-red-50 text-red-600 px-4 py-3 rounded-lg mb-6 flex items-center text-sm",
                        ),
                    ),
                    rx.el.button(
                        "Create Account",
                        on_click=AuthState.handle_register,
                        class_name="w-full bg-[#6b2d5b] text-white py-2 rounded-lg hover:bg-[#5a254c] font-medium transition-colors shadow-sm",
                    ),
                ),
                rx.el.div(
                    rx.el.span("Already have an account? ", class_name="text-gray-600"),
                    rx.el.a(
                        "Sign In",
                        href="/login",
                        class_name="text-[#6b2d5b] font-medium hover:underline",
                    ),
                    class_name="mt-6 text-center text-sm",
                ),
                class_name="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100",
            ),
            class_name="flex flex-col items-center justify-center min-h-screen px-4",
        ),
        class_name="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50",
    )