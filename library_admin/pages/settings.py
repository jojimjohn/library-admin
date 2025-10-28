"""Settings management page for PTC Library Admin."""

import reflex as rx
from library_admin.state import State


def settings_form() -> rx.Component:
    """Application settings form."""
    return rx.card(
        rx.vstack(
            rx.heading("Application Settings", size="5"),

            # WhatsApp Group ID
            rx.vstack(
                rx.text("WhatsApp Group ID", size="2", weight="bold"),
                rx.input(
                    placeholder="Enter WhatsApp group ID...",
                    value=State.setting_whatsapp_group_id,
                    on_change=State.set_setting_whatsapp_group_id,
                    size="2",
                ),
                rx.text(
                    "Group ID for broadcasting announcements (get from WhatsApp or Evolution API)",
                    size="1",
                    color="gray",
                ),
                spacing="1",
                width="100%",
            ),

            # Loan Due Days
            rx.vstack(
                rx.text("Loan Due Period (days)", size="2", weight="bold"),
                rx.input(
                    type="number",
                    placeholder="14",
                    value=State.setting_loan_due_days,
                    on_change=State.set_setting_loan_due_days,
                    size="2",
                ),
                rx.text(
                    "Number of days before a borrowed book is due (default: 14)",
                    size="1",
                    color="gray",
                ),
                spacing="1",
                width="100%",
            ),

            # Reminder Days Before
            rx.vstack(
                rx.text("Reminder Days Before Due", size="2", weight="bold"),
                rx.input(
                    type="number",
                    placeholder="2",
                    value=State.setting_reminder_days_before,
                    on_change=State.set_setting_reminder_days_before,
                    size="2",
                ),
                rx.text(
                    "Send reminder X days before book is due (default: 2)",
                    size="1",
                    color="gray",
                ),
                spacing="1",
                width="100%",
            ),

            # Overdue Alert Days After
            rx.vstack(
                rx.text("Overdue Alert Days After", size="2", weight="bold"),
                rx.input(
                    type="number",
                    placeholder="1",
                    value=State.setting_overdue_alert_days_after,
                    on_change=State.set_setting_overdue_alert_days_after,
                    size="2",
                ),
                rx.text(
                    "Send overdue alert X days after due date (default: 1)",
                    size="1",
                    color="gray",
                ),
                spacing="1",
                width="100%",
            ),

            # Save button
            rx.button(
                "Save Settings",
                on_click=State.save_settings,
                size="3",
                width="100%",
            ),

            spacing="4",
            width="100%",
        ),
    )


def template_card(template: dict) -> rx.Component:
    """Message template card."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(template["template_name"], size="4"),
                rx.spacer(),
                rx.badge(template["template_type"], variant="soft", size="1"),
                width="100%",
                align="center",
            ),

            rx.cond(
                template.get("description", "") != "",
                rx.text(template["description"], size="1", color="gray"),
            ),

            rx.text_area(
                value=template["message_content"],
                rows="5",
                disabled=True,
                size="1",
            ),

            rx.hstack(
                rx.button(
                    rx.icon("pencil", size=16),
                    "Edit",
                    on_click=lambda: State.open_edit_template_form(template["template_id"]),
                    size="2",
                    variant="soft",
                ),
                spacing="2",
            ),

            spacing="3",
            width="100%",
        ),
    )


def template_form_dialog() -> rx.Component:
    """Template add/edit form."""
    form_title = rx.cond(
        State.template_form_mode == "add",
        "Add Template",
        "Edit Template"
    )

    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=16),
                "Add Template",
                on_click=State.open_add_template_form,
                size="2",
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(form_title, size="5"),

            rx.vstack(
                rx.cond(
                    State.template_form_error != "",
                    rx.callout(State.template_form_error, icon="circle_alert", color_scheme="red", size="1"),
                ),

                # Template name
                rx.vstack(
                    rx.text("Template Name", size="2", weight="bold"),
                    rx.input(
                        value=State.template_form_name,
                        on_change=State.set_template_form_name,
                        placeholder="e.g., custom_reminder",
                        size="2",
                    ),
                    spacing="1",
                    width="100%",
                ),

                # Template type
                rx.vstack(
                    rx.text("Template Type", size="2", weight="bold"),
                    rx.select(
                        ["due_reminder", "overdue_alert", "new_book", "custom"],
                        value=State.template_form_type,
                        on_change=State.set_template_form_type,
                        placeholder="Select type...",
                        size="2",
                    ),
                    spacing="1",
                    width="100%",
                ),

                # Message content
                rx.vstack(
                    rx.text("Message Content", size="2", weight="bold"),
                    rx.text_area(
                        value=State.template_form_content,
                        on_change=State.set_template_form_content,
                        placeholder="Use {book_title}, {due_date}, {days_overdue}, {author}, {genre} as placeholders",
                        rows="6",
                    ),
                    rx.text(
                        "Available placeholders: {book_title}, {due_date}, {days_overdue}, {author}, {genre}, {user_name}",
                        size="1",
                        color="gray",
                    ),
                    spacing="1",
                    width="100%",
                ),

                # Description
                rx.vstack(
                    rx.text("Description (optional)", size="2", weight="bold"),
                    rx.input(
                        value=State.template_form_description,
                        on_change=State.set_template_form_description,
                        placeholder="Brief description...",
                        size="2",
                    ),
                    spacing="1",
                    width="100%",
                ),

                # Actions
                rx.hstack(
                    rx.dialog.close(
                        rx.button("Cancel", variant="soft", size="2", on_click=State.close_template_form),
                    ),
                    rx.dialog.close(
                        rx.button("Save", size="2", on_click=State.save_template),
                    ),
                    spacing="2",
                    justify="end",
                    width="100%",
                ),

                spacing="3",
                width="100%",
            ),
        ),
        open=State.template_form_mode != "",
    )


def targeted_notifications() -> rx.Component:
    """Targeted notification buttons."""
    return rx.card(
        rx.vstack(
            rx.heading("Send Targeted Notifications", size="5"),

            rx.text(
                "Send notifications to specific groups of users based on their loan status.",
                size="2",
                color="gray",
            ),

            # Overdue notifications
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("circle_alert", size=20, color="red"),
                        rx.text("Users with Overdue Books", size="3", weight="bold"),
                        rx.spacer(),
                        rx.badge(State.overdue_users_count.to(str), color_scheme="red"),
                        width="100%",
                        align="center",
                    ),
                    rx.button(
                        rx.icon("send", size=16),
                        f"Send Alert to {State.overdue_users_count.to(str)} Users",
                        on_click=State.send_overdue_alerts_bulk,
                        size="2",
                        color_scheme="red",
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                ),
                padding="3",
                border_radius="8px",
                border=f"1px solid {rx.color('red', 6)}",
            ),

            # Due soon notifications
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("clock", size=20, color="orange"),
                        rx.text("Users with Books Due Soon", size="3", weight="bold"),
                        rx.spacer(),
                        rx.badge(State.due_soon_users_count.to(str), color_scheme="yellow"),
                        width="100%",
                        align="center",
                    ),
                    rx.button(
                        rx.icon("send", size=16),
                        f"Send Reminder to {State.due_soon_users_count.to(str)} Users",
                        on_click=State.send_due_soon_reminders_bulk,
                        size="2",
                        color_scheme="yellow",
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                ),
                padding="3",
                border_radius="8px",
                border=f"1px solid {rx.color('yellow', 6)}",
            ),

            spacing="3",
            width="100%",
        ),
        variant="surface",
    )


def settings_page() -> rx.Component:
    """Main settings page."""
    return rx.box(
        rx.vstack(
            # Header
            rx.heading("Settings", size="6"),

            # Messages
            rx.cond(
                State.success_message != "",
                rx.callout(
                    State.success_message,
                    icon="circle_check",
                    color_scheme="green",
                    size="1",
                    on_click=State.clear_messages,
                ),
            ),
            rx.cond(
                State.error_message != "",
                rx.callout(
                    State.error_message,
                    icon="circle_alert",
                    color_scheme="red",
                    size="1",
                    on_click=State.clear_messages,
                ),
            ),

            # Tabs
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("Application Settings", value="settings"),
                    rx.tabs.trigger("Message Templates", value="templates"),
                    rx.tabs.trigger("Bulk Notifications", value="notifications"),
                ),
                rx.tabs.content(
                    settings_form(),
                    value="settings",
                ),
                rx.tabs.content(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Message Templates", size="5"),
                            rx.spacer(),
                            template_form_dialog(),
                            width="100%",
                            align="center",
                        ),
                        rx.cond(
                            State.templates.length() == 0,
                            rx.callout("No templates found. Add your first template!", icon="info", color_scheme="blue"),
                            rx.vstack(
                                rx.foreach(State.templates, template_card),
                                spacing="3",
                                width="100%",
                            ),
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    value="templates",
                ),
                rx.tabs.content(
                    targeted_notifications(),
                    value="notifications",
                ),
                default_value="settings",
            ),

            spacing="3",
            padding="3",
            width="100%",
        ),
    )
