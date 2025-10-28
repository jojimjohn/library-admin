"""WhatsApp notification service using Evolution API."""

import requests
from typing import Optional, Dict, Any
from library_admin.config import Config


class NotificationService:
    """Service for sending WhatsApp notifications via Evolution API."""

    @staticmethod
    def send_whatsapp_message(phone_number: str, message: str) -> Dict[str, Any]:
        """
        Send a WhatsApp message to a phone number.

        Args:
            phone_number: Phone number with country code (e.g., 61412345678)
            message: Message text to send

        Returns:
            Dict with 'success' (bool) and 'message' (str) or 'error' (str)
        """
        try:
            # Remove any spaces or special characters from phone number
            clean_phone = phone_number.replace(" ", "").replace("+", "").replace("-", "")

            # Evolution API endpoint for sending text messages
            url = f"{Config.EVOLUTION_API_URL}/message/sendText/{Config.EVOLUTION_INSTANCE}"

            headers = {
                "Content-Type": "application/json",
                "apikey": Config.EVOLUTION_API_KEY
            }

            payload = {
                "number": clean_phone,
                "text": message
            }

            response = requests.post(url, json=payload, headers=headers, timeout=10)

            if response.status_code == 200 or response.status_code == 201:
                return {
                    "success": True,
                    "message": f"Message sent successfully to {phone_number}",
                    "response": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to send message. Status: {response.status_code}",
                    "response": response.text
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timeout. Please check your Evolution API connection."
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Connection error. Please check if Evolution API is running."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error sending message: {str(e)}"
            }

    @staticmethod
    def send_group_message(group_id: str, message: str) -> Dict[str, Any]:
        """
        Send a WhatsApp message to a group.

        Args:
            group_id: WhatsApp group ID
            message: Message text to send

        Returns:
            Dict with 'success' (bool) and 'message' (str) or 'error' (str)
        """
        try:
            url = f"{Config.EVOLUTION_API_URL}/message/sendText/{Config.EVOLUTION_INSTANCE}"

            headers = {
                "Content-Type": "application/json",
                "apikey": Config.EVOLUTION_API_KEY
            }

            payload = {
                "number": group_id,
                "text": message
            }

            response = requests.post(url, json=payload, headers=headers, timeout=10)

            if response.status_code == 200 or response.status_code == 201:
                return {
                    "success": True,
                    "message": "Message sent successfully to group",
                    "response": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to send message. Status: {response.status_code}",
                    "response": response.text
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error sending group message: {str(e)}"
            }

    @staticmethod
    def send_due_reminder(user_id: str, book_title: str, due_date: str) -> Dict[str, Any]:
        """
        Send a reminder about a book due soon.

        Args:
            user_id: User's phone number
            book_title: Title of the book
            due_date: Due date string

        Returns:
            Result from send_whatsapp_message
        """
        message = f"""📚 PTC Library Reminder

Your borrowed book is due soon:

📖 {book_title}
📅 Due: {due_date}

Please return it by the due date or renew if needed.

Thank you! 🙏"""

        return NotificationService.send_whatsapp_message(user_id, message)

    @staticmethod
    def send_overdue_alert(user_id: str, book_title: str, days_overdue: int) -> Dict[str, Any]:
        """
        Send an alert about an overdue book.

        Args:
            user_id: User's phone number
            book_title: Title of the book
            days_overdue: Number of days overdue

        Returns:
            Result from send_whatsapp_message
        """
        message = f"""⚠️ PTC Library - Overdue Book

Your borrowed book is {days_overdue} days overdue:

📖 {book_title}

Please return it as soon as possible so others can borrow it.

Thank you for your understanding! 🙏"""

        return NotificationService.send_whatsapp_message(user_id, message)

    @staticmethod
    def broadcast_new_book(group_id: str, book_title: str, author: str, genre: str) -> Dict[str, Any]:
        """
        Broadcast a new book announcement to the group.

        Args:
            group_id: WhatsApp group ID
            book_title: Title of the new book
            author: Author name
            genre: Book genre

        Returns:
            Result from send_group_message
        """
        message = f"""📚 New Book Alert!

We've just added a new book to the PTC Library:

📖 {book_title}
✍️ by {author}
🏷️ Genre: {genre}

Come and borrow it today! 📚✨"""

        return NotificationService.send_group_message(group_id, message)

    @staticmethod
    def test_connection() -> Dict[str, Any]:
        """
        Test the Evolution API connection.

        Returns:
            Dict with connection status
        """
        try:
            # Try to fetch instance info
            url = f"{Config.EVOLUTION_API_URL}/instance/fetchInstances"

            headers = {
                "apikey": Config.EVOLUTION_API_KEY
            }

            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "Evolution API connection successful"
                }
            else:
                return {
                    "success": False,
                    "error": f"Connection failed. Status: {response.status_code}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Connection error: {str(e)}"
            }
