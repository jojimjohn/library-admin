"""Compact Users management page - Professional Mobile Design."""

import reflex as rx
from library_admin.state import State
from typing import Dict


def user_row(user: Dict) -> rx.Component:
    """Compact user row."""
    role_color = rx.cond(user["role"] == "admin", "blue", "gray")

    return rx.box(
        rx.hstack(
            # User info
            rx.vstack(
                # Name + Role
                rx.hstack(
                    rx.text(user.get("name", "Unknown"), weight="bold", size="2"),
                    rx.badge(user["role"], color_scheme=role_color, size="1"),
                    rx.spacer(),
                    rx.badge(f"{user.get('active_loans', 0)} loans", variant="soft", size="1"),
                    width="100%",
                    align="center",
                ),

                # Phone number
                rx.text(user["user_id"], size="1", color="gray", font_family="mono"),

                spacing="1",
                flex="1",
            ),

            # Edit action
            rx.icon(
                "pencil",
                size=16,
                on_click=lambda: State.open_edit_user_form(user["user_id"]),
                cursor="pointer",
                color=rx.color("blue", 11),
            ),

            spacing="2",
            width="100%",
            align="start",
        ),
        padding="3",
        border_bottom=f"1px solid {rx.color('gray', 4)}",
        _hover={"background_color": rx.color("gray", 2)},
    )


def user_form_dialog() -> rx.Component:
    """Compact user edit form."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Edit User", size="5"),

            rx.vstack(
                rx.cond(
                    State.user_form_error != "",
                    rx.callout(State.user_form_error, icon="circle_alert", color_scheme="red", size="1"),
                ),

                # Form fields
                rx.vstack(
                    rx.hstack(
                        rx.text("Phone", size="1", weight="bold", width="60px"),
                        rx.input(
                            value=State.user_form_id,
                            disabled=True,
                            size="2",
                        ),
                        width="100%",
                        align="center",
                    ),

                    rx.hstack(
                        rx.text("Name", size="1", weight="bold", width="60px"),
                        rx.input(
                            value=State.user_form_name,
                            on_change=State.set_user_form_name,
                            size="2",
                            placeholder="User name",
                        ),
                        width="100%",
                        align="center",
                    ),

                    rx.hstack(
                        rx.text("Role", size="1", weight="bold", width="60px"),
                        rx.select(
                            ["user", "admin"],
                            value=State.user_form_role,
                            on_change=State.set_user_form_role,
                            size="2",
                        ),
                        width="100%",
                        align="center",
                    ),

                    spacing="2",
                    width="100%",
                ),

                # Actions
                rx.hstack(
                    rx.dialog.close(
                        rx.button("Cancel", variant="soft", size="2", on_click=State.close_user_form),
                    ),
                    rx.dialog.close(
                        rx.button("Save", size="2", on_click=State.save_user),
                    ),
                    spacing="2",
                    justify="end",
                    width="100%",
                ),

                spacing="3",
                width="100%",
            ),
        ),
        open=State.user_form_mode != "",
    )


def users_page() -> rx.Component:
    """Compact professional users page."""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading("Users", size="6"),
                rx.badge(State.users.length().to(str), variant="soft"),
                rx.spacer(),
                rx.icon("refresh_cw", size=16, on_click=State.load_users, cursor="pointer"),
                width="100%",
                align="center",
            ),

            # Messages
            rx.cond(State.success_message != "", rx.callout(State.success_message, icon="circle_check", color_scheme="green", size="1", on_click=State.clear_messages)),
            rx.cond(State.error_message != "", rx.callout(State.error_message, icon="circle_alert", color_scheme="red", size="1", on_click=State.clear_messages)),

            # Search
            rx.input(
                placeholder="Search users...",
                value=State.user_search,
                on_change=State.set_user_search,
                on_key_up=lambda: State.search_users(),
                size="2",
            ),

            # Users list
            rx.box(
                rx.cond(
                    State.users.length() == 0,
                    rx.box(rx.text("No users found", size="2", color="gray", align="center"), padding="4"),
                    rx.foreach(State.users, user_row),
                ),
                border=f"1px solid {rx.color('gray', 4)}",
                border_radius="8px",
                overflow="hidden",
            ),

            user_form_dialog(),

            spacing="3",
            padding="3",
        ),
        width="100%",
    )
