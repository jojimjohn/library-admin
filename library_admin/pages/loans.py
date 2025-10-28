"""Loans management page for PTC Library Admin."""

import reflex as rx
from library_admin.state import State
from typing import Dict


def loan_card(loan: Dict) -> rx.Component:
    """Create a loan card for mobile view."""
    # Determine status color
    status_color = rx.cond(
        loan["status"] == "overdue",
        "red",
        rx.cond(
            loan["status"] == "due_soon",
            "yellow",
            "green"
        )
    )

    # Status badge text
    status_text = rx.cond(
        loan["status"] == "overdue",
        "OVERDUE",
        rx.cond(
            loan["status"] == "due_soon",
            "DUE SOON",
            "OK"
        )
    )

    return rx.card(
        rx.vstack(
            # Header: Status and Loan Date
            rx.hstack(
                rx.badge(
                    status_text,
                    color_scheme=status_color,
                    size="2",
                ),
                rx.spacer(),
                rx.text(
                    f"Borrowed: {loan.get('borrow_date', 'N/A')}",
                    size="1",
                    color="gray",
                ),
                width="100%",
            ),

            # Book Title
            rx.heading(loan.get("title", "Unknown Book"), size="4"),

            # Book Details
            rx.hstack(
                rx.badge(loan.get("book_id", ""), variant="outline", size="1"),
                rx.text(f"by {loan.get('author', 'Unknown')}", size="2", color="gray"),
                spacing="2",
            ),

            # User Info
            rx.box(
                rx.text(
                    f"Borrowed by: {loan.get('user_id', 'Unknown')}",
                    size="2",
                    weight="medium",
                ),
                margin_top="2",
            ),

            # Due Date Info
            rx.box(
                rx.hstack(
                    rx.icon("calendar", size=16),
                    rx.text(
                        f"Due: {loan.get('due_date', 'N/A')}",
                        size="2",
                        weight="medium",
                    ),
                    rx.text(
                        f"({loan.get('days_remaining', 0)} days)",
                        size="2",
                        color=status_color,
                    ),
                    spacing="2",
                ),
                margin_top="2",
            ),

            spacing="3",
            align="start",
            width="100%",
        ),
        width="100%",
    )


def loans_filters() -> rx.Component:
    """Loans search and filter controls."""
    return rx.vstack(
        # Search bar
        rx.hstack(
            rx.input(
                placeholder="Search by book, user, or book ID...",
                value=State.loan_search,
                on_change=State.set_loan_search,
                width="100%",
            ),
            rx.button(
                rx.icon("search", size=18),
                on_click=State.search_loans,
                size="3",
            ),
            width="100%",
        ),

        # Filter by status
        rx.hstack(
            rx.select(
                ["all", "ok", "due_soon", "overdue"],
                placeholder="Status",
                value=State.loan_filter_status,
                on_change=State.set_loan_filter_status,
                width="100%",
            ),
            rx.button(
                rx.icon("x", size=18),
                "Clear",
                on_click=State.clear_loan_filters,
                variant="soft",
                color_scheme="gray",
            ),
            width="100%",
            spacing="2",
        ),

        spacing="3",
        width="100%",
    )


def loans_list() -> rx.Component:
    """Loans list with cards."""
    return rx.box(
        rx.cond(
            State.active_loans.length() == 0,
            rx.callout(
                "No active loans found. All books are available!",
                icon="info",
                color_scheme="blue",
            ),
            rx.vstack(
                rx.foreach(State.active_loans, loan_card),
                spacing="3",
                width="100%",
            ),
        ),
        width="100%",
    )


def loans_page() -> rx.Component:
    """Main loans management page."""
    return rx.container(
        rx.vstack(
            # Header
            rx.heading("Active Loans", size="8", margin_bottom="4"),

            # Success message
            rx.cond(
                State.success_message != "",
                rx.callout(
                    State.success_message,
                    icon="circle_check",
                    color_scheme="green",
                    role="status",
                    on_click=State.clear_messages,
                ),
            ),

            # Error message
            rx.cond(
                State.error_message != "",
                rx.callout(
                    State.error_message,
                    icon="circle_alert",
                    color_scheme="red",
                    role="alert",
                    on_click=State.clear_messages,
                ),
            ),

            # Loading indicator
            rx.cond(
                State.is_loading,
                rx.hstack(
                    rx.spinner(size="3"),
                    rx.text(State.loading_message, size="2"),
                    spacing="2",
                ),
            ),

            # Filters
            loans_filters(),

            # Loans list
            loans_list(),

            spacing="4",
            width="100%",
            padding="4",
        ),
        max_width="800px",
    )
