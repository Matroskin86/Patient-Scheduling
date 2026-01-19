import reflex as rx
from app.states.models import Document
from app.states.auth_state import AuthState
import datetime
import os


class DocumentState(rx.State):
    documents: list[Document] = [
        {
            "id": "doc1",
            "user_id": "u1",
            "name": "Blood Test Results",
            "date": "2024-10-15",
            "filename": "blood_test.pdf",
            "type": "Lab Report",
        },
        {
            "id": "doc2",
            "user_id": "u1",
            "name": "Chest X-Ray",
            "date": "2024-09-20",
            "filename": "xray.jpg",
            "type": "Imaging",
        },
    ]
    uploading: bool = False

    @rx.var
    async def my_documents(self) -> list[Document]:
        auth_state = await self.get_state(AuthState)
        if not auth_state.current_user:
            return []
        return [
            d for d in self.documents if d["user_id"] == auth_state.current_user["id"]
        ]

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        auth_state = await self.get_state(AuthState)
        if not auth_state.current_user:
            return
        self.uploading = True
        upload_dir = rx.get_upload_dir()
        upload_dir.mkdir(parents=True, exist_ok=True)
        for file in files:
            data = await file.read()
            file_path = upload_dir / file.name
            with file_path.open("wb") as f:
                f.write(data)
            new_doc: Document = {
                "id": f"doc{len(self.documents) + 1}",
                "user_id": auth_state.current_user["id"],
                "name": file.name.split(".")[0].replace("_", " ").title(),
                "date": datetime.date.today().isoformat(),
                "filename": file.name,
                "type": "Uploaded",
            }
            self.documents.append(new_doc)
        self.uploading = False
        return rx.toast.success("Document uploaded successfully")

    @rx.event
    def delete_document(self, doc_id: str):
        self.documents = [d for d in self.documents if d["id"] != doc_id]