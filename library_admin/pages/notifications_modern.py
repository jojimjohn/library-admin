"""Modern WhatsApp Notifications page."""

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


def connection_status_modern() -> rx.Component:
    """Modern API status card."""
    return gradient_card(
        rx.vstack(
            rx.hstack(
                rx.text("Evolution API Status", size="4", weight="bold", color=Colors.white),
                rx.spacer(),
                modern_button(
                    "Test",
                    icon="refresh_cw",
                    on_click=State.test_evolution_api,
                    variant="soft",
                    color_scheme="whiteAlpha",
                ),
                width="100%",
                align="center",
            ),

            rx.cond(
                State.evolution_api_status == "connected",
                rx.hstack(
                    rx.icon("circle_check", size=18, color=Colors.white),
                    rx.text("Connected", size="2", color=Colors.white),
                    spacing="2",
                ),
            ),
            rx.cond(
                State.evolution_api_status == "disconnected",
                rx.hstack(
                    rx.icon("circle_x", size=18, color=Colors.white),
                    rx.text(State.evolution_api_error, size="2", color=Colors.white),
                    spacing="2",
                ),
            ),
            rx.cond(
                State.evolution_api_status == "testing",
                rx.hstack(
                    rx.spinner(size="2"),
                    rx.text("Testing connection...", size="2", color=Colors.white),
                    spacing="2",
                ),
            ),

            spacing="3",
            width="100%",
        ),
        gradient=rx.cond(
            State.evolution_api_status == "connected",
            Gradients.mint_gradient,
            Gradients.coral_gradient
        ),
    )


def send_to_user_card() -> rx.Component:
    """Send message to individual user."""
    return gradient_card(
        rx.vstack(
            rx.text("Send to User", size="5", weight="bold", color=Colors.white),

            # User selection
            rx.select(
                State.user_select_options,
                placeholder="Select user...",
                value=State.notify_selected_user,
                on_change=State.set_notify_selected_user,
                size="3",
            ),

            # Or phone number
            rx.input(
                placeholder="Or enter phone (61412345678)",
                value=State.notify_phone_number,
                on_change=State.set_notify_phone_number,
                size="3",
            ),

            # Message
            rx.text_area(
                placeholder="Enter message...",
                value=State.notify_message,
                on_change=State.set_notify_message,
                rows="4",
            ),

            rx.text(
                f"Characters: {State.notify_message.length()}",
                size="1",
                color=Colors.white,
                opacity="0.8",
            ),

            # Send button
            modern_button(
                "Send Message",
                icon="send",
                on_click=State.send_notification_to_user,
                width="100%",
                color_scheme="whiteAlpha",
            ),

            spacing="3",
            width="100%",
        ),
        gradient=Gradients.light_blue_gradient,
    )


def send_to_group_card() -> rx.Component:
    """Send broadcast to group."""
    return gradient_card(
        rx.vstack(
            rx.text("Broadcast to Group", size="5", weight="bold", color=Colors.white),

            # Group ID from settings
            rx.input(
                placeholder="Group ID from settings",
                value=State.setting_whatsapp_group_id,
                disabled=True,
                size="3",
            ),

            rx.cond(
                State.setting_whatsapp_group_id == "",
                rx.text(
                    "⚠️ Configure group ID in Settings",
                    size="1",
                    color=Colors.white,
                ),
                rx.text(
                    "✓ Using saved group ID",
                    size="1",
                    color=Colors.white,
                ),
            ),

            # Message
            rx.text_area(
                placeholder="Enter broadcast message...",
                value=State.notify_group_message,
                on_change=State.set_notify_group_message,
                rows="4",
            ),

            rx.text(
                f"Characters: {State.notify_group_message.length()}",
                size="1",
                color=Colors.white,
                opacity="0.8",
            ),

            # Send button
            modern_button(
                "Send Broadcast",
                icon="megaphone",
                on_click=State.send_notification_to_group,
                width="100%",
                color_scheme="whiteAlpha",
            ),

            spacing="3",
            width="100%",
        ),
        gradient=Gradients.navy_gradient,
    )


def notifications_page_modern() -> rx.Component:
    """Modern notifications page."""
    return modern_page_container(
        # Header
        section_header(
            title="Notifications",
            subtitle="Send WhatsApp messages",
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

        # API Status
        connection_status_modern(),

        # Send to user
        send_to_user_card(),

        # Send to group
        send_to_group_card(),
    )
