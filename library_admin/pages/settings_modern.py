"""Modern Settings page with tabs."""

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
)


def settings_form_card() -> rx.Component:
    """Application settings card."""
    return gradient_card(
        rx.vstack(
            rx.text("Application Settings", size="5", weight="bold", color=Colors.white),

            # WhatsApp Group ID
            rx.vstack(
                rx.text("WhatsApp Group ID", size="2", weight="bold", color=Colors.white),
                rx.input(
                    placeholder="120363422718577509",
                    value=State.setting_whatsapp_group_id,
                    on_change=State.set_setting_whatsapp_group_id,
                    size="3",
                ),
                spacing="1",
                width="100%",
            ),

            # Loan Due Days
            rx.vstack(
                rx.text("Loan Due Period (days)", size="2", weight="bold", color=Colors.white),
                rx.input(
                    type="number",
                    placeholder="14",
                    value=State.setting_loan_due_days,
                    on_change=State.set_setting_loan_due_days,
                    size="3",
                ),
                spacing="1",
                width="100%",
            ),

            # Reminder Days Before
            rx.vstack(
                rx.text("Reminder Days Before Due", size="2", weight="bold", color=Colors.white),
                rx.input(
                    type="number",
                    placeholder="2",
                    value=State.setting_reminder_days_before,
                    on_change=State.set_setting_reminder_days_before,
                    size="3",
                ),
                spacing="1",
                width="100%",
            ),

            # Overdue Alert Days
            rx.vstack(
                rx.text("Overdue Alert Days After", size="2", weight="bold", color=Colors.white),
                rx.input(
                    type="number",
                    placeholder="1",
                    value=State.setting_overdue_alert_days_after,
                    on_change=State.set_setting_overdue_alert_days_after,
                    size="3",
                ),
                spacing="1",
                width="100%",
            ),

            # Save button
            modern_button(
                "Save Settings",
                icon="check",
                on_click=State.save_settings,
                width="100%",
                color_scheme="whiteAlpha",
            ),

            spacing="3",
            width="100%",
        ),
        gradient=Gradients.light_blue_gradient,
    )


def bulk_notifications_card() -> rx.Component:
    """Bulk notification buttons."""
    return gradient_card(
        rx.vstack(
            rx.text("Bulk Notifications", size="5", weight="bold", color=Colors.white),
            rx.text(
                "Send alerts to all users with overdue or due-soon books",
                size="2",
                color=Colors.white,
                opacity="0.9",
            ),

            # Overdue alerts
            rx.hstack(
                rx.vstack(
                    rx.text("Overdue Books", size="2", weight="bold", color=Colors.white),
                    rx.text(
                        f"{State.overdue_users_count.to(str)} users",
                        size="1",
                        color=Colors.white,
                        opacity="0.8",
                    ),
                    spacing="0",
                    align="start",
                    flex="1",
                ),
                modern_button(
                    "Send Alerts",
                    icon="alert_triangle",
                    on_click=State.send_overdue_alerts_bulk,
                    color_scheme="red",
                ),
                width="100%",
                align="center",
            ),

            # Due soon reminders
            rx.hstack(
                rx.vstack(
                    rx.text("Due Soon", size="2", weight="bold", color=Colors.white),
                    rx.text(
                        f"{State.due_soon_users_count.to(str)} users",
                        size="1",
                        color=Colors.white,
                        opacity="0.8",
                    ),
                    spacing="0",
                    align="start",
                    flex="1",
                ),
                modern_button(
                    "Send Reminders",
                    icon="clock",
                    on_click=State.send_due_soon_reminders_bulk,
                    color_scheme="orange",
                ),
                width="100%",
                align="center",
            ),

            spacing="3",
            width="100%",
        ),
        gradient=Gradients.navy_gradient,
    )


def settings_page_modern() -> rx.Component:
    """Modern settings page."""
    return modern_page_container(
        # Header
        section_header(
            title="Settings",
            subtitle="Configure your library system",
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

        # Settings form
        settings_form_card(),

        # Bulk notifications
        bulk_notifications_card(),
    )
