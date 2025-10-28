"""Database service for PTC Library Admin Dashboard."""

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from library_admin.config import Config


class DatabaseService:
    """Service for database operations."""

    @staticmethod
    def get_connection():
        """Get database connection."""
        return psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            cursor_factory=RealDictCursor
        )

    # ===== STATISTICS =====

    @staticmethod
    def get_dashboard_stats() -> Dict[str, Any]:
        """Get dashboard statistics."""
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()

        try:
            # Total books
            cursor.execute("SELECT COUNT(*) as total FROM books")
            total_books = cursor.fetchone()['total']

            # Available books
            cursor.execute("SELECT COUNT(*) as available FROM books WHERE status = 'available'")
            available_books = cursor.fetchone()['available']

            # Borrowed books
            cursor.execute("SELECT COUNT(*) as borrowed FROM books WHERE status = 'borrowed'")
            borrowed_books = cursor.fetchone()['borrowed']

            # Active loans
            cursor.execute("SELECT COUNT(*) as active FROM loans WHERE return_date IS NULL")
            active_loans = cursor.fetchone()['active']

            # Overdue books
            cursor.execute("""
                SELECT COUNT(*) as overdue
                FROM loans
                WHERE return_date IS NULL
                  AND (borrow_date + INTERVAL '14 days') < CURRENT_DATE
            """)
            overdue_books = cursor.fetchone()['overdue']

            # Due soon (within 2 days)
            cursor.execute("""
                SELECT COUNT(*) as due_soon
                FROM loans
                WHERE return_date IS NULL
                  AND (borrow_date + INTERVAL '14 days') BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '2 days'
            """)
            due_soon = cursor.fetchone()['due_soon']

            # Total users
            cursor.execute("SELECT COUNT(*) as total FROM users")
            total_users = cursor.fetchone()['total']

            return {
                'total_books': total_books,
                'available_books': available_books,
                'borrowed_books': borrowed_books,
                'active_loans': active_loans,
                'overdue_books': overdue_books,
                'due_soon': due_soon,
                'total_users': total_users
            }
        finally:
            cursor.close()
            conn.close()

    # ===== BOOKS =====

    @staticmethod
    def get_all_books(search: str = "", filter_status: str = "all", filter_genre: str = "all") -> List[Dict]:
        """Get all books with optional filters."""
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()

        try:
            query = """
                SELECT book_id, title, author, genre, status, loaned_to, loaned_date, created_at
                FROM books
                WHERE 1=1
            """
            params = []

            # Search filter
            if search:
                query += " AND (LOWER(title) LIKE %s OR LOWER(author) LIKE %s OR LOWER(book_id) LIKE %s)"
                search_pattern = f"%{search.lower()}%"
                params.extend([search_pattern, search_pattern, search_pattern])

            # Status filter
            if filter_status != "all":
                query += " AND status = %s"
                params.append(filter_status)

            # Genre filter
            if filter_genre != "all":
                query += " AND genre = %s"
                params.append(filter_genre)

            query += " ORDER BY book_id"

            cursor.execute(query, params)
            books = cursor.fetchall()

            # Convert to list of dicts and format dates
            result = []
            for book in books:
                book_dict = dict(book)
                if book_dict.get('loaned_date'):
                    book_dict['loaned_date'] = book_dict['loaned_date'].strftime('%Y-%m-%d')
                if book_dict.get('created_at'):
                    book_dict['created_at'] = book_dict['created_at'].strftime('%Y-%m-%d')
                result.append(book_dict)

            return result
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_book_by_id(book_id: str) -> Optional[Dict]:
        """Get a single book by ID."""
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT book_id, title, author, genre, status, loaned_to, loaned_date, created_at
                FROM books
                WHERE book_id = %s
            """, (book_id,))

            book = cursor.fetchone()
            if book:
                return dict(book)
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_book(book_id: str, title: str, author: str, genre: str) -> bool:
        """Add a new book."""
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO books (book_id, title, author, genre, status)
                VALUES (%s, %s, %s, %s, 'available')
            """, (book_id, title, author, genre))

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error adding book: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_book(book_id: str, title: str, author: str, genre: str, new_book_id: str = None) -> bool:
        """Update an existing book. If new_book_id is provided, also update the book_id."""
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()

        try:
            # If changing book_id, check if new ID already exists
            if new_book_id and new_book_id != book_id:
                cursor.execute("SELECT book_id FROM books WHERE book_id = %s", (new_book_id,))
                if cursor.fetchone():
                    return False  # New book_id already exists

                # Update book_id along with other fields
                # Note: This also updates foreign key references in loans table due to ON UPDATE CASCADE
                cursor.execute("""
                    UPDATE books
                    SET book_id = %s, title = %s, author = %s, genre = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE book_id = %s
                """, (new_book_id, title, author, genre, book_id))
            else:
                # Just update title, author, genre
                cursor.execute("""
                    UPDATE books
                    SET title = %s, author = %s, genre = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE book_id = %s
                """, (title, author, genre, book_id))

            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error updating book: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_book(book_id: str) -> bool:
        """Delete a book (only if not currently borrowed)."""
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()

        try:
            # Check if book is borrowed
            cursor.execute("SELECT status FROM books WHERE book_id = %s", (book_id,))
            book = cursor.fetchone()

            if not book:
                return False

            if book['status'] == 'borrowed':
                return False  # Cannot delete borrowed book

            cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error deleting book: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    # ===== GENRES =====

    @staticmethod
    def get_all_genres() -> List[str]:
        """Get all genre names."""
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT genre_name FROM genres ORDER BY display_order, genre_name")
            genres = cursor.fetchall()
            return [g['genre_name'] for g in genres]
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_genres_with_counts() -> List[Dict]:
        """Get all genres with book counts."""
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    g.genre_id,
                    g.genre_name,
                    g.description,
                    g.display_order,
                    COUNT(b.book_id) as book_count
                FROM genres g
                LEFT JOIN books b ON g.genre_name = b.genre
                GROUP BY g.genre_id, g.genre_name, g.description, g.display_order
                ORDER BY g.display_order, g.genre_name
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_genre(genre_name: str, description: str = "") -> bool:
        """Add a new genre."""
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()

        try:
            # Get max display_order
            cursor.execute("SELECT COALESCE(MAX(display_order), 0) + 1 FROM genres")
            display_order = cursor.fetchone()['coalesce']

            cursor.execute(
                "INSERT INTO genres (genre_name, description, display_order) VALUES (%s, %s, %s)",
                (genre_name, description, display_order)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error adding genre: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_genre(genre_id: int, genre_name: str, description: str) -> bool:
        """Update genre details."""
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE genres SET genre_name = %s, description = %s WHERE genre_id = %s",
                (genre_name, description, genre_id)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error updating genre: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_genre(genre_id: int) -> bool:
        """Delete a genre (only if no books use it)."""
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()

        try:
            # Check if any books use this genre
            cursor.execute("SELECT genre_name FROM genres WHERE genre_id = %s", (genre_id,))
            genre = cursor.fetchone()
            if not genre:
                return False

            cursor.execute("SELECT COUNT(*) as count FROM books WHERE genre = %s", (genre['genre_name'],))
            count = cursor.fetchone()['count']

            if count > 0:
                return False  # Cannot delete genre with books

            cursor.execute("DELETE FROM genres WHERE genre_id = %s", (genre_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error deleting genre: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    # ===== LOANS =====

    @staticmethod
    def get_active_loans() -> List[Dict]:
        """Get all active loans with user and book info."""
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    l.loan_id,
                    l.book_id,
                    l.user_id,
                    l.borrow_date,
                    (l.borrow_date + INTERVAL '14 days') as due_date,
                    b.title,
                    b.author,
                    b.genre,
                    COALESCE(u.name, 'User ' || u.user_id) as name,
                    EXTRACT(DAY FROM ((l.borrow_date + INTERVAL '14 days') - CURRENT_DATE))::integer as days_remaining,
                    CASE
                        WHEN (l.borrow_date + INTERVAL '14 days') < CURRENT_DATE THEN 'overdue'
                        WHEN (l.borrow_date + INTERVAL '14 days') BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '2 days' THEN 'due_soon'
                        ELSE 'ok'
                    END as status
                FROM loans l
                JOIN books b ON l.book_id = b.book_id
                LEFT JOIN users u ON l.user_id = u.user_id
                WHERE l.return_date IS NULL
                ORDER BY l.borrow_date + INTERVAL '14 days'
            """)

            loans = cursor.fetchall()

            # Convert to list of dicts and format dates
            result = []
            for loan in loans:
                loan_dict = dict(loan)
                if loan_dict.get('borrow_date'):
                    loan_dict['borrow_date'] = loan_dict['borrow_date'].strftime('%Y-%m-%d')
                if loan_dict.get('due_date'):
                    loan_dict['due_date'] = loan_dict['due_date'].strftime('%Y-%m-%d')
                result.append(loan_dict)

            return result
        finally:
            cursor.close()
            conn.close()

    # ===== USERS =====

    @staticmethod
    def get_all_users() -> List[Dict]:
        """Get all users."""
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    u.user_id,
                    u.name,
                    u.role,
                    u.created_at,
                    COUNT(l.loan_id) FILTER (WHERE l.return_date IS NULL) as active_loans
                FROM users u
                LEFT JOIN loans l ON u.user_id = l.user_id
                GROUP BY u.user_id, u.name, u.role, u.created_at
                ORDER BY u.created_at DESC
            """)

            users = cursor.fetchall()

            # Convert to list of dicts
            result = []
            for user in users:
                user_dict = dict(user)
                if user_dict.get('created_at'):
                    user_dict['created_at'] = user_dict['created_at'].strftime('%Y-%m-%d')
                result.append(user_dict)

            return result
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_user(user_id: str, name: str, role: str) -> bool:
        """Update user details."""
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE users SET name = %s, role = %s WHERE user_id = %s",
                (name, role, user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error updating user: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_user_name(user_id: str, name: str) -> bool:
        """Update user's name."""
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE users
                SET name = %s
                WHERE user_id = %s
            """, (name, user_id))

            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error updating user: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
