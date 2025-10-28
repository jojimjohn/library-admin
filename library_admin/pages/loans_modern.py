"""Modern Loans management page - Mobile-first design with gradients."""

import reflex as rx
from library_admin.state import State
from library_admin.components.modern_ui import (
    Colors,
    Gradients,
    modern_page_container,
    section_header,
    modern_input,
    filter_chip,
    list_item_modern,
    empty_state,
)
from typing import Dict


def loan_card_modern(loan: Dict) -> rx.Component:
    """Modern loan card with status indicators."""
    # Determine status colors and icons
    status_config = rx.match(
        loan["status"],
        ("overdue", {"color": Colors.error_red, "icon": "circle_alert", "label": "Overdue"}),
        ("due_soon", {"color": Colors.warning_orange, "icon": "clock", "label": "Due Soon"}),
        ("ok", {"color": Colors.success_green, "icon": "circle_check", "label": "On Time"}),
        {"color": Colors.dark_gray, "icon": "circle", "label": "Unknown"},
    )

    return list_item_modern(
        rx.hstack(
            # Left: Status indicator with gradient
            rx.box(
                rx.icon(
                    rx.cond(
                        loan["status"] == "overdue",
                        "circle_alert",
                        rx.cond(
                            loan["status"] == "due_soon",
                            "clock",
                            "circle_check"
                        )
                    ),
                    size=24,
                    color=Colors.white,
                ),
                background=rx.cond(
                    loan["status"] == "overdue",
                    f"linear-gradient(135deg, {Colors.error_red} 0%, #C62828 100%)",
                    rx.cond(
                        loan["status"] == "due_soon",
                        f"linear-gradient(135deg, {Colors.warning_orange} 0%, #F57C00 100%)",
                        Gradients.mint_gradient
                    )
                ),
                border_radius="12px",
                padding="2",
                display="flex",
                align_items="center",
                justify_content="center",
            ),

            # Middle: Loan info
            rx.vstack(
                # Book title
                rx.text(
                    loan.get("title", "Unknown Book"),
                    size="3",
                    weight="bold",
                    color=Colors.dark_navy,
                ),

                # User name and book ID
                rx.hstack(
                    rx.text(
                        loan.get("name", "Unknown User"),
                        size="2",
                        color=Colors.dark_gray,
                    ),
                    rx.text("•", size="1", color=Colors.gray),
                    rx.text(
                        loan.get("book_id", ""),
                        size="1",
                        font_family="monospace",
                        color=Colors.dark_gray,
                    ),
                    spacing="1",
                ),

                # Days remaining with color
                rx.text(
                    f"{loan.get('days_remaining', 0)} days remaining",
                    size="1",
                    color=rx.cond(
                        loan["status"] == "overdue",
                        Colors.error_red,
                        rx.cond(
                            loan["status"] == "due_soon",
                            Colors.warning_orange,
                            Colors.dark_gray
                        )
                    ),
                    weight="medium",
                ),

                spacing="1",
                align="start",
                flex="1",
            ),

            # Right: Quick action button
            rx.cond(
                loan["status"] != "ok",
                rx.icon_button(
                    rx.icon("send", size=16),
                    on_click=lambda: State.send_notification_to_loan_user(
                        loan.get("user_id"),
                        loan.get("title"),
                        loan.get("status")
                    ),
                    variant="soft",
                    color_scheme=rx.cond(
                        loan["status"] == "overdue",
                        "red",
                        "orange"
                    ),
                    size="2",
                ),
            ),

            spacing="3",
            width="100%",
            align="start",
        ),
        margin_bottom="3",
    )


def filters_loans_modern() -> rx.Component:
    """Modern filters for loans."""
    return rx.vstack(
        # Search input
        modern_input(
            placeholder="Search loans...",
            value=State.loan_search,
            on_change=State.set_loan_search,
            on_key_up=lambda: State.search_loans(),
            icon="search",
        ),

        # Status filters
        rx.hstack(
            filter_chip(
                "All",
                is_active=State.loan_filter_status == "all",
                on_click=lambda: State.set_loan_filter_status("all"),
            ),
            filter_chip(
                "On Time",
                is_active=State.loan_filter_status == "ok",
                on_click=lambda: State.set_loan_filter_status("ok"),
                color_scheme="green",
            ),
            filter_chip(
                "Due Soon",
                is_active=State.loan_filter_status == "due_soon",
                on_click=lambda: State.set_loan_filter_status("due_soon"),
                color_scheme="orange",
            ),
            filter_chip(
                "Overdue",
                is_active=State.loan_filter_status == "overdue",
                on_click=lambda: State.set_loan_filter_status("overdue"),
                color_scheme="red",
            ),
            spacing="2",
            wrap="wrap",
        ),

        spacing="3",
        width="100%",
    )


def loans_page_modern() -> rx.Component:
    """Modern loans page with gradient cards."""
    return modern_page_container(
        # Header with count and refresh
        rx.hstack(
            section_header(
                title="Active Loans",
                badge_value=State.active_loans.length().to(str),
            ),
            rx.spacer(),
            rx.icon_button(
                rx.icon("refresh_cw", size=18),
                on_click=State.load_active_loans,
                variant="ghost",
                size="2",
            ),
            width="100%",
            align="center",
        ),

        # Error message
        rx.cond(
            State.error_message != "",
            rx.box(
                rx.hstack(
                    rx.icon("circle_alert", size=18, color=Colors.error_red),
                    rx.text(
                        State.error_message,
                        size="2",
                        color=Colors.error_red,
                        weight="medium",
                    ),
                    spacing="2",
                ),
                background=f"{Colors.error_red}15",
                border=f"1px solid {Colors.error_red}",
                border_radius="12px",
                padding="3",
            ),
        ),

        # Filters
        filters_loans_modern(),

        # Loans list
        rx.cond(
            State.active_loans.length() == 0,
            empty_state(
                icon="bookmark",
                title="No active loans",
                description="All books have been returned or no loans match your filters",
            ),
            rx.vstack(
                rx.foreach(State.active_loans, loan_card_modern),
                spacing="0",
                width="100%",
            ),
        ),
    )
