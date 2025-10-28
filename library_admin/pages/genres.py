"""Genres management page for PTC Library Admin."""

import reflex as rx
from library_admin.state import State
from typing import Dict


def genre_card(genre: Dict) -> rx.Component:
    """Create a genre card."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(genre["genre_name"], size="5"),
                rx.spacer(),
                rx.badge(f"{genre['book_count']} books", variant="soft"),
                width="100%",
                align="center",
            ),
            rx.cond(
                genre.get("description", "") != "",
                rx.text(genre["description"], size="2", color="gray"),
            ),
            rx.hstack(
                rx.button(
                    rx.icon("pencil", size=16),
                    "Edit",
                    on_click=lambda: State.open_edit_genre_form(genre["genre_id"]),
                    size="2",
                    variant="soft",
                ),
                rx.cond(
                    genre["book_count"] == 0,
                    rx.button(
                        rx.icon("trash_2", size=16),
                        "Delete",
                        on_click=lambda: State.delete_genre_confirm(genre["genre_id"]),
                        size="2",
                        color_scheme="red",
                        variant="soft",
                    ),
                    rx.button(
                        rx.icon("trash_2", size=16),
                        "Delete",
                        size="2",
                        color_scheme="gray",
                        variant="soft",
                        disabled=True,
                    ),
                ),
                spacing="2",
                width="100%",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        width="100%",
    )


def genre_form_dialog() -> rx.Component:
    """Genre add/edit form dialog."""
    form_title = rx.cond(
        State.genre_form_mode == "add",
        "Add New Genre",
        "Edit Genre"
    )

    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=18),
                "Add Genre",
                on_click=State.open_add_genre_form,
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(form_title),
            rx.vstack(
                rx.cond(
                    State.genre_form_error != "",
                    rx.callout(
                        State.genre_form_error,
                        icon="circle_alert",
                        color_scheme="red",
                        role="alert",
                    ),
                ),
                rx.text("Genre Name", size="2", weight="bold"),
                rx.input(
                    placeholder="e.g., Theology",
                    value=State.genre_form_name,
                    on_change=State.set_genre_form_name,
                ),
                rx.text("Description (Optional)", size="2", weight="bold"),
                rx.text_area(
                    placeholder="Brief description of this genre...",
                    value=State.genre_form_description,
                    on_change=State.set_genre_form_description,
                    rows="3",
                ),
                spacing="3",
                width="100%",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        color_scheme="gray",
                        on_click=State.close_genre_form,
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        "Save",
                        on_click=State.save_genre,
                    ),
                ),
                spacing="3",
                margin_top="4",
                justify="end",
            ),
        ),
        open=State.genre_form_mode != "",
    )


def genres_page() -> rx.Component:
    """Main genres management page."""
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading("Genres", size="8"),
                rx.spacer(),
                genre_form_dialog(),
                width="100%",
                align="center",
            ),
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
            rx.cond(
                State.is_loading,
                rx.spinner(size="3"),
            ),
            rx.cond(
                State.genres_list.length() == 0,
                rx.callout(
                    "No genres found. Add your first genre!",
                    icon="info",
                    color_scheme="blue",
                ),
                rx.vstack(
                    rx.foreach(State.genres_list, genre_card),
                    spacing="3",
                    width="100%",
                ),
            ),
            spacing="4",
            width="100%",
            padding="4",
        ),
        max_width="800px",
    )
