"""Compact Books management page - Professional Mobile Design."""

import reflex as rx
from library_admin.state import State
from typing import Dict


def book_row(book: Dict) -> rx.Component:
    """Compact book row."""
    status_color = rx.cond(book["status"] == "available", "green", "orange")

    return rx.box(
        rx.hstack(
            # Book info (main area)
            rx.vstack(
                # Title + Status
                rx.hstack(
                    rx.text(book["title"], weight="bold", size="2"),
                    rx.spacer(),
                    rx.badge(
                        book["status"],
                        color_scheme=status_color,
                        size="1",
                    ),
                    width="100%",
                    align="center",
                ),

                # Author + Genre + ID
                rx.hstack(
                    rx.text(book["author"], size="1", color="gray"),
                    rx.text("•", size="1", color="gray"),
                    rx.text(book["genre"], size="1", color="gray"),
                    rx.text("•", size="1", color="gray"),
                    rx.text(book["book_id"], size="1", color="gray", font_family="mono"),
                    spacing="1",
                ),

                # Borrowed info (if applicable)
                rx.cond(
                    book["status"] == "borrowed",
                    rx.text(
                        f"→ {book.get('loaned_to', 'Unknown')}",
                        size="1",
                        color="orange",
                    ),
                ),

                spacing="1",
                flex="1",
            ),

            # Actions (right edge)
            rx.hstack(
                rx.icon(
                    "edit",
                    size=16,
                    on_click=lambda: State.open_edit_book_form(book["book_id"]),
                    cursor="pointer",
                    color=rx.color("blue", 11),
                ),
                rx.icon(
                    "trash-2",
                    size=16,
                    on_click=lambda: State.delete_book_confirm(book["book_id"]),
                    cursor="pointer",
                    color=rx.color("red", 9),
                ),
                spacing="3",
            ),

            spacing="2",
            width="100%",
            align="start",
        ),
        padding="3",
        border_bottom=f"1px solid {rx.color('gray', 4)}",
        _hover={"background_color": rx.color("gray", 2)},
    )


def book_form_compact() -> rx.Component:
    """Compact book add/edit form."""
    form_title = rx.cond(State.book_form_mode == "add", "Add Book", "Edit Book")

    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(rx.icon("plus", size=16), "Add", size="2", on_click=State.open_add_book_form),
        ),
        rx.dialog.content(
            rx.dialog.title(form_title, size="5"),

            rx.vstack(
                rx.cond(
                    State.book_form_error != "",
                    rx.callout(State.book_form_error, icon="circle-alert", color_scheme="red", size="1"),
                ),

                # Compact form fields
                rx.vstack(
                    rx.hstack(
                        rx.text("ID", size="1", weight="bold", width="60px"),
                        rx.input(
                            value=State.book_form_id,
                            on_change=State.set_book_form_id,
                            size="2",
                            placeholder="BOOK001",
                        ),
                        width="100%",
                        align="center",
                    ),

                    rx.hstack(
                        rx.text("Title", size="1", weight="bold", width="60px"),
                        rx.input(
                            value=State.book_form_title,
                            on_change=State.set_book_form_title,
                            size="2",
                            placeholder="Book title",
                        ),
                        width="100%",
                        align="center",
                    ),

                    rx.hstack(
                        rx.text("Author", size="1", weight="bold", width="60px"),
                        rx.input(
                            value=State.book_form_author,
                            on_change=State.set_book_form_author,
                            size="2",
                            placeholder="Author name",
                        ),
                        width="100%",
                        align="center",
                    ),

                    rx.hstack(
                        rx.text("Genre", size="1", weight="bold", width="60px"),
                        rx.select(
                            State.genres,
                            value=State.book_form_genre,
                            on_change=State.set_book_form_genre,
                            size="2",
                            placeholder="Select...",
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
                        rx.button("Cancel", variant="soft", size="2", on_click=State.close_book_form),
                    ),
                    rx.dialog.close(
                        rx.button("Save", size="2", on_click=State.save_book),
                    ),
                    spacing="2",
                    justify="end",
                    width="100%",
                ),

                spacing="3",
                width="100%",
            ),
        ),
        open=State.book_form_mode != "",
    )


def compact_filters() -> rx.Component:
    """Compact filter chips."""
    return rx.vstack(
        rx.input(
            placeholder="Search books...",
            value=State.book_search,
            on_change=State.set_book_search,
            on_key_up=lambda: State.search_books(),
            size="2",
        ),

        rx.hstack(
            # Status filter
            rx.badge("All", variant="solid" if State.book_filter_status == "all" else "soft",
                    on_click=lambda: State.set_book_filter_status("all"), cursor="pointer", size="1"),
            rx.badge("Available", variant="solid" if State.book_filter_status == "available" else "soft", color_scheme="green",
                    on_click=lambda: State.set_book_filter_status("available"), cursor="pointer", size="1"),
            rx.badge("Borrowed", variant="solid" if State.book_filter_status == "borrowed" else "soft", color_scheme="orange",
                    on_click=lambda: State.set_book_filter_status("borrowed"), cursor="pointer", size="1"),
            spacing="2",
        ),

        spacing="2",
        width="100%",
    )


def books_page_v2() -> rx.Component:
    """Compact professional books page."""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading("Books", size="6"),
                rx.badge(State.books.length().to(str), variant="soft"),
                rx.spacer(),
                book_form_compact(),
                width="100%",
                align="center",
            ),

            # Messages
            rx.cond(State.success_message != "", rx.callout(State.success_message, icon="circle-check", color_scheme="green", size="1", on_click=State.clear_messages)),
            rx.cond(State.error_message != "", rx.callout(State.error_message, icon="circle-alert", color_scheme="red", size="1", on_click=State.clear_messages)),

            # Filters
            compact_filters(),

            # Books list
            rx.box(
                rx.cond(
                    State.books.length() == 0,
                    rx.box(rx.text("No books found", size="2", color="gray", align="center"), padding="4"),
                    rx.foreach(State.books, book_row),
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
