"""Modern Genres management page."""

import reflex as rx
from library_admin.state import State
from library_admin.components.modern_ui import (
    Colors,
    Gradients,
    gradient_card,
    modern_page_container,
    section_header,
    modern_button,
    modern_input,
    empty_state,
)
from typing import Dict


def genre_card_modern(genre: Dict) -> rx.Component:
    """Modern genre card with gradient."""
    return gradient_card(
        rx.vstack(
            # Genre name and book count
            rx.hstack(
                rx.text(
                    genre["genre_name"],
                    size="5",
                    weight="bold",
                    color=Colors.white,
                ),
                rx.spacer(),
                rx.badge(
                    f"{genre['book_count']} books",
                    color_scheme="whiteAlpha",
                    size="2",
                ),
                width="100%",
                align="center",
            ),

            # Description
            rx.cond(
                genre.get("description", "") != "",
                rx.text(
                    genre["description"],
                    size="2",
                    color=Colors.white,
                    opacity="0.9",
                ),
            ),

            # Action buttons
            rx.hstack(
                modern_button(
                    "Edit",
                    icon="pencil",
                    on_click=lambda: State.open_edit_genre_form(genre["genre_id"]),
                    variant="soft",
                    color_scheme="whiteAlpha",
                ),
                rx.cond(
                    genre["book_count"] == 0,
                    modern_button(
                        "Delete",
                        icon="trash_2",
                        on_click=lambda: State.delete_genre_confirm(genre["genre_id"]),
                        variant="soft",
                        color_scheme="red",
                    ),
                    rx.box(
                        modern_button(
                            "Delete",
                            icon="trash_2",
                            variant="soft",
                            color_scheme="gray",
                        ),
                        opacity="0.5",
                        cursor="not-allowed",
                    ),
                ),
                spacing="2",
            ),

            spacing="3",
            align="start",
            width="100%",
        ),
        gradient=Gradients.light_blue_gradient,
        margin_bottom="3",
    )


def genre_form_modern() -> rx.Component:
    """Modern genre add/edit dialog."""
    form_title = rx.cond(State.genre_form_mode == "add", "Add Genre", "Edit Genre")

    return rx.dialog.root(
        rx.dialog.trigger(
            rx.box(
                rx.icon("plus", size=20, color=Colors.white),
                background=Gradients.mint_gradient,
                border_radius="12px",
                padding="3",
                cursor="pointer",
                _hover={"transform": "scale(1.05)", "transition": "transform 0.2s"},
                on_click=State.open_add_genre_form,
            ),
        ),

        rx.dialog.content(
            rx.vstack(
                # Header
                rx.text(
                    form_title,
                    size="6",
                    weight="bold",
                    color=Colors.dark_navy,
                ),

                # Error message
                rx.cond(
                    State.genre_form_error != "",
                    rx.box(
                        rx.hstack(
                            rx.icon("circle_alert", size=16, color=Colors.error_red),
                            rx.text(State.genre_form_error, size="2", color=Colors.error_red),
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
                    # Genre Name
                    rx.vstack(
                        rx.text("Genre Name", size="2", weight="bold", color=Colors.dark_navy),
                        modern_input(
                            placeholder="Enter genre name",
                            value=State.genre_form_name,
                            on_change=State.set_genre_form_name,
                            icon="library",
                        ),
                        spacing="1",
                        width="100%",
                    ),

                    # Description
                    rx.vstack(
                        rx.text("Description (Optional)", size="2", weight="bold", color=Colors.dark_navy),
                        rx.text_area(
                            placeholder="Enter genre description...",
                            value=State.genre_form_description,
                            on_change=State.set_genre_form_description,
                            rows="3",
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
                            on_click=State.close_genre_form,
                        ),
                    ),
                    rx.dialog.close(
                        modern_button(
                            "Save",
                            icon="check",
                            on_click=State.save_genre,
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

        open=State.genre_form_mode != "",
    )


def genres_page_modern() -> rx.Component:
    """Modern genres page."""
    return modern_page_container(
        # Header with add button
        rx.hstack(
            section_header(
                title="Genres",
                badge_value=State.genres_list.length().to(str),
            ),
            rx.spacer(),
            genre_form_modern(),
            width="100%",
            align="center",
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

        # Genres list
        rx.cond(
            State.genres_list.length() == 0,
            empty_state(
                icon="library",
                title="No genres yet",
                description="Add your first genre to organize your library books",
                action_text="Add Genre",
                on_action=State.open_add_genre_form,
            ),
            rx.vstack(
                rx.foreach(State.genres_list, genre_card_modern),
                spacing="0",
                width="100%",
            ),
        ),
    )
