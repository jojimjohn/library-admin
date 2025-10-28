"""Compact Loans management page - Professional Mobile Design."""

import reflex as rx
from library_admin.state import State
from typing import Dict


def status_badge(status: str) -> rx.Component:
    """Compact status indicator."""
    return rx.cond(
        status == "overdue",
        rx.badge("!", color_scheme="red", size="1"),
        rx.cond(
            status == "due_soon",
            rx.badge("⚠", color_scheme="yellow", size="1"),
            rx.badge("✓", color_scheme="green", size="1")
        )
    )


def loan_row(loan: Dict) -> rx.Component:
    """Compact loan row with all info and notification button."""
    return rx.box(
        rx.hstack(
            # Status indicator (left edge)
            status_badge(loan["status"]),

            # Main content area
            rx.vstack(
                # Row 1: Book title (bold) + Days remaining
                rx.hstack(
                    rx.text(loan.get("title", "Unknown"), weight="bold", size="2"),
                    rx.spacer(),
                    rx.text(
                        f"{loan.get('days_remaining', 0)}d",
                        size="1",
                        color=rx.cond(
                            loan["status"] == "overdue",
                            "red",
                            rx.cond(loan["status"] == "due_soon", "yellow", "gray")
                        ),
                    ),
                    width="100%",
                    align="center",
                ),

                # Row 2: User name + Book ID
                rx.hstack(
                    rx.text(loan.get("name", "Unknown User"), size="1", color="gray"),
                    rx.text("•", size="1", color="gray"),
                    rx.text(loan.get("book_id", ""), size="1", color="gray"),
                    spacing="1",
                ),

                spacing="1",
                flex="1",
            ),

            # Quick notification button (right edge)
            rx.cond(
                loan["status"] != "ok",  # Only show button for overdue or due_soon
                rx.icon_button(
                    rx.icon("send", size=14),
                    on_click=lambda: State.send_notification_to_loan_user(
                        loan.get("user_id"),
                        loan.get("title"),
                        loan.get("status")
                    ),
                    size="1",
                    variant="ghost",
                    color_scheme=rx.cond(
                        loan["status"] == "overdue",
                        "red",
                        "yellow"
                    ),
                ),
            ),

            spacing="2",
            width="100%",
            align="start",
        ),
        padding="3",
        border_bottom=f"1px solid {rx.color('gray', 4)}",
        _hover={"background_color": rx.color("gray", 2)},
    )


def compact_search_bar() -> rx.Component:
    """Compact search with filter chips."""
    return rx.vstack(
        # Search input
        rx.input(
            placeholder="Search loans...",
            value=State.loan_search,
            on_change=State.set_loan_search,
            on_key_up=lambda: State.search_loans(),
            size="2",
            width="100%",
        ),

        # Filter chips
        rx.hstack(
            rx.badge(
                "All",
                variant=rx.cond(State.loan_filter_status == "all", "solid", "soft"),
                color_scheme="blue",
                on_click=lambda: State.set_loan_filter_status("all"),
                cursor="pointer",
                size="1",
            ),
            rx.badge(
                "OK",
                variant=rx.cond(State.loan_filter_status == "ok", "solid", "soft"),
                color_scheme="green",
                on_click=lambda: State.set_loan_filter_status("ok"),
                cursor="pointer",
                size="1",
            ),
            rx.badge(
                "Due Soon",
                variant=rx.cond(State.loan_filter_status == "due_soon", "solid", "soft"),
                color_scheme="yellow",
                on_click=lambda: State.set_loan_filter_status("due_soon"),
                cursor="pointer",
                size="1",
            ),
            rx.badge(
                "Overdue",
                variant=rx.cond(State.loan_filter_status == "overdue", "solid", "soft"),
                color_scheme="red",
                on_click=lambda: State.set_loan_filter_status("overdue"),
                cursor="pointer",
                size="1",
            ),
            spacing="2",
            wrap="wrap",
        ),
        spacing="2",
        width="100%",
    )


def loans_page_v2() -> rx.Component:
    """Compact professional loans page."""
    return rx.box(
        rx.vstack(
            # Header with count
            rx.hstack(
                rx.heading("Loans", size="6"),
                rx.badge(State.active_loans.length().to(str), variant="soft"),
                rx.spacer(),
                rx.icon("refresh_cw", size=16, on_click=State.load_active_loans, cursor="pointer"),
                width="100%",
                align="center",
            ),

            # Messages
            rx.cond(
                State.error_message != "",
                rx.callout(State.error_message, icon="circle_alert", color_scheme="red", size="1"),
            ),

            # Search and filters
            compact_search_bar(),

            # Loans list (compact)
            rx.box(
                rx.cond(
                    State.active_loans.length() == 0,
                    rx.box(
                        rx.text("No loans found", size="2", color="gray", align="center"),
                        padding="4",
                    ),
                    rx.foreach(State.active_loans, loan_row),
                ),
                border=f"1px solid {rx.color('gray', 4)}",
                border_radius="8px",
                overflow="hidden",
            ),

            spacing="3",
            padding="3",
        ),
        width="100%",
    )
