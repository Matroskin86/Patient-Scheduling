import reflex as rx
from typing import Optional
from app.states.models import User
import asyncio


class AuthState(rx.State):
    users: list[User] = [
        {
            "id": "u1",
            "email": "patient@test.com",
            "password_hash": "password",
            "role": "patient",
            "name": "John Doe",
        },
        {
            "id": "u2",
            "email": "doctor@test.com",
            "password_hash": "password",
            "role": "doctor",
            "name": "Dr. Sarah Smith",
        },
        {
            "id": "u3",
            "email": "admin@test.com",
            "password_hash": "password",
            "role": "admin",
            "name": "Admin User",
        },
    ]
    current_user: Optional[User] = None
    login_email: str = ""
    login_password: str = ""
    login_error: str = ""
    reg_name: str = ""
    reg_email: str = ""
    reg_password: str = ""
    reg_role: str = "patient"
    reg_error: str = ""

    @rx.var
    def is_authenticated(self) -> bool:
        return self.current_user is not None

    @rx.var
    def user_initials(self) -> str:
        if not self.current_user:
            return "?"
        name_parts = self.current_user["name"].split()
        if len(name_parts) >= 2:
            return f"{name_parts[0][0]}{name_parts[1][0]}".upper()
        return self.current_user["name"][0].upper()

    @rx.event
    def handle_login(self):
        user = next(
            (
                u
                for u in self.users
                if u["email"] == self.login_email
                and u["password_hash"] == self.login_password
            ),
            None,
        )
        if user:
            self.current_user = user
            self.login_error = ""
            return rx.redirect("/")
        else:
            self.login_error = "Invalid email or password."

    @rx.event
    def handle_logout(self):
        self.current_user = None
        return rx.redirect("/login")

    @rx.event
    def handle_register(self):
        if any((u["email"] == self.reg_email for u in self.users)):
            self.reg_error = "Email already registered."
            return
        new_user: User = {
            "id": f"u{len(self.users) + 1}",
            "email": self.reg_email,
            "password_hash": self.reg_password,
            "role": self.reg_role,
            "name": self.reg_name,
        }
        self.users.append(new_user)
        self.current_user = new_user
        self.reg_error = ""
        return rx.redirect("/")

    @rx.event
    def set_reg_role(self, role: str):
        self.reg_role = role