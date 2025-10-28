"""Scheduled notification service for PTC Library Admin."""

from datetime import datetime, timedelta
from typing import List, Dict, Any
from library_admin.services.database import DatabaseService
from library_admin.services.notifications import NotificationService


class ScheduledNotificationService:
    """Service for scheduled automated notifications."""

    @staticmethod
    def send_due_reminders(days_before: int = 2) -> Dict[str, Any]:
        """
        Send reminders for books due soon.

        Args:
            days_before: Send reminder X days before due date

        Returns:
            Dict with results: total, success, failed counts and details
        """
        results = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "details": []
        }

        try:
            # Get all active loans
            loans = DatabaseService.get_active_loans()

            # Filter loans that are due soon (but not overdue)
            target_date = datetime.now().date()
            due_soon_loans = [
                loan for loan in loans
                if loan.get('status') == 'due_soon'
                and loan.get('days_remaining') == days_before
            ]

            results["total"] = len(due_soon_loans)

            # Send reminder for each loan
            for loan in due_soon_loans:
                user_id = loan.get('user_id')
                book_title = loan.get('title')
                due_date = loan.get('due_date')

                if not user_id or not book_title:
                    results["failed"] += 1
                    results["details"].append({
                        "loan_id": loan.get('loan_id'),
                        "status": "failed",
                        "error": "Missing user_id or book_title"
                    })
                    continue

                # Send reminder
                result = NotificationService.send_due_reminder(
                    user_id,
                    book_title,
                    due_date
                )

                if result.get("success"):
                    results["success"] += 1
                    results["details"].append({
                        "loan_id": loan.get('loan_id'),
                        "user_id": user_id,
                        "book_title": book_title,
                        "status": "sent"
                    })
                else:
                    results["failed"] += 1
                    results["details"].append({
                        "loan_id": loan.get('loan_id'),
                        "user_id": user_id,
                        "status": "failed",
                        "error": result.get("error")
                    })

        except Exception as e:
            results["error"] = str(e)

        return results

    @staticmethod
    def send_overdue_alerts(days_overdue: int = 1) -> Dict[str, Any]:
        """
        Send alerts for overdue books.

        Args:
            days_overdue: Send alert X days after due date

        Returns:
            Dict with results: total, success, failed counts and details
        """
        results = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "details": []
        }

        try:
            # Get all active loans
            loans = DatabaseService.get_active_loans()

            # Filter overdue loans
            overdue_loans = [
                loan for loan in loans
                if loan.get('status') == 'overdue'
                and abs(loan.get('days_remaining', 0)) >= days_overdue
            ]

            results["total"] = len(overdue_loans)

            # Send alert for each overdue loan
            for loan in overdue_loans:
                user_id = loan.get('user_id')
                book_title = loan.get('title')
                days_late = abs(loan.get('days_remaining', 0))

                if not user_id or not book_title:
                    results["failed"] += 1
                    results["details"].append({
                        "loan_id": loan.get('loan_id'),
                        "status": "failed",
                        "error": "Missing user_id or book_title"
                    })
                    continue

                # Send overdue alert
                result = NotificationService.send_overdue_alert(
                    user_id,
                    book_title,
                    days_late
                )

                if result.get("success"):
                    results["success"] += 1
                    results["details"].append({
                        "loan_id": loan.get('loan_id'),
                        "user_id": user_id,
                        "book_title": book_title,
                        "days_overdue": days_late,
                        "status": "sent"
                    })
                else:
                    results["failed"] += 1
                    results["details"].append({
                        "loan_id": loan.get('loan_id'),
                        "user_id": user_id,
                        "status": "failed",
                        "error": result.get("error")
                    })

        except Exception as e:
            results["error"] = str(e)

        return results

    @staticmethod
    def get_notification_summary() -> Dict[str, Any]:
        """
        Get a summary of pending notifications.

        Returns:
            Dict with counts of due soon and overdue books
        """
        try:
            stats = DatabaseService.get_dashboard_stats()

            return {
                "due_soon": stats.get('due_soon', 0),
                "overdue": stats.get('overdue_books', 0),
                "total_pending": stats.get('due_soon', 0) + stats.get('overdue_books', 0)
            }

        except Exception as e:
            return {
                "error": str(e)
            }

    @staticmethod
    def run_daily_notifications() -> Dict[str, Any]:
        """
        Run all daily notifications (due reminders and overdue alerts).

        This method should be called once per day by a cron job or scheduler.

        Returns:
            Combined results from all notification types
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "due_reminders": {},
            "overdue_alerts": {}
        }

        # Send due reminders (2 days before)
        results["due_reminders"] = ScheduledNotificationService.send_due_reminders(days_before=2)

        # Send overdue alerts (1+ days overdue)
        results["overdue_alerts"] = ScheduledNotificationService.send_overdue_alerts(days_overdue=1)

        # Calculate totals
        results["total_sent"] = (
            results["due_reminders"].get("success", 0) +
            results["overdue_alerts"].get("success", 0)
        )
        results["total_failed"] = (
            results["due_reminders"].get("failed", 0) +
            results["overdue_alerts"].get("failed", 0)
        )

        return results
