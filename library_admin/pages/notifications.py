"""WhatsApp Notifications page for PTC Library Admin."""

import reflex as rx
from library_admin.state import State


def notification_templates() -> rx.Component:
    """Quick message templates."""
    return rx.box(
        rx.vstack(
            rx.heading("Quick Templates", size="4"),
            rx.hstack(
                rx.button(
                    "Due Reminder",
                    on_click=State.use_due_reminder_template,
                    variant="soft",
                    size="2",
                ),
                rx.button(
                    "Overdue Alert",
                    on_click=State.use_overdue_alert_template,
                    variant="soft",
                    size="2",
                ),
                rx.button(
                    "New Book",
                    on_click=State.use_new_book_template,
                    variant="soft",
                    size="2",
                ),
                rx.button(
                    "Custom",
                    on_click=State.use_custom_template,
                    variant="soft",
                    size="2",
                ),
                spacing="2",
                wrap="wrap",
            ),
            spacing="2",
        ),
        padding="3",
        border_radius="8px",
        border=f"1px solid {rx.color('gray', 4)}",
    )


def send_to_user_form() -> rx.Component:
    """Form to send message to individual user."""
    return rx.card(
        rx.vstack(
            rx.heading("Send to User", size="5"),

            # User selection
            rx.text("Select User", size="2", weight="bold"),
            rx.select(
                [f"{u.get('name', 'Unknown')} ({u.get('user_id', '')})" for u in State.users],
                placeholder="Choose a user...",
                value=State.notify_selected_user,
                on_change=State.set_notify_selected_user,
                size="2",
            ),

            # Or manual phone number
            rx.text("Or enter phone number", size="2", weight="bold", color="gray"),
            rx.input(
                placeholder="61412345678 (with country code)",
                value=State.notify_phone_number,
                on_change=State.set_notify_phone_number,
                size="2",
            ),

            # Message
            rx.text("Message", size="2", weight="bold"),
            rx.text_area(
                placeholder="Enter your message...",
                value=State.notify_message,
                on_change=State.set_notify_message,
                rows="5",
            ),

            # Character count
            rx.text(
                f"Characters: {State.notify_message.length()}",
                size="1",
                color="gray",
            ),

            # Send button
            rx.button(
                rx.icon("send", size=16),
                "Send Message",
                on_click=State.send_notification_to_user,
                size="3",
                width="100%",
            ),

            spacing="3",
            width="100%",
        ),
    )


def send_to_group_form() -> rx.Component:
    """Form to send broadcast message to group."""
    return rx.card(
        rx.vstack(
            rx.heading("Broadcast to Group", size="5"),

            # Group ID
            rx.text("Group ID", size="2", weight="bold"),
            rx.input(
                placeholder="Enter WhatsApp group ID",
                value=State.notify_group_id,
                on_change=State.set_notify_group_id,
                size="2",
            ),
            rx.text(
                "Get the group ID from WhatsApp or Evolution API",
                size="1",
                color="gray",
            ),

            # Message
            rx.text("Message", size="2", weight="bold"),
            rx.text_area(
                placeholder="Enter broadcast message...",
                value=State.notify_group_message,
                on_change=State.set_notify_group_message,
                rows="5",
            ),

            # Character count
            rx.text(
                f"Characters: {State.notify_group_message.length()}",
                size="1",
                color="gray",
            ),

            # Send button
            rx.button(
                rx.icon("megaphone", size=16),
                "Send Broadcast",
                on_click=State.send_notification_to_group,
                size="3",
                width="100%",
                color_scheme="orange",
            ),

            spacing="3",
            width="100%",
        ),
    )


def connection_status() -> rx.Component:
    """Evolution API connection status."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading("API Status", size="4"),
                rx.spacer(),
                rx.button(
                    rx.icon("refresh-cw", size=16),
                    "Test",
                    on_click=State.test_evolution_api,
                    variant="soft",
                    size="2",
                ),
                width="100%",
                align="center",
            ),

            rx.cond(
                State.evolution_api_status == "connected",
                rx.callout(
                    "Evolution API is connected",
                    icon="check-circle",
                    color_scheme="green",
                    size="1",
                ),
            ),
            rx.cond(
                State.evolution_api_status == "disconnected",
                rx.callout(
                    State.evolution_api_error,
                    icon="x-circle",
                    color_scheme="red",
                    size="1",
                ),
            ),
            rx.cond(
                State.evolution_api_status == "testing",
                rx.hstack(
                    rx.spinner(size="1"),
                    rx.text("Testing connection...", size="1"),
                    spacing="2",
                ),
            ),

            spacing="2",
            width="100%",
        ),
        variant="surface",
    )


def notifications_page() -> rx.Component:
    """Main notifications page."""
    return rx.box(
        rx.vstack(
            # Header
            rx.heading("WhatsApp Notifications", size="6"),

            # Messages
            rx.cond(
                State.success_message != "",
                rx.callout(
                    State.success_message,
                    icon="circle-check",
                    color_scheme="green",
                    size="1",
                    on_click=State.clear_messages,
                ),
            ),
            rx.cond(
                State.error_message != "",
                rx.callout(
                    State.error_message,
                    icon="circle-alert",
                    color_scheme="red",
                    size="1",
                    on_click=State.clear_messages,
                ),
            ),

            # Connection status
            connection_status(),

            # Templates
            notification_templates(),

            # Forms
            rx.box(
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger("Send to User", value="user"),
                        rx.tabs.trigger("Broadcast to Group", value="group"),
                    ),
                    rx.tabs.content(
                        send_to_user_form(),
                        value="user",
                    ),
                    rx.tabs.content(
                        send_to_group_form(),
                        value="group",
                    ),
                    default_value="user",
                ),
                width="100%",
            ),

            spacing="3",
            padding="3",
            width="100%",
        ),
    )
