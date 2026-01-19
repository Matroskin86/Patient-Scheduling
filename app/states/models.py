import reflex as rx
from typing import TypedDict, Optional


class User(TypedDict):
    id: str
    email: str
    password_hash: str
    role: str
    name: str


class Doctor(TypedDict):
    id: str
    user_id: str
    name: str
    specialty: str
    address: str
    city: str
    state: str
    zip_code: str
    bio: str
    skills: list[str]
    services: list[str]
    rates: str
    image: str


class Patient(TypedDict):
    id: str
    user_id: str
    date_of_birth: str
    phone: str


class Appointment(TypedDict):
    id: str
    patient_id: str
    patient_name: str
    doctor_id: str
    doctor_name: str
    date: str
    start_time: str
    end_time: str
    duration: int
    notes: str
    status: str


class Document(TypedDict):
    id: str
    user_id: str
    name: str
    date: str
    filename: str
    type: str


class Prescription(TypedDict):
    id: str
    patient_id: str
    patient_name: str
    doctor_id: str
    doctor_name: str
    medication: str
    dosage: str
    instructions: str
    date: str
    status: str


class Message(TypedDict):
    id: str
    sender_id: str
    sender_name: str
    receiver_id: str
    receiver_name: str
    content: str
    timestamp: str