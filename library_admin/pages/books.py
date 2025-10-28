"""Books management page for PTC Library Admin."""

import reflex as rx
from library_admin.state import State
from typing import Dict


def book_card(book: Dict) -> rx.Component:
    """Create a book card for mobile view."""
    status_color = rx.cond(
        book["status"] == "available",
        "green",
        "orange"
    )

    return rx.card(
        rx.vstack(
            # Book ID and Status
            rx.hstack(
                rx.badge(book["book_id"], variant="soft"),
                rx.spacer(),
                rx.badge(
                    book["status"],
                    color_scheme=status_color,
                ),
                width="100%",
            ),

            # Title
            rx.heading(book["title"], size="4"),

            # Author and Genre
            rx.text(
                f"by {book['author']}",
                size="2",
                color="gray",
            ),
            rx.badge(book["genre"], variant="outline", size="1"),

            # Loan info (if borrowed)
            rx.cond(
                book["status"] == "borrowed",
                rx.box(
                    rx.text(
                        f"Borrowed by: {book.get('loaned_to', 'Unknown')}",
                        size="1",
                        color="gray",
                    ),
                    rx.text(
                        f"Since: {book.get('loaned_date', 'Unknown')}",
                        size="1",
                        color="gray",
                    ),
                    margin_top="2",
                ),
            ),

            # Action buttons
            rx.hstack(
                rx.button(
                    rx.icon("pencil", size=16),
                    "Edit",
                    on_click=lambda: State.open_edit_book_form(book["book_id"]),
                    size="2",
                    variant="soft",
                ),
                rx.button(
                    rx.icon("trash_2", size=16),
                    "Delete",
                    on_click=lambda: State.delete_book_confirm(book["book_id"]),
                    size="2",
                    color_scheme="red",
                    variant="soft",
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


def book_form_dialog() -> rx.Component:
    """Book add/edit form dialog."""
    form_title = rx.cond(
        State.book_form_mode == "add",
        "Add New Book",
        "Edit Book"
    )

    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=18),
                "Add Book",
                on_click=State.open_add_book_form,
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(form_title),
            rx.dialog.description(
                "Fill in the book details below.",
                size="2",
            ),

            rx.vstack(
                # Error message
                rx.cond(
                    State.book_form_error != "",
                    rx.callout(
                        State.book_form_error,
                        icon="circle-alert",
                        color_scheme="red",
                        role="alert",
                    ),
                ),

                # Book ID
                rx.text("Book ID", size="2", weight="bold"),
                rx.input(
                    placeholder="e.g., BOOK001",
                    value=State.book_form_id,
                    on_change=State.set_book_form_id,
                    disabled=State.book_form_mode == "edit",
                ),

                # Title
                rx.text("Title", size="2", weight="bold"),
                rx.input(
                    placeholder="Book title",
                    value=State.book_form_title,
                    on_change=State.set_book_form_title,
                ),

                # Author
                rx.text("Author", size="2", weight="bold"),
                rx.input(
                    placeholder="Author name",
                    value=State.book_form_author,
                    on_change=State.set_book_form_author,
                ),

                # Genre
                rx.text("Genre", size="2", weight="bold"),
                rx.select(
                    State.genres,
                    placeholder="Select genre",
                    value=State.book_form_genre,
                    on_change=State.set_book_form_genre,
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
                        on_click=State.close_book_form,
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        "Save",
                        on_click=State.save_book,
                    ),
                ),
                spacing="3",
                margin_top="4",
                justify="end",
            ),
        ),
        open=State.book_form_mode != "",
    )


def books_filters() -> rx.Component:
    """Books search and filter controls."""
    return rx.vstack(
        # Search bar
        rx.hstack(
            rx.input(
                placeholder="Search by title or author...",
                value=State.book_search,
                on_change=State.set_book_search,
                width="100%",
            ),
            rx.button(
                rx.icon("search", size=18),
                on_click=State.search_books,
                size="3",
            ),
            width="100%",
        ),

        # Filters
        rx.hstack(
            rx.select(
                ["all", "available", "borrowed"],
                placeholder="Status",
                value=State.book_filter_status,
                on_change=State.set_book_filter_status,
                width="100%",
            ),
            rx.select(
                State.genres_with_all,
                placeholder="Genre",
                value=State.book_filter_genre,
                on_change=State.set_book_filter_genre,
                width="100%",
            ),
            rx.button(
                rx.icon("x", size=18),
                "Clear",
                on_click=State.clear_book_filters,
                variant="soft",
                color_scheme="gray",
            ),
            width="100%",
            spacing="2",
        ),

        spacing="3",
        width="100%",
    )


def books_list() -> rx.Component:
    """Books list with cards."""
    return rx.box(
        rx.cond(
            State.books.length() == 0,
            rx.callout(
                "No books found. Try adjusting your filters or add a new book.",
                icon="info",
                color_scheme="blue",
            ),
            rx.vstack(
                rx.foreach(State.books, book_card),
                spacing="3",
                width="100%",
            ),
        ),
        width="100%",
    )


def books_page() -> rx.Component:
    """Main books management page."""
    return rx.container(
        rx.vstack(
            # Header with Add button
            rx.hstack(
                rx.heading("Books", size="8"),
                rx.spacer(),
                book_form_dialog(),
                width="100%",
                align="center",
            ),

            # Success message
            rx.cond(
                State.success_message != "",
                rx.callout(
                    State.success_message,
                    icon="circle-check",
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
                    icon="circle-alert",
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
            books_filters(),

            # Books list
            books_list(),

            spacing="4",
            width="100%",
            padding="4",
        ),
        max_width="800px",
    )
