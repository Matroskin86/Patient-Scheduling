import reflex as rx
from app.components.layout import layout
from app.states.document_state import DocumentState
from app.states.models import Document


def document_row(doc: Document) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.icon("file-text", class_name="w-5 h-5 text-gray-400 mr-3"),
                rx.el.span(doc["name"], class_name="font-medium text-gray-900"),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            doc["type"], class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
        ),
        rx.el.td(
            doc["date"], class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
        ),
        rx.el.td(
            rx.el.div(
                rx.el.a(
                    rx.el.button(
                        "View",
                        class_name="text-[#6b2d5b] hover:text-[#5a254c] text-sm font-medium mr-4",
                    ),
                    href=rx.get_upload_url(doc["filename"]),
                    target="_blank",
                ),
                rx.el.button(
                    "Delete",
                    on_click=lambda: DocumentState.delete_document(doc["id"]),
                    class_name="text-red-600 hover:text-red-900 text-sm font-medium",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
    )


def my_documents_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "My Medical Documents",
                class_name="text-2xl font-bold text-gray-900 mb-2",
            ),
            rx.el.p(
                "Securely store and access your medical records.",
                class_name="text-gray-500 mb-8",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Upload New Document",
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.upload.root(
                    rx.el.div(
                        rx.icon(
                            "cloud-upload", class_name="w-10 h-10 text-gray-400 mb-2"
                        ),
                        rx.el.p(
                            "Drag and drop or click to upload",
                            class_name="text-sm text-gray-600 font-medium",
                        ),
                        rx.el.p(
                            "PDF, JPG, PNG up to 10MB",
                            class_name="text-xs text-gray-400 mt-1",
                        ),
                        class_name="flex flex-col items-center justify-center p-6 border-2 border-dashed border-gray-300 rounded-xl hover:bg-gray-50 transition-colors cursor-pointer",
                    ),
                    id="doc_upload",
                    accept={
                        "application/pdf": [".pdf"],
                        "image/png": [".png"],
                        "image/jpeg": [".jpg", ".jpeg"],
                    },
                    multiple=True,
                    class_name="w-full mb-4",
                ),
                rx.el.div(
                    rx.foreach(
                        rx.selected_files("doc_upload"),
                        lambda file: rx.el.div(
                            rx.icon(
                                "paperclip", class_name="w-4 h-4 text-gray-500 mr-2"
                            ),
                            rx.el.span(
                                file, class_name="text-sm text-gray-700 truncate"
                            ),
                            class_name="flex items-center p-2 bg-gray-50 rounded-lg border border-gray-200",
                        ),
                    ),
                    class_name="flex flex-col gap-2 mb-4",
                ),
                rx.el.button(
                    rx.cond(
                        DocumentState.uploading,
                        rx.el.span("Uploading..."),
                        rx.el.span("Upload Selected Files"),
                    ),
                    on_click=DocumentState.handle_upload(
                        rx.upload_files(upload_id="doc_upload")
                    ),
                    disabled=DocumentState.uploading,
                    class_name="bg-[#6b2d5b] text-white px-4 py-2 rounded-lg hover:bg-[#5a254c] font-medium disabled:opacity-50 disabled:cursor-not-allowed text-sm",
                ),
                class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-8",
            )
        ),
        rx.cond(
            DocumentState.my_documents.length() > 0,
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Name",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Type",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Date",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Actions",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                        ),
                        class_name="bg-gray-50",
                    ),
                    rx.el.tbody(
                        rx.foreach(DocumentState.my_documents, document_row),
                        class_name="bg-white divide-y divide-gray-200",
                    ),
                    class_name="min-w-full divide-y divide-gray-200",
                ),
                class_name="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden overflow-x-auto",
            ),
            rx.el.div(
                rx.icon("folder-open", class_name="w-12 h-12 text-gray-300 mb-3"),
                rx.el.h3(
                    "No documents found", class_name="text-lg font-medium text-gray-900"
                ),
                rx.el.p(
                    "Upload medical records to keep them safe.",
                    class_name="text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center py-12 bg-white rounded-xl border border-gray-200 border-dashed",
            ),
        ),
        class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
    )


def my_documents_page() -> rx.Component:
    return layout(my_documents_content())