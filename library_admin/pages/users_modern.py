"""Modern Users management page - Mobile-first design."""

import reflex as rx
from library_admin.state import State
from library_admin.components.modern_ui import (
    Colors,
    Gradients,
    modern_page_container,
    section_header,
    modern_input,
    list_item_modern,
    modern_button,
    empty_state,
)
from typing import Dict


def user_card_modern(user: Dict) -> rx.Component:
    """Modern user card."""
    return list_item_modern(
        rx.hstack(
            # Left: User icon with gradient
            rx.box(
                rx.icon(
                    rx.cond(user["role"] == "admin", "user_cog", "user"),
                    size=24,
                    color=Colors.white,
                ),
                background=rx.cond(
                    user["role"] == "admin",
                    Gradients.navy_gradient,
                    Gradients.light_blue_gradient
                ),
                border_radius="12px",
                padding="2",
                display="flex",
                align_items="center",
                justify_content="center",
            ),

            # Middle: User info
            rx.vstack(
                # Name and role
                rx.hstack(
                    rx.text(
                        user.get("name", "Unknown"),
                        size="3",
                        weight="bold",
                        color=Colors.dark_navy,
                    ),
                    rx.badge(
                        user["role"],
                        color_scheme=rx.cond(user["role"] == "admin", "blue", "gray"),
                        size="1",
                        border_radius="8px",
                    ),
                    spacing="2",
                    align="center",
                ),

                # Phone number
                rx.text(
                    user["user_id"],
                    size="1",
                    font_family="monospace",
                    color=Colors.dark_gray,
                ),

                # Active loans
                rx.hstack(
                    rx.icon("bookmark", size=14, color=Colors.dark_gray),
                    rx.text(
                        f"{user.get('active_loans', 0)} active loans",
                        size="1",
                        color=Colors.dark_gray,
                    ),
                    spacing="1",
                ),

                spacing="1",
                align="start",
                flex="1",
            ),

            # Right: Edit button
            rx.icon_button(
                rx.icon("pencil", size=16),
                on_click=lambda: State.open_edit_user_form(user["user_id"]),
                variant="ghost",
                color_scheme="blue",
                size="2",
            ),

            spacing="3",
            width="100%",
            align="start",
        ),
        margin_bottom="3",
    )


def user_form_modern() -> rx.Component:
    """Modern user edit dialog."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header
                rx.text(
                    "Edit User",
                    size="6",
                    weight="bold",
                    color=Colors.dark_navy,
                ),

                # Error message
                rx.cond(
                    State.user_form_error != "",
                    rx.box(
                        rx.hstack(
                            rx.icon("circle_alert", size=16, color=Colors.error_red),
                            rx.text(
                                State.user_form_error,
                                size="2",
                                color=Colors.error_red,
                            ),
                            spacing="2",
                        ),
                        background=f"{Colors.error_red}15",
                        border=f"1px solid {Colors.error_red}",
                        border_radius="8px",
                        padding="2",
                    ),
                ),

                # Form fields
                rx.vstack(
                    # Phone (disabled)
                    rx.vstack(
                        rx.text("Phone Number", size="2", weight="bold", color=Colors.dark_navy),
                        rx.input(
                            value=State.user_form_id,
                            disabled=True,
                            size="3",
                        ),
                        spacing="1",
                        width="100%",
                    ),

                    # Name
                    rx.vstack(
                        rx.text("Name", size="2", weight="bold", color=Colors.dark_navy),
                        modern_input(
                            placeholder="Enter name",
                            value=State.user_form_name,
                            on_change=State.set_user_form_name,
                            icon="user",
                        ),
                        spacing="1",
                        width="100%",
                    ),

                    # Role
                    rx.vstack(
                        rx.text("Role", size="2", weight="bold", color=Colors.dark_navy),
                        rx.select(
                            ["user", "admin"],
                            value=State.user_form_role,
                            on_change=State.set_user_form_role,
                            size="3",
                        ),
                        spacing="1",
                        width="100%",
                    ),

                    spacing="3",
                    width="100%",
                ),

                # Action buttons
                rx.hstack(
                    rx.dialog.close(
                        modern_button(
                            "Cancel",
                            variant="soft",
                            color_scheme="gray",
                            on_click=State.close_user_form,
                        ),
                    ),
                    rx.dialog.close(
                        modern_button(
                            "Save",
                            icon="check",
                            on_click=State.save_user,
                        ),
                    ),
                    spacing="2",
                    justify="end",
                    width="100%",
                ),

                spacing="4",
                width="100%",
            ),
            max_width="500px",
        ),

        open=State.user_form_mode != "",
    )


def users_page_modern() -> rx.Component:
    """Modern users page."""
    return modern_page_container(
        # Header with count
        section_header(
            title="Users",
            badge_value=State.users.length().to(str),
        ),

        # Success/Error messages
        rx.cond(
            State.success_message != "",
            rx.box(
                rx.hstack(
                    rx.icon("circle_check", size=18, color=Colors.success_green),
                    rx.text(
                        State.success_message,
                        size="2",
                        color=Colors.success_green,
                        weight="medium",
                    ),
                    spacing="2",
                ),
                background=f"{Colors.success_green}15",
                border=f"1px solid {Colors.success_green}",
                border_radius="12px",
                padding="3",
                cursor="pointer",
                on_click=State.clear_messages,
            ),
        ),

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
                cursor="pointer",
                on_click=State.clear_messages,
            ),
        ),

        # Search
        modern_input(
            placeholder="Search users...",
            value=State.user_search,
            on_change=State.set_user_search,
            on_key_up=lambda: State.search_users(),
            icon="search",
        ),

        # Users list
        rx.cond(
            State.users.length() == 0,
            empty_state(
                icon="users",
                title="No users found",
                description="No users match your search criteria",
            ),
            rx.vstack(
                rx.foreach(State.users, user_card_modern),
                spacing="0",
                width="100%",
            ),
        ),

        # Edit form dialog
        user_form_modern(),
    )
