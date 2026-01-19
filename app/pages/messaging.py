import reflex as rx
from app.components.layout import layout
from app.states.message_state import MessageState
from app.states.auth_state import AuthState


def contact_item(user: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                user["name"][0],
                class_name="w-10 h-10 rounded-full bg-purple-100 text-[#6b2d5b] flex items-center justify-center font-bold text-lg",
            ),
            rx.el.div(
                rx.el.p(user["name"], class_name="font-medium text-gray-900 truncate"),
                rx.el.p(user["role"].capitalize(), class_name="text-xs text-gray-500"),
                class_name="ml-3 overflow-hidden",
            ),
            class_name="flex items-center",
        ),
        on_click=lambda: MessageState.select_contact(user["id"]),
        class_name=rx.cond(
            MessageState.selected_contact_id == user["id"],
            "p-3 rounded-lg bg-purple-50 cursor-pointer border-l-4 border-[#6b2d5b]",
            "p-3 rounded-lg hover:bg-gray-50 cursor-pointer border-l-4 border-transparent",
        ),
    )


def message_bubble(msg: dict) -> rx.Component:
    is_me = msg["sender_id"] == AuthState.current_user["id"]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(msg["content"], class_name="text-sm"),
                class_name=rx.cond(
                    is_me,
                    "bg-[#6b2d5b] text-white p-3 rounded-2xl rounded-tr-none",
                    "bg-gray-100 text-gray-800 p-3 rounded-2xl rounded-tl-none",
                ),
            ),
            rx.el.p(
                msg["timestamp"].split(" ")[1],
                class_name="text-xs text-gray-400 mt-1 px-1",
            ),
            class_name=rx.cond(
                is_me, "flex flex-col items-end", "flex flex-col items-start"
            ),
        ),
        class_name=rx.cond(is_me, "flex justify-end mb-4", "flex justify-start mb-4"),
    )


def messaging_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Messages", class_name="text-xl font-bold text-gray-900 mb-4"
                    ),
                    rx.el.input(
                        placeholder="Search contacts...",
                        class_name="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm mb-4 focus:outline-none focus:ring-2 focus:ring-[#6b2d5b]",
                    ),
                    class_name="p-4 border-b border-gray-100",
                ),
                rx.el.div(
                    rx.foreach(MessageState.contacts, contact_item),
                    class_name="p-2 space-y-1 overflow-y-auto h-[calc(100vh-16rem)]",
                ),
                class_name="w-full md:w-80 bg-white border-r border-gray-200 flex flex-col h-[calc(100vh-8rem)]",
            ),
            rx.el.div(
                rx.cond(
                    MessageState.selected_contact_id != "",
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3("Chat", class_name="font-bold text-gray-900"),
                            class_name="h-16 border-b border-gray-200 flex items-center px-6 bg-white",
                        ),
                        rx.el.div(
                            rx.foreach(
                                MessageState.current_conversation, message_bubble
                            ),
                            class_name="flex-1 bg-gray-50 p-6 overflow-y-auto",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.input(
                                    placeholder="Type a message...",
                                    on_change=MessageState.set_message_content,
                                    class_name="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:border-[#6b2d5b]",
                                    default_value=MessageState.new_message_content,
                                ),
                                rx.el.button(
                                    rx.icon("send", class_name="w-5 h-5"),
                                    on_click=MessageState.send_message,
                                    disabled=MessageState.new_message_content == "",
                                    class_name=rx.cond(
                                        MessageState.new_message_content == "",
                                        "ml-2 p-2 bg-gray-300 text-white rounded-full cursor-not-allowed",
                                        "ml-2 p-2 bg-[#6b2d5b] text-white rounded-full hover:bg-[#5a254c] transition-colors",
                                    ),
                                ),
                                class_name="flex items-center bg-white p-4 border-t border-gray-200",
                            ),
                            class_name="sticky bottom-0",
                        ),
                        class_name="flex flex-col h-full",
                    ),
                    rx.el.div(
                        rx.icon(
                            "message-square", class_name="w-16 h-16 text-gray-300 mb-4"
                        ),
                        rx.el.p(
                            "Select a contact to start messaging",
                            class_name="text-gray-500 font-medium",
                        ),
                        class_name="flex flex-col items-center justify-center h-full bg-gray-50",
                    ),
                ),
                class_name="flex-1 flex flex-col h-[calc(100vh-8rem)]",
            ),
            class_name="flex bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden h-[calc(100vh-8rem)]",
        ),
        class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 h-full",
    )


def messaging_page() -> rx.Component:
    return layout(messaging_content())