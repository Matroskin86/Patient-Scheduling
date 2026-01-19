import reflex as rx
from app.components.navbar import navbar


def layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(content, class_name="flex-grow bg-gray-50 min-h-[calc(100vh-4rem)]"),
        rx.el.footer(
            rx.el.div(
                rx.el.p(
                    "© 2024 MediConnect. Secure Patient Scheduling System.",
                    class_name="text-gray-500 text-sm text-center",
                ),
                class_name="max-w-7xl mx-auto py-6 px-4",
            ),
            class_name="bg-white border-t border-gray-200",
        ),
        class_name="min-h-screen flex flex-col font-sans",
    )