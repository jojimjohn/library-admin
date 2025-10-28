#!/usr/bin/env python3
"""
CLI script to send scheduled notifications.

This script should be run daily via cron or systemd timer.

Example crontab entry (run daily at 9 AM):
0 9 * * * cd /path/to/library-admin && python send_scheduled_notifications.py

Example systemd timer:
[Unit]
Description=Send PTC Library scheduled notifications

[Timer]
OnCalendar=daily
OnCalendar=09:00

[Install]
WantedBy=timers.target
"""

import sys
import json
from datetime import datetime
from library_admin.services.scheduled_notifications import ScheduledNotificationService


def main():
    """Run scheduled notifications and output results."""
    print(f"=== PTC Library Scheduled Notifications ===")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    try:
        # Run all daily notifications
        results = ScheduledNotificationService.run_daily_notifications()

        # Display results
        print("Due Reminders:")
        print(f"  Total: {results['due_reminders'].get('total', 0)}")
        print(f"  Sent: {results['due_reminders'].get('success', 0)}")
        print(f"  Failed: {results['due_reminders'].get('failed', 0)}")
        print()

        print("Overdue Alerts:")
        print(f"  Total: {results['overdue_alerts'].get('total', 0)}")
        print(f"  Sent: {results['overdue_alerts'].get('success', 0)}")
        print(f"  Failed: {results['overdue_alerts'].get('failed', 0)}")
        print()

        print(f"Total notifications sent: {results.get('total_sent', 0)}")
        print(f"Total notifications failed: {results.get('total_failed', 0)}")
        print()

        # Output detailed JSON for logging
        print("Detailed Results (JSON):")
        print(json.dumps(results, indent=2))

        # Exit with appropriate code
        if results.get('total_failed', 0) > 0:
            print("\nWARNING: Some notifications failed to send")
            sys.exit(1)
        else:
            print("\nAll notifications sent successfully")
            sys.exit(0)

    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(2)


if __name__ == "__main__":
    main()
