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
    book_form_original_id: str = ""  # Store original ID for updates
    book_form_title: str = ""
    book_form_author: str = ""
    book_form_genre: str = ""
    book_form_error: str = ""

    # Loans
    active_loans: List[Dict] = []
    loan_search: str = ""
    loan_filter_status: str = "all"

    # Users
    users: List[Dict] = []
    user_search: str = ""
    user_form_mode: str = ""
    user_form_id: str = ""
    user_form_name: str = ""
    user_form_role: str = ""
    user_form_error: str = ""

    # Genres
    genres_list: List[Dict] = []
    genre_form_mode: str = ""  # "add" or "edit"
    genre_form_id: int = 0
    genre_form_name: str = ""
    genre_form_description: str = ""
    genre_form_error: str = ""

    # Notifications
    notify_selected_user: str = ""
    notify_phone_number: str = ""
    notify_message: str = ""
    notify_group_id: str = ""
    notify_group_message: str = ""
    evolution_api_status: str = ""  # "connected", "disconnected", "testing"
    evolution_api_error: str = ""

    @rx.var
    def user_select_options(self) -> list[str]:
        """Get formatted user options for select dropdown."""
        return [f"{u.get('name', 'Unknown')} ({u.get('user_id', '')})" for u in self.users]

    # Settings
    setting_whatsapp_group_id: str = ""
    setting_loan_due_days: str = "14"
    setting_reminder_days_before: str = "2"
    setting_overdue_alert_days_after: str = "1"

    # Message Templates
    templates: List[Dict] = []
    template_form_mode: str = ""  # "add" or "edit"
    template_form_id: int = 0
    template_form_name: str = ""
    template_form_type: str = ""
    template_form_content: str = ""
    template_form_description: str = ""
    template_form_error: str = ""

    # Targeted notifications
    overdue_users_count: int = 0
    due_soon_users_count: int = 0

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
            self.book_form_original_id = book['book_id']  # Store original ID
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
        self.book_form_original_id = ""
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
                # Pass new_book_id only if it changed
                new_id = self.book_form_id if self.book_form_id != self.book_form_original_id else None
                success = DatabaseService.update_book(
                    self.book_form_original_id,  # Use original ID to find the book
                    self.book_form_title,
                    self.book_form_author,
                    self.book_form_genre,
                    new_book_id=new_id
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
        """Load all active loans with filters."""
        self.is_loading = True
        self.loading_message = "Loading loans..."

        try:
            # Get all loans first
            all_loans = DatabaseService.get_active_loans()

            # Apply search filter
            if self.loan_search:
                search_lower = self.loan_search.lower()
                all_loans = [
                    loan for loan in all_loans
                    if search_lower in loan.get('title', '').lower()
                    or search_lower in loan.get('author', '').lower()
                    or search_lower in loan.get('book_id', '').lower()
                    or search_lower in loan.get('user_id', '').lower()
                ]

            # Apply status filter
            if self.loan_filter_status != "all":
                all_loans = [
                    loan for loan in all_loans
                    if loan.get('status') == self.loan_filter_status
                ]

            self.active_loans = all_loans
            self.error_message = ""
        except Exception as e:
            self.error_message = f"Error loading loans: {str(e)}"
        finally:
            self.is_loading = False
            self.loading_message = ""

    def set_loan_search(self, value: str):
        """Set loan search filter."""
        self.loan_search = value

    def set_loan_filter_status(self, value: str):
        """Set loan status filter."""
        self.loan_filter_status = value
        self.load_active_loans()

    def search_loans(self):
        """Search loans."""
        self.load_active_loans()

    def clear_loan_filters(self):
        """Clear all loan filters."""
        self.loan_search = ""
        self.loan_filter_status = "all"
        self.load_active_loans()

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

    def set_user_search(self, value: str):
        """Set user search."""
        self.user_search = value

    def search_users(self):
        """Search users."""
        if self.user_search:
            search_lower = self.user_search.lower()
            all_users = DatabaseService.get_all_users()
            self.users = [
                u for u in all_users
                if search_lower in u.get('name', '').lower()
                or search_lower in u.get('user_id', '').lower()
            ]
        else:
            self.load_users()

    def open_edit_user_form(self, user_id: str):
        """Open edit user form."""
        users_list = [u for u in self.users if u['user_id'] == user_id]
        if users_list:
            user = users_list[0]
            self.user_form_mode = "edit"
            self.user_form_id = user['user_id']
            self.user_form_name = user.get('name', '')
            self.user_form_role = user.get('role', 'user')
            self.user_form_error = ""

    def set_user_form_name(self, value: str):
        """Set user form name."""
        self.user_form_name = value

    def set_user_form_role(self, value: str):
        """Set user form role."""
        self.user_form_role = value

    def close_user_form(self):
        """Close user form."""
        self.user_form_mode = ""
        self.user_form_error = ""

    def save_user(self):
        """Save user."""
        if not self.user_form_name:
            self.user_form_error = "Name is required"
            return

        self.is_loading = True
        try:
            success = DatabaseService.update_user(
                self.user_form_id,
                self.user_form_name,
                self.user_form_role
            )

            if success:
                self.success_message = "User updated successfully"
                self.close_user_form()
                self.load_users()
            else:
                self.user_form_error = "Failed to update user"
        except Exception as e:
            self.user_form_error = f"Error: {str(e)}"
        finally:
            self.is_loading = False

    # ===== GENRES =====

    def load_genres_list(self):
        """Load all genres with book counts."""
        self.is_loading = True
        self.loading_message = "Loading genres..."

        try:
            self.genres_list = DatabaseService.get_genres_with_counts()
            self.error_message = ""
        except Exception as e:
            self.error_message = f"Error loading genres: {str(e)}"
        finally:
            self.is_loading = False
            self.loading_message = ""

    def open_add_genre_form(self):
        """Open add genre form."""
        self.genre_form_mode = "add"
        self.genre_form_id = 0
        self.genre_form_name = ""
        self.genre_form_description = ""
        self.genre_form_error = ""

    def open_edit_genre_form(self, genre_id: int):
        """Open edit genre form."""
        # Find the genre in the list
        for genre in self.genres_list:
            if genre['genre_id'] == genre_id:
                self.genre_form_mode = "edit"
                self.genre_form_id = genre_id
                self.genre_form_name = genre['genre_name']
                self.genre_form_description = genre.get('description', '')
                self.genre_form_error = ""
                break

    def close_genre_form(self):
        """Close genre form."""
        self.genre_form_mode = ""
        self.genre_form_id = 0
        self.genre_form_name = ""
        self.genre_form_description = ""
        self.genre_form_error = ""

    def set_genre_form_name(self, value: str):
        """Set genre form name."""
        self.genre_form_name = value

    def set_genre_form_description(self, value: str):
        """Set genre form description."""
        self.genre_form_description = value

    def save_genre(self):
        """Save genre (add or update)."""
        if not self.genre_form_name:
            self.genre_form_error = "Genre name is required"
            return

        self.is_loading = True
        self.loading_message = "Saving genre..."

        try:
            if self.genre_form_mode == "add":
                success = DatabaseService.add_genre(
                    self.genre_form_name,
                    self.genre_form_description
                )
                message = "Genre added successfully"
            else:  # edit
                success = DatabaseService.update_genre(
                    self.genre_form_id,
                    self.genre_form_name,
                    self.genre_form_description
                )
                message = "Genre updated successfully"

            if success:
                self.success_message = message
                self.close_genre_form()
                self.load_genres_list()
                self.load_genres()  # Refresh genres dropdown
            else:
                self.genre_form_error = "Failed to save genre. Genre name may already exist."

        except Exception as e:
            self.genre_form_error = f"Error: {str(e)}"
        finally:
            self.is_loading = False
            self.loading_message = ""

    def delete_genre_confirm(self, genre_id: int):
        """Delete a genre."""
        self.is_loading = True
        self.loading_message = "Deleting genre..."

        try:
            success = DatabaseService.delete_genre(genre_id)
            if success:
                self.success_message = "Genre deleted successfully"
                self.load_genres_list()
                self.load_genres()  # Refresh genres dropdown
            else:
                self.error_message = "Cannot delete genre. It may be used by books."
        except Exception as e:
            self.error_message = f"Error deleting genre: {str(e)}"
        finally:
            self.is_loading = False
            self.loading_message = ""

    # ===== NOTIFICATIONS =====

    def set_notify_selected_user(self, value: str):
        """Set selected user for notification."""
        self.notify_selected_user = value
        # Extract phone number from selection (format: "Name (phone)")
        if "(" in value and ")" in value:
            self.notify_phone_number = value.split("(")[1].split(")")[0]

    def set_notify_phone_number(self, value: str):
        """Set phone number for notification."""
        self.notify_phone_number = value

    def set_notify_message(self, value: str):
        """Set notification message."""
        self.notify_message = value

    def set_notify_group_id(self, value: str):
        """Set group ID for broadcast."""
        self.notify_group_id = value

    def set_notify_group_message(self, value: str):
        """Set group broadcast message."""
        self.notify_group_message = value

    def use_due_reminder_template(self):
        """Use due reminder template."""
        self.notify_message = """📚 PTC Library Reminder

Your borrowed book is due soon:

📖 [Book Title]
📅 Due: [Due Date]

Please return it by the due date or renew if needed.

Thank you! 🙏"""

    def use_overdue_alert_template(self):
        """Use overdue alert template."""
        self.notify_message = """⚠️ PTC Library - Overdue Book

Your borrowed book is overdue:

📖 [Book Title]

Please return it as soon as possible so others can borrow it.

Thank you for your understanding! 🙏"""

    def use_new_book_template(self):
        """Use new book announcement template."""
        self.notify_group_message = """📚 New Book Alert!

We've just added a new book to the PTC Library:

📖 [Book Title]
✍️ by [Author]
🏷️ Genre: [Genre]

Come and borrow it today! 📚✨"""

    def use_custom_template(self):
        """Clear message for custom content."""
        self.notify_message = ""
        self.notify_group_message = ""

    def send_notification_to_user(self):
        """Send notification to a user."""
        from library_admin.services.notifications import NotificationService

        if not self.notify_phone_number:
            self.error_message = "Please select a user or enter a phone number"
            return

        if not self.notify_message:
            self.error_message = "Please enter a message"
            return

        self.is_loading = True
        self.loading_message = "Sending message..."

        try:
            result = NotificationService.send_whatsapp_message(
                self.notify_phone_number,
                self.notify_message
            )

            if result.get("success"):
                self.success_message = result.get("message", "Message sent successfully")
                self.notify_message = ""
                self.notify_phone_number = ""
                self.notify_selected_user = ""
            else:
                self.error_message = result.get("error", "Failed to send message")

        except Exception as e:
            self.error_message = f"Error: {str(e)}"
        finally:
            self.is_loading = False
            self.loading_message = ""

    def send_notification_to_group(self):
        """Send broadcast notification to group."""
        from library_admin.services.notifications import NotificationService

        if not self.notify_group_id:
            self.error_message = "Please enter a group ID"
            return

        if not self.notify_group_message:
            self.error_message = "Please enter a message"
            return

        self.is_loading = True
        self.loading_message = "Sending broadcast..."

        try:
            result = NotificationService.send_group_message(
                self.notify_group_id,
                self.notify_group_message
            )

            if result.get("success"):
                self.success_message = result.get("message", "Broadcast sent successfully")
                self.notify_group_message = ""
            else:
                self.error_message = result.get("error", "Failed to send broadcast")

        except Exception as e:
            self.error_message = f"Error: {str(e)}"
        finally:
            self.is_loading = False
            self.loading_message = ""

    def test_evolution_api(self):
        """Test Evolution API connection."""
        from library_admin.services.notifications import NotificationService

        self.evolution_api_status = "testing"
        self.evolution_api_error = ""

        try:
            result = NotificationService.test_connection()

            if result.get("success"):
                self.evolution_api_status = "connected"
                self.success_message = "Evolution API connection successful"
            else:
                self.evolution_api_status = "disconnected"
                self.evolution_api_error = result.get("error", "Connection failed")

        except Exception as e:
            self.evolution_api_status = "disconnected"
            self.evolution_api_error = f"Error: {str(e)}"

    # ===== SETTINGS =====

    def load_settings(self):
        """Load all settings."""
        self.is_loading = True
        try:
            settings = DatabaseService.get_all_settings()
            for setting in settings:
                key = setting['setting_key']
                value = setting['setting_value']
                if key == 'whatsapp_group_id':
                    self.setting_whatsapp_group_id = value
                elif key == 'loan_due_days':
                    self.setting_loan_due_days = value
                elif key == 'reminder_days_before':
                    self.setting_reminder_days_before = value
                elif key == 'overdue_alert_days_after':
                    self.setting_overdue_alert_days_after = value

            # Load counts for targeted notifications
            overdue_users = DatabaseService.get_users_with_overdue_books()
            self.overdue_users_count = len(overdue_users)

            due_soon_users = DatabaseService.get_users_with_due_soon_books()
            self.due_soon_users_count = len(due_soon_users)

            self.error_message = ""
        except Exception as e:
            self.error_message = f"Error loading settings: {str(e)}"
        finally:
            self.is_loading = False

    def set_setting_whatsapp_group_id(self, value: str):
        """Set WhatsApp group ID."""
        self.setting_whatsapp_group_id = value

    def set_setting_loan_due_days(self, value: str):
        """Set loan due days."""
        self.setting_loan_due_days = value

    def set_setting_reminder_days_before(self, value: str):
        """Set reminder days before."""
        self.setting_reminder_days_before = value

    def set_setting_overdue_alert_days_after(self, value: str):
        """Set overdue alert days after."""
        self.setting_overdue_alert_days_after = value

    def save_settings(self):
        """Save all settings."""
        self.is_loading = True
        try:
            DatabaseService.update_setting('whatsapp_group_id', self.setting_whatsapp_group_id)
            DatabaseService.update_setting('loan_due_days', self.setting_loan_due_days)
            DatabaseService.update_setting('reminder_days_before', self.setting_reminder_days_before)
            DatabaseService.update_setting('overdue_alert_days_after', self.setting_overdue_alert_days_after)

            self.success_message = "Settings saved successfully"
            self.error_message = ""
        except Exception as e:
            self.error_message = f"Error saving settings: {str(e)}"
        finally:
            self.is_loading = False

    # ===== MESSAGE TEMPLATES =====

    def load_templates(self):
        """Load all message templates."""
        self.is_loading = True
        try:
            self.templates = DatabaseService.get_all_templates()
            self.error_message = ""
        except Exception as e:
            self.error_message = f"Error loading templates: {str(e)}"
        finally:
            self.is_loading = False

    def open_add_template_form(self):
        """Open add template form."""
        self.template_form_mode = "add"
        self.template_form_id = 0
        self.template_form_name = ""
        self.template_form_type = ""
        self.template_form_content = ""
        self.template_form_description = ""
        self.template_form_error = ""

    def open_edit_template_form(self, template_id: int):
        """Open edit template form."""
        for template in self.templates:
            if template['template_id'] == template_id:
                self.template_form_mode = "edit"
                self.template_form_id = template_id
                self.template_form_name = template['template_name']
                self.template_form_type = template['template_type']
                self.template_form_content = template['message_content']
                self.template_form_description = template.get('description', '')
                self.template_form_error = ""
                break

    def close_template_form(self):
        """Close template form."""
        self.template_form_mode = ""
        self.template_form_error = ""

    def set_template_form_name(self, value: str):
        """Set template form name."""
        self.template_form_name = value

    def set_template_form_type(self, value: str):
        """Set template form type."""
        self.template_form_type = value

    def set_template_form_content(self, value: str):
        """Set template form content."""
        self.template_form_content = value

    def set_template_form_description(self, value: str):
        """Set template form description."""
        self.template_form_description = value

    def save_template(self):
        """Save message template."""
        if not self.template_form_name or not self.template_form_type or not self.template_form_content:
            self.template_form_error = "Name, type, and content are required"
            return

        self.is_loading = True
        try:
            if self.template_form_mode == "add":
                success = DatabaseService.add_template(
                    self.template_form_name,
                    self.template_form_type,
                    self.template_form_content,
                    self.template_form_description
                )
                message = "Template added successfully"
            else:  # edit
                success = DatabaseService.update_template(
                    self.template_form_id,
                    self.template_form_name,
                    self.template_form_type,
                    self.template_form_content,
                    self.template_form_description
                )
                message = "Template updated successfully"

            if success:
                self.success_message = message
                self.close_template_form()
                self.load_templates()
            else:
                self.template_form_error = "Failed to save template"

        except Exception as e:
            self.template_form_error = f"Error: {str(e)}"
        finally:
            self.is_loading = False

    # ===== TARGETED NOTIFICATIONS =====

    def send_overdue_alerts_bulk(self):
        """Send alerts to all users with overdue books."""
        from library_admin.services.notifications import NotificationService

        self.is_loading = True
        self.loading_message = "Sending overdue alerts..."

        try:
            overdue_users = DatabaseService.get_users_with_overdue_books()

            if not overdue_users:
                self.error_message = "No users with overdue books found"
                return

            # Get template
            template = DatabaseService.get_template_by_name('overdue_alert')
            if not template:
                self.error_message = "Overdue alert template not found"
                return

            success_count = 0
            for user in overdue_users:
                user_id = user['user_id']
                overdue_count = user['overdue_count']

                # Get user's overdue loans
                loans = DatabaseService.get_active_loans()
                user_loans = [l for l in loans if l['user_id'] == user_id and l['status'] == 'overdue']

                if user_loans:
                    first_book = user_loans[0]
                    message = template['message_content'].format(
                        book_title=first_book['title'],
                        days_overdue=abs(first_book['days_remaining'])
                    )

                    result = NotificationService.send_whatsapp_message(user_id, message)
                    if result.get('success'):
                        success_count += 1

            self.success_message = f"Sent alerts to {success_count} of {len(overdue_users)} users"
            self.load_settings()  # Reload counts

        except Exception as e:
            self.error_message = f"Error sending alerts: {str(e)}"
        finally:
            self.is_loading = False
            self.loading_message = ""

    def send_due_soon_reminders_bulk(self):
        """Send reminders to all users with books due soon."""
        from library_admin.services.notifications import NotificationService

        self.is_loading = True
        self.loading_message = "Sending due soon reminders..."

        try:
            due_soon_users = DatabaseService.get_users_with_due_soon_books()

            if not due_soon_users:
                self.error_message = "No users with books due soon found"
                return

            # Get template
            template = DatabaseService.get_template_by_name('due_reminder')
            if not template:
                self.error_message = "Due reminder template not found"
                return

            success_count = 0
            for user in due_soon_users:
                user_id = user['user_id']

                # Get user's due soon loans
                loans = DatabaseService.get_active_loans()
                user_loans = [l for l in loans if l['user_id'] == user_id and l['status'] == 'due_soon']

                if user_loans:
                    first_book = user_loans[0]
                    message = template['message_content'].format(
                        book_title=first_book['title'],
                        due_date=first_book['due_date']
                    )

                    result = NotificationService.send_whatsapp_message(user_id, message)
                    if result.get('success'):
                        success_count += 1

            self.success_message = f"Sent reminders to {success_count} of {len(due_soon_users)} users"
            self.load_settings()  # Reload counts

        except Exception as e:
            self.error_message = f"Error sending reminders: {str(e)}"
        finally:
            self.is_loading = False
            self.loading_message = ""

    def send_notification_to_loan_user(self, user_id: str, book_title: str, loan_status: str):
        """Send notification to a specific user about their loan."""
        from library_admin.services.notifications import NotificationService

        self.is_loading = True
        self.loading_message = "Sending notification..."

        try:
            # Get appropriate template
            template_name = 'overdue_alert' if loan_status == 'overdue' else 'due_reminder'
            template = DatabaseService.get_template_by_name(template_name)

            if not template:
                self.error_message = f"Template '{template_name}' not found"
                return

            # Get loan details
            loans = DatabaseService.get_active_loans()
            user_loans = [l for l in loans if l['user_id'] == user_id and l['title'] == book_title]

            if not user_loans:
                self.error_message = "Loan not found"
                return

            loan = user_loans[0]

            # Format message
            if loan_status == 'overdue':
                message = template['message_content'].format(
                    book_title=loan['title'],
                    days_overdue=abs(loan['days_remaining'])
                )
            else:
                message = template['message_content'].format(
                    book_title=loan['title'],
                    due_date=loan['due_date']
                )

            # Send notification
            result = NotificationService.send_whatsapp_message(user_id, message)

            if result.get('success'):
                self.success_message = f"Notification sent to {user_id}"
            else:
                self.error_message = result.get('error', 'Failed to send notification')

        except Exception as e:
            self.error_message = f"Error sending notification: {str(e)}"
        finally:
            self.is_loading = False
            self.loading_message = ""

    # ===== MESSAGES =====

    def clear_messages(self):
        """Clear success/error messages."""
        self.success_message = ""
        self.error_message = ""
