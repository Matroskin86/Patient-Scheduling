import reflex as rx
from typing import Optional
from app.states.models import Doctor
import math


class DoctorState(rx.State):
    doctors: list[Doctor] = [
        {
            "id": "d1",
            "user_id": "u2",
            "name": "Dr. Sarah Smith",
            "specialty": "Cardiology",
            "address": "123 Heartbeat Ln",
            "city": "New York",
            "state": "NY",
            "zip_code": "10001",
            "bio": "Dr. Smith has over 15 years of experience in interventional cardiology. She is dedicated to providing patient-centered care focused on prevention and treatment of heart disease.",
            "skills": ["Angioplasty", "Echocardiography", "Preventive Cardiology"],
            "services": ["Consultation", "ECG", "Stress Test"],
            "rates": "$200/consult",
            "image": "https://api.dicebear.com/9.x/avataaars/svg?seed=Sarah",
        },
        {
            "id": "d2",
            "user_id": "u4",
            "name": "Dr. James Wilson",
            "specialty": "General Practitioner",
            "address": "456 Main St",
            "city": "Brooklyn",
            "state": "NY",
            "zip_code": "11201",
            "bio": "A compassionate family doctor who treats patients of all ages. Dr. Wilson believes in holistic medicine and building long-term relationships with his patients.",
            "skills": ["Family Medicine", "Pediatrics", "Geriatrics"],
            "services": ["Check-up", "Vaccination", "Physical Exam"],
            "rates": "$150/consult",
            "image": "https://api.dicebear.com/9.x/avataaars/svg?seed=James",
        },
        {
            "id": "d3",
            "user_id": "u5",
            "name": "Dr. Emily Chen",
            "specialty": "Dermatology",
            "address": "789 Skin Care Blvd",
            "city": "Queens",
            "state": "NY",
            "zip_code": "11375",
            "bio": "Specializing in both medical and cosmetic dermatology, Dr. Chen helps patients achieve healthy, beautiful skin through cutting-edge treatments.",
            "skills": ["Acne Treatment", "Skin Cancer Screening", "Laser Therapy"],
            "services": ["Skin Biopsy", "Botox", "Chemical Peel"],
            "rates": "$250/consult",
            "image": "https://api.dicebear.com/9.x/avataaars/svg?seed=Emily",
        },
        {
            "id": "d4",
            "user_id": "u6",
            "name": "Dr. Michael Ross",
            "specialty": "Neurology",
            "address": "321 Brain Ave",
            "city": "New York",
            "state": "NY",
            "zip_code": "10022",
            "bio": "Expert in treating neurological disorders including migraines, epilepsy, and stroke. Dr. Ross uses the latest diagnostic tools to help his patients.",
            "skills": ["MRI Interpretation", "EEG", "Migraine Management"],
            "services": ["Neurological Exam", "EEG", "Consultation"],
            "rates": "$300/consult",
            "image": "https://api.dicebear.com/9.x/avataaars/svg?seed=Michael",
        },
        {
            "id": "d5",
            "user_id": "u7",
            "name": "Dr. Linda Martinez",
            "specialty": "Pediatrics",
            "address": "555 Kids Way",
            "city": "Bronx",
            "state": "NY",
            "zip_code": "10451",
            "bio": "Dr. Martinez loves working with children and ensuring they grow up healthy and strong. She is known for her gentle approach and ability to put kids at ease.",
            "skills": ["Newborn Care", "Adolescent Medicine", "Immunizations"],
            "services": ["Well-child Visit", "Sick Visit", "School Physical"],
            "rates": "$175/consult",
            "image": "https://api.dicebear.com/9.x/avataaars/svg?seed=Linda",
        },
        {
            "id": "d6",
            "user_id": "u8",
            "name": "Dr. Robert Taylor",
            "specialty": "Orthopedics",
            "address": "999 Bone St",
            "city": "Staten Island",
            "state": "NY",
            "zip_code": "10301",
            "bio": "Specializing in sports medicine and joint replacement, Dr. Taylor helps athletes and seniors alike regain their mobility and live pain-free lives.",
            "skills": ["Joint Replacement", "Arthroscopy", "Sports Injury Rehab"],
            "services": ["X-Ray", "Surgery Consultation", "Fracture Care"],
            "rates": "$275/consult",
            "image": "https://api.dicebear.com/9.x/avataaars/svg?seed=Robert",
        },
    ]
    search_query: str = ""
    selected_specialty: str = ""
    page: int = 1
    limit: int = 6
    possible_limits: list[int] = [6, 12, 24]
    current_doctor_id: str = ""

    @rx.var
    def specialties(self) -> list[str]:
        specs = set((d["specialty"] for d in self.doctors))
        return sorted(list(specs))

    @rx.var
    def filtered_doctors(self) -> list[Doctor]:
        filtered = self.doctors
        if self.search_query:
            query = self.search_query.lower()
            filtered = [
                d
                for d in filtered
                if query in d["name"].lower()
                or query in d["specialty"].lower()
                or query in d["bio"].lower()
            ]
        if self.selected_specialty and self.selected_specialty != "All Specialties":
            filtered = [
                d for d in filtered if d["specialty"] == self.selected_specialty
            ]
        return filtered

    @rx.var
    def total_pages(self) -> int:
        return math.ceil(len(self.filtered_doctors) / self.limit)

    @rx.var
    def paginated_doctors(self) -> list[Doctor]:
        start = (self.page - 1) * self.limit
        end = start + self.limit
        return self.filtered_doctors[start:end]

    @rx.var
    def current_doctor(self) -> Optional[Doctor]:
        if not self.current_doctor_id:
            return None
        return next(
            (d for d in self.doctors if d["id"] == self.current_doctor_id), None
        )

    @rx.event
    def load_doctor_detail(self):
        """Load doctor details on page load."""
        self.current_doctor_id = self.router.url.query_parameters.get("id") or ""

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query
        self.page = 1

    @rx.event
    def set_specialty_filter(self, value: str):
        self.selected_specialty = value
        self.page = 1

    @rx.event
    def set_page(self, page: int):
        self.page = page

    @rx.event
    def set_limit(self, limit: str):
        self.limit = int(limit)
        self.page = 1

    @rx.event
    def next_page(self):
        if self.page < self.total_pages:
            self.page += 1

    @rx.event
    def prev_page(self):
        if self.page > 1:
            self.page -= 1

    @rx.event
    async def update_profile(self, form_data: dict):
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        if not auth_state.current_user:
            return
        user_id = auth_state.current_user["id"]
        doctor_idx = -1
        for i, d in enumerate(self.doctors):
            if d["user_id"] == user_id:
                doctor_idx = i
                break
        if doctor_idx != -1:
            doc = self.doctors[doctor_idx]
            doc["bio"] = form_data.get("bio", doc["bio"])
            doc["specialty"] = form_data.get("specialty", doc["specialty"])
            doc["rates"] = form_data.get("rates", doc["rates"])
            doc["address"] = form_data.get("address", doc["address"])
            if "skills" in form_data:
                doc["skills"] = [s.strip() for s in form_data["skills"].split(",")]
            if "services" in form_data:
                doc["services"] = [s.strip() for s in form_data["services"].split(",")]
            self.doctors[doctor_idx] = doc
            rx.toast.success("Profile updated successfully")
        else:
            pass