"""State management for PTC Library Admin Dashboard."""

import reflex as rx
from typing import List, Dict, Optional
from library_admin.services.database import DatabaseService


class State(rx.State):
    """Main application state."""

    # Current page
    current_page: str = "dashboard"

    # Authentication
    is_authenticated: bool = False
    password_input: str = ""
    auth_error: str = ""

    # Dashboard stats
    dashboard_stats: Dict = {}

    # Books
    books: List[Dict] = []
    selected_book: Optional[Dict] = None
    book_search: str = ""
    book_filter_status: str = "all"
    book_filter_genre: str = "all"
    genres: List[str] = []

    @rx.var
    def genres_with_all(self) -> List[str]:
        """Get genres list with 'all' option prepended."""
        return ["all"] + self.genres

    # Book form
    book_form_mode: str = ""  # "add" or "edit"
    book_form_id: str = ""
    book_form_title: str = ""
    book_form_author: str = ""
    book_form_genre: str = ""
    book_form_error: str = ""

    # Loans
    active_loans: List[Dict] = []

    # Users
    users: List[Dict] = []

    # Loading states
    is_loading: bool = False
    loading_message: str = ""

    # Success/Error messages
    success_message: str = ""
    error_message: str = ""

    # ===== AUTHENTICATION =====

    def set_password_input(self, value: str):
        """Set password input."""
        self.password_input = value

    def check_password(self):
        """Check admin password."""
        from library_admin.config import Config

        if self.password_input == Config.ADMIN_PASSWORD:
            self.is_authenticated = True
            self.auth_error = ""
            self.load_dashboard_data()
        else:
            self.auth_error = "Invalid password"
            self.password_input = ""

    def logout(self):
        """Logout admin."""
        self.is_authenticated = False
        self.password_input = ""
        self.auth_error = ""

    # ===== DASHBOARD =====

    def load_dashboard_data(self):
        """Load dashboard statistics."""
        self.is_loading = True
        self.loading_message = "Loading dashboard..."

        try:
            self.dashboard_stats = DatabaseService.get_dashboard_stats()
            self.error_message = ""
        except Exception as e:
            self.error_message = f"Error loading dashboard: {str(e)}"
        finally:
            self.is_loading = False
            self.loading_message = ""

    # ===== BOOKS =====

    def load_books(self):
        """Load all books with current filters."""
        self.is_loading = True
        self.loading_message = "Loading books..."

        try:
            self.books = DatabaseService.get_all_books(
                search=self.book_search,
                filter_status=self.book_filter_status,
                filter_genre=self.book_filter_genre
            )
            self.error_message = ""
        except Exception as e:
            self.error_message = f"Error loading books: {str(e)}"
        finally:
            self.is_loading = False
            self.loading_message = ""

    def load_genres(self):
        """Load all genres."""
        try:
            self.genres = DatabaseService.get_all_genres()
        except Exception as e:
            print(f"Error loading genres: {e}")

    def set_book_search(self, value: str):
        """Set book search filter."""
        self.book_search = value

    def set_book_filter_status(self, value: str):
        """Set book status filter."""
        self.book_filter_status = value
        self.load_books()

    def set_book_filter_genre(self, value: str):
        """Set book genre filter."""
        self.book_filter_genre = value
        self.load_books()

    def search_books(self):
        """Search books."""
        self.load_books()

    def clear_book_filters(self):
        """Clear all book filters."""
        self.book_search = ""
        self.book_filter_status = "all"
        self.book_filter_genre = "all"
        self.load_books()

    def open_add_book_form(self):
        """Open add book form."""
        self.book_form_mode = "add"
        self.book_form_id = ""
        self.book_form_title = ""
        self.book_form_author = ""
        self.book_form_genre = ""
        self.book_form_error = ""
        if not self.genres:
            self.load_genres()

    def open_edit_book_form(self, book_id: str):
        """Open edit book form."""
        book = DatabaseService.get_book_by_id(book_id)
        if book:
            self.book_form_mode = "edit"
            self.book_form_id = book['book_id']
            self.book_form_title = book['title']
            self.book_form_author = book['author']
            self.book_form_genre = book['genre']
            self.book_form_error = ""
            if not self.genres:
                self.load_genres()

    def close_book_form(self):
        """Close book form."""
        self.book_form_mode = ""
        self.book_form_id = ""
        self.book_form_title = ""
        self.book_form_author = ""
        self.book_form_genre = ""
        self.book_form_error = ""

    def set_book_form_id(self, value: str):
        """Set book form ID."""
        self.book_form_id = value

    def set_book_form_title(self, value: str):
        """Set book form title."""
        self.book_form_title = value

    def set_book_form_author(self, value: str):
        """Set book form author."""
        self.book_form_author = value

    def set_book_form_genre(self, value: str):
        """Set book form genre."""
        self.book_form_genre = value

    def save_book(self):
        """Save book (add or update)."""
        # Validation
        if not self.book_form_id or not self.book_form_title or not self.book_form_author or not self.book_form_genre:
            self.book_form_error = "All fields are required"
            return

        self.is_loading = True
        self.loading_message = "Saving book..."

        try:
            if self.book_form_mode == "add":
                success = DatabaseService.add_book(
                    self.book_form_id,
                    self.book_form_title,
                    self.book_form_author,
                    self.book_form_genre
                )
                message = "Book added successfully"
            else:  # edit
                success = DatabaseService.update_book(
                    self.book_form_id,
                    self.book_form_title,
                    self.book_form_author,
                    self.book_form_genre
                )
                message = "Book updated successfully"

            if success:
                self.success_message = message
                self.close_book_form()
                self.load_books()
            else:
                self.book_form_error = "Failed to save book. Book ID may already exist."

        except Exception as e:
            self.book_form_error = f"Error: {str(e)}"
        finally:
            self.is_loading = False
            self.loading_message = ""

    def delete_book_confirm(self, book_id: str):
        """Delete a book."""
        self.is_loading = True
        self.loading_message = "Deleting book..."

        try:
            success = DatabaseService.delete_book(book_id)
            if success:
                self.success_message = "Book deleted successfully"
                self.load_books()
                self.load_dashboard_data()
            else:
                self.error_message = "Cannot delete book. It may be currently borrowed."
        except Exception as e:
            self.error_message = f"Error deleting book: {str(e)}"
        finally:
            self.is_loading = False
            self.loading_message = ""

    # ===== LOANS =====

    def load_active_loans(self):
        """Load all active loans."""
        self.is_loading = True
        self.loading_message = "Loading loans..."

        try:
            self.active_loans = DatabaseService.get_active_loans()
            self.error_message = ""
        except Exception as e:
            self.error_message = f"Error loading loans: {str(e)}"
        finally:
            self.is_loading = False
            self.loading_message = ""

    # ===== USERS =====

    def load_users(self):
        """Load all users."""
        self.is_loading = True
        self.loading_message = "Loading users..."

        try:
            self.users = DatabaseService.get_all_users()
            self.error_message = ""
        except Exception as e:
            self.error_message = f"Error loading users: {str(e)}"
        finally:
            self.is_loading = False
            self.loading_message = ""

    # ===== MESSAGES =====

    def clear_messages(self):
        """Clear success/error messages."""
        self.success_message = ""
        self.error_message = ""
