import reflex as rx
from app.states.models import Message, User
from app.states.auth_state import AuthState
import datetime


class MessageState(rx.State):
    messages: list[Message] = [
        {
            "id": "m1",
            "sender_id": "u2",
            "sender_name": "Dr. Sarah Smith",
            "receiver_id": "u1",
            "receiver_name": "John Doe",
            "content": "Hello John, how are you feeling after the medication?",
            "timestamp": "2024-11-16 10:00",
        },
        {
            "id": "m2",
            "sender_id": "u1",
            "sender_name": "John Doe",
            "receiver_id": "u2",
            "receiver_name": "Dr. Sarah Smith",
            "content": "Much better, thank you Doctor.",
            "timestamp": "2024-11-16 10:15",
        },
    ]
    selected_contact_id: str = ""
    new_message_content: str = ""

    @rx.var
    async def contacts(self) -> list[User]:
        auth_state = await self.get_state(AuthState)
        current_user_id = (
            auth_state.current_user["id"] if auth_state.current_user else ""
        )
        return [
            u
            for u in auth_state.users
            if u["id"] != current_user_id and u["role"] != "admin"
        ]

    @rx.var
    async def current_conversation(self) -> list[Message]:
        auth_state = await self.get_state(AuthState)
        if not auth_state.current_user or not self.selected_contact_id:
            return []
        uid = auth_state.current_user["id"]
        cid = self.selected_contact_id
        conversation = [
            m
            for m in self.messages
            if m["sender_id"] == uid
            and m["receiver_id"] == cid
            or (m["sender_id"] == cid and m["receiver_id"] == uid)
        ]
        return sorted(conversation, key=lambda x: x["timestamp"])

    @rx.event
    def select_contact(self, contact_id: str):
        self.selected_contact_id = contact_id

    @rx.event
    def set_message_content(self, content: str):
        self.new_message_content = content

    @rx.event
    async def send_message(self):
        if not self.new_message_content or not self.selected_contact_id:
            return
        auth_state = await self.get_state(AuthState)
        if not auth_state.current_user:
            return
        receiver_name = "Unknown"
        for u in auth_state.users:
            if u["id"] == self.selected_contact_id:
                receiver_name = u["name"]
                break
        new_msg: Message = {
            "id": f"m{len(self.messages) + 1}",
            "sender_id": auth_state.current_user["id"],
            "sender_name": auth_state.current_user["name"],
            "receiver_id": self.selected_contact_id,
            "receiver_name": receiver_name,
            "content": self.new_message_content,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self.messages.append(new_msg)
        self.new_message_content = ""