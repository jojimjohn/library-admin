"""Dashboard page for PTC Library Admin."""

import reflex as rx
from library_admin.state import State


def stat_card(title: str, value: str, icon: str, color: str) -> rx.Component:
    """Create a statistics card."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon(icon, size=24, color=color),
                rx.spacer(),
            ),
            rx.text(title, size="2", color="gray"),
            rx.text(value, size="6", weight="bold"),
            spacing="2",
            align="start",
        ),
        width="100%",
    )


def dashboard_stats() -> rx.Component:
    """Dashboard statistics grid."""
    return rx.box(
        rx.grid(
            stat_card(
                "Total Books",
                State.dashboard_stats.get("total_books", 0).to(str),
                "book",
                "blue"
            ),
            stat_card(
                "Available",
                State.dashboard_stats.get("available_books", 0).to(str),
                "circle-check",
                "green"
            ),
            stat_card(
                "Borrowed",
                State.dashboard_stats.get("borrowed_books", 0).to(str),
                "bookmark",
                "orange"
            ),
            stat_card(
                "Active Loans",
                State.dashboard_stats.get("active_loans", 0).to(str),
                "users",
                "purple"
            ),
            stat_card(
                "Overdue",
                State.dashboard_stats.get("overdue_books", 0).to(str),
                "circle-alert",
                "red"
            ),
            stat_card(
                "Due Soon",
                State.dashboard_stats.get("due_soon", 0).to(str),
                "clock",
                "yellow"
            ),
            stat_card(
                "Total Users",
                State.dashboard_stats.get("total_users", 0).to(str),
                "user",
                "indigo"
            ),
            columns="2",
            spacing="4",
            width="100%",
        ),
        width="100%",
    )


def dashboard_page() -> rx.Component:
    """Main dashboard page."""
    return rx.container(
        rx.vstack(
            # Header
            rx.heading("Dashboard", size="8", margin_bottom="4"),

            # Loading indicator
            rx.cond(
                State.is_loading,
                rx.spinner(size="3"),
            ),

            # Error message
            rx.cond(
                State.error_message != "",
                rx.callout(
                    State.error_message,
                    icon="circle-alert",
                    color_scheme="red",
                    role="alert",
                ),
            ),

            # Stats grid
            dashboard_stats(),

            # Refresh button
            rx.button(
                rx.icon("refresh-cw", size=18),
                "Refresh",
                on_click=State.load_dashboard_data,
                variant="soft",
                margin_top="4",
            ),

            spacing="4",
            width="100%",
            padding="4",
        ),
        max_width="800px",
    )
