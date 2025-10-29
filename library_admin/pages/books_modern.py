"""Modern Books management page - Inspired by modern mobile app design."""

import reflex as rx
from library_admin.state import State
from library_admin.components.modern_ui import (
    Colors,
    Gradients,
    Shadows,
    modern_page_container,
    section_header,
    modern_input,
    filter_chip,
    list_item_modern,
    modern_button,
    empty_state,
)
from typing import Dict


def book_card_modern(book: Dict) -> rx.Component:
    """Modern book card with clean design."""
    # Determine status color and icon
    status_color = rx.cond(book["status"] == "available", Colors.success_green, Colors.warning_orange)
    status_icon = rx.cond(book["status"] == "available", "circle_check", "bookmark")

    return list_item_modern(
        rx.hstack(
            # Left side: Book icon with gradient background
            rx.box(
                rx.icon("book_open", size=28, color=Colors.white),
                background=Gradients.light_blue_gradient,
                border_radius="12px",
                padding="3",
                display="flex",
                align_items="center",
                justify_content="center",
            ),

            # Middle: Book info
            rx.vstack(
                # Title
                rx.text(
                    book["title"],
                    size="3",
                    weight="bold",
                    color=Colors.dark_navy,
                ),

                # Author & Genre
                rx.hstack(
                    rx.text(
                        book["author"],
                        size="1",
                        color=Colors.dark_gray,
                    ),
                    rx.text("•", size="1", color=Colors.gray),
                    rx.badge(
                        book["genre"],
                        color_scheme="gray",
                        size="1",
                        border_radius="8px",
                    ),
                    spacing="1",
                    align="center",
                ),

                # Book ID and borrowed info
                rx.hstack(
                    rx.text(
                        book["book_id"],
                        size="1",
                        font_family="monospace",
                        color=Colors.dark_gray,
                        opacity="0.7",
                    ),
                    rx.cond(
                        book["status"] == "borrowed",
                        rx.text(
                            f"→ {book.get('loaned_to', 'Unknown')}",
                            size="1",
                            color=Colors.warning_orange,
                            weight="medium",
                        ),
                    ),
                    spacing="2",
                ),

                spacing="1",
                align="start",
                flex="1",
            ),

            # Right side: Status badge and actions
            rx.vstack(
                # Status indicator
                rx.box(
                    rx.icon(status_icon, size=18, color=status_color),
                    background=f"{status_color}20",
                    border_radius="8px",
                    padding="2",
                ),

                # Action buttons
                rx.hstack(
                    rx.icon_button(
                        rx.icon("pencil", size=16),
                        on_click=lambda: State.open_edit_book_form(book["book_id"]),
                        variant="ghost",
                        color_scheme="blue",
                        size="1",
                    ),
                    rx.icon_button(
                        rx.icon("trash_2", size=16),
                        on_click=lambda: State.delete_book_confirm(book["book_id"]),
                        variant="ghost",
                        color_scheme="red",
                        size="1",
                    ),
                    spacing="1",
                ),

                spacing="2",
                align="end",
            ),

            spacing="3",
            width="100%",
            align="start",
        ),
        margin_bottom="3",
    )


def book_form_modern() -> rx.Component:
    """Modern book add/edit dialog."""
    form_title = rx.cond(State.book_form_mode == "add", "Add New Book", "Edit Book")

    return rx.dialog.root(
        rx.dialog.trigger(
            rx.box(
                rx.icon("plus", size=20, color=Colors.white),
                background=Gradients.mint_gradient,
                border_radius="12px",
                padding="3",
                cursor="pointer",
                _hover={
                    "transform": "scale(1.05)",
                    "transition": "transform 0.2s",
                },
                on_click=State.open_add_book_form,
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
                    State.book_form_error != "",
                    rx.box(
                        rx.hstack(
                            rx.icon("circle_alert", size=16, color=Colors.error_red),
                            rx.text(
                                State.book_form_error,
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
                    # Book ID
                    rx.vstack(
                        rx.text("Book ID", size="2", weight="bold", color=Colors.dark_navy),
                        modern_input(
                            placeholder="BOOK001",
                            value=State.book_form_id,
                            on_change=State.set_book_form_id,
                        ),
                        spacing="1",
                        width="100%",
                    ),

                    # Title
                    rx.vstack(
                        rx.text("Title", size="2", weight="bold", color=Colors.dark_navy),
                        modern_input(
                            placeholder="Enter book title",
                            value=State.book_form_title,
                            on_change=State.set_book_form_title,
                            icon="book_open",
                        ),
                        spacing="1",
                        width="100%",
                    ),

                    # Author
                    rx.vstack(
                        rx.text("Author", size="2", weight="bold", color=Colors.dark_navy),
                        modern_input(
                            placeholder="Enter author name",
                            value=State.book_form_author,
                            on_change=State.set_book_form_author,
                            icon="user",
                        ),
                        spacing="1",
                        width="100%",
                    ),

                    # Genre
                    rx.vstack(
                        rx.text("Genre", size="2", weight="bold", color=Colors.dark_navy),
                        rx.select(
                            State.genres,
                            value=State.book_form_genre,
                            on_change=State.set_book_form_genre,
                            placeholder="Select genre...",
                            size="3",
                        ),
                        spacing="1",
                        width="100%",
                    ),

                    spacing="3",
                    width="100%",
                ),

                # Notification checkbox (for new books)
                rx.cond(
                    State.book_form_mode == "add",
                    rx.box(
                        rx.hstack(
                            rx.checkbox(
                                checked=State.book_form_send_notification,
                                on_change=State.set_book_form_send_notification,
                            ),
                            rx.text(
                                "Send notification to WhatsApp group",
                                size="2",
                                color=Colors.dark_gray,
                            ),
                            spacing="2",
                            align="center",
                        ),
                        border_top=f"1px solid {Colors.gray}",
                        padding_top="3",
                    ),
                ),

                # Action buttons
                rx.hstack(
                    rx.dialog.close(
                        modern_button(
                            "Cancel",
                            variant="soft",
                            color_scheme="gray",
                            on_click=State.close_book_form,
                        ),
                    ),
                    rx.dialog.close(
                        modern_button(
                            "Save Book",
                            icon="check",
                            on_click=State.save_book,
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

        open=State.book_form_mode != "",
    )


def filters_modern() -> rx.Component:
    """Modern filters section with search and chips."""
    return rx.vstack(
        # Search input
        modern_input(
            placeholder="Search books...",
            value=State.book_search,
            on_change=State.set_book_search,
            on_key_up=lambda: State.search_books(),
            icon="search",
        ),

        # Status filters
        rx.hstack(
            filter_chip(
                "All",
                is_active=State.book_filter_status == "all",
                on_click=lambda: State.set_book_filter_status("all"),
            ),
            filter_chip(
                "Available",
                is_active=State.book_filter_status == "available",
                on_click=lambda: State.set_book_filter_status("available"),
                color_scheme="green",
            ),
            filter_chip(
                "Borrowed",
                is_active=State.book_filter_status == "borrowed",
                on_click=lambda: State.set_book_filter_status("borrowed"),
                color_scheme="orange",
            ),
            spacing="2",
            wrap="wrap",
        ),

        # Genre filter
        rx.hstack(
            rx.text(
                "Genre:",
                size="2",
                weight="bold",
                color=Colors.dark_navy,
            ),
            rx.select(
                State.genres_with_all,
                value=State.book_filter_genre,
                on_change=State.set_book_filter_genre,
                placeholder="All genres",
                size="2",
            ),
            rx.cond(
                State.book_filter_genre != "all",
                rx.icon_button(
                    rx.icon("x", size=14),
                    on_click=lambda: State.set_book_filter_genre("all"),
                    size="1",
                    variant="ghost",
                ),
            ),
            spacing="2",
            align="center",
            width="100%",
        ),

        spacing="3",
        width="100%",
    )


def books_page_modern() -> rx.Component:
    """Modern books page with gradient cards."""
    return modern_page_container(
        # Header with count and add button
        rx.hstack(
            section_header(
                title="Books",
                badge_value=State.books.length().to(str),
            ),
            rx.spacer(),
            book_form_modern(),
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

        # Filters
        filters_modern(),

        # Books list
        rx.cond(
            State.books.length() == 0,
            empty_state(
                icon="book_open",
                title="No books found",
                description="Try adjusting your filters or add a new book to get started",
                action_text="Add Book",
                on_action=State.open_add_book_form,
            ),
            rx.vstack(
                rx.foreach(State.books, book_card_modern),
                spacing="0",
                width="100%",
            ),
        ),
    )
