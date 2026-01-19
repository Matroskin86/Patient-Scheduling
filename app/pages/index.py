import reflex as rx
from app.components.layout import layout
from app.components.doctor_card import doctor_card
from app.states.doctor_state import DoctorState


def filter_sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Filters",
                class_name="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2",
            ),
            rx.el.div(
                rx.el.label(
                    "Search", class_name="text-sm font-medium text-gray-700 mb-2 block"
                ),
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400",
                    ),
                    rx.el.input(
                        placeholder="Name, specialty, keyword...",
                        on_change=DoctorState.set_search_query.debounce(500),
                        class_name="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent text-sm",
                    ),
                    class_name="relative",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.label(
                    "Specialty",
                    class_name="text-sm font-medium text-gray-700 mb-2 block",
                ),
                rx.el.select(
                    rx.el.option("All Specialties", value=""),
                    rx.foreach(
                        DoctorState.specialties, lambda s: rx.el.option(s, value=s)
                    ),
                    on_change=DoctorState.set_specialty_filter,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent text-sm bg-white",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.label(
                    "Doctors per page",
                    class_name="text-sm font-medium text-gray-700 mb-2 block",
                ),
                rx.el.select(
                    rx.foreach(
                        DoctorState.possible_limits,
                        lambda l: rx.el.option(f"{l} results", value=l.to_string()),
                    ),
                    on_change=DoctorState.set_limit,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6b2d5b] focus:border-transparent text-sm bg-white",
                ),
            ),
            class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200 sticky top-24",
        ),
        class_name="w-full lg:w-64 flex-shrink-0 mb-8 lg:mb-0 lg:mr-8",
    )


def doctor_grid() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Book an appointment with a doctor",
                class_name="text-2xl md:text-3xl font-bold text-gray-900 mb-2",
            ),
            rx.el.p(
                "Find the right specialist for your needs and book instantly.",
                class_name="text-gray-500 mb-6",
            ),
            class_name="mb-6",
        ),
        rx.cond(
            DoctorState.paginated_doctors.length() > 0,
            rx.el.div(
                rx.el.div(
                    rx.foreach(DoctorState.paginated_doctors, doctor_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("chevron-left", class_name="w-5 h-5"),
                        on_click=DoctorState.prev_page,
                        disabled=DoctorState.page == 1,
                        class_name="p-2 rounded-lg border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed bg-white",
                    ),
                    rx.el.span(
                        f"Page {DoctorState.page} of {DoctorState.total_pages}",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.el.button(
                        rx.icon("chevron-right", class_name="w-5 h-5"),
                        on_click=DoctorState.next_page,
                        disabled=DoctorState.page == DoctorState.total_pages,
                        class_name="p-2 rounded-lg border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed bg-white",
                    ),
                    class_name="flex items-center justify-center gap-4 mt-8",
                ),
            ),
            rx.el.div(
                rx.icon("search-x", class_name="w-12 h-12 text-gray-300 mb-3"),
                rx.el.h3(
                    "No doctors found", class_name="text-lg font-medium text-gray-900"
                ),
                rx.el.p(
                    "Try adjusting your search or filters.", class_name="text-gray-500"
                ),
                class_name="flex flex-col items-center justify-center py-12 bg-white rounded-xl border border-gray-200 border-dashed",
            ),
        ),
        class_name="flex-1",
    )


def index_content() -> rx.Component:
    return rx.el.div(
        filter_sidebar(),
        doctor_grid(),
        class_name="flex flex-col lg:flex-row max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
    )


def index() -> rx.Component:
    return layout(index_content())