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
                rx.button(
                    rx.icon("refresh_cw", size=16),
                    "Test",
                    on_click=State.test_evolution_api,
                    variant="soft",
                    size="2",
                    background="rgba(255, 255, 255, 0.2)",
                    color=Colors.white,
                    _hover={"background": "rgba(255, 255, 255, 0.3)"},
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
            align="start",
        ),
        gradient=rx.cond(
            State.evolution_api_status == "connected",
            Gradients.mint_gradient,
            Gradients.coral_gradient
        ),
        padding="5",
    )


def send_to_user_card() -> rx.Component:
    """Send message to individual user."""
    return gradient_card(
        rx.vstack(
            rx.box(
                rx.text("Send to User", size="5", weight="bold", color=Colors.white),
                text_align="center",
                width="100%",
                margin_bottom="3",
            ),

            # User selection
            rx.vstack(
                rx.text("Select User", size="2", weight="medium", color=Colors.white),
                rx.select(
                    State.user_select_options,
                    placeholder="Select user...",
                    value=State.notify_selected_user,
                    on_change=State.set_notify_selected_user,
                    size="3",
                    width="100%",
                ),
                spacing="2",
                width="100%",
                align="start",
            ),

            # Or phone number
            rx.vstack(
                rx.text("Or Phone Number", size="2", weight="medium", color=Colors.white),
                rx.input(
                    placeholder="61412345678 (with country code)",
                    value=State.notify_phone_number,
                    on_change=State.set_notify_phone_number,
                    size="3",
                    width="100%",
                ),
                spacing="2",
                width="100%",
                align="start",
            ),

            # Message
            rx.vstack(
                rx.text("Message", size="2", weight="medium", color=Colors.white),
                rx.text_area(
                    placeholder="Enter message...",
                    value=State.notify_message,
                    on_change=State.set_notify_message,
                    rows="4",
                    width="100%",
                ),
                rx.text(
                    f"Characters: {State.notify_message.length()}",
                    size="1",
                    color=Colors.white,
                    opacity="0.8",
                ),
                spacing="2",
                width="100%",
                align="start",
            ),

            # Send button
            rx.button(
                rx.icon("send", size=18),
                "Send Message",
                on_click=State.send_notification_to_user,
                width="100%",
                size="3",
                background="rgba(255, 255, 255, 0.2)",
                color=Colors.white,
                _hover={"background": "rgba(255, 255, 255, 0.3)"},
            ),

            spacing="4",
            width="100%",
            align="stretch",
        ),
        gradient=Gradients.light_blue_gradient,
        padding="6",
    )


def send_to_group_card() -> rx.Component:
    """Send broadcast to group."""
    return gradient_card(
        rx.vstack(
            rx.box(
                rx.text("Broadcast to Group", size="5", weight="bold", color=Colors.white),
                text_align="center",
                width="100%",
                margin_bottom="3",
            ),

            # Group ID from settings
            rx.vstack(
                rx.text("Group ID", size="2", weight="medium", color=Colors.white),
                rx.input(
                    placeholder="From settings",
                    value=State.setting_whatsapp_group_id,
                    disabled=True,
                    size="3",
                    width="100%",
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
                spacing="2",
                width="100%",
                align="start",
            ),

            # Message
            rx.vstack(
                rx.text("Broadcast Message", size="2", weight="medium", color=Colors.white),
                rx.text_area(
                    placeholder="Enter broadcast message...",
                    value=State.notify_group_message,
                    on_change=State.set_notify_group_message,
                    rows="4",
                    width="100%",
                ),
                rx.text(
                    f"Characters: {State.notify_group_message.length()}",
                    size="1",
                    color=Colors.white,
                    opacity="0.8",
                ),
                spacing="2",
                width="100%",
                align="start",
            ),

            # Send button
            rx.button(
                rx.icon("megaphone", size=18),
                "Send Broadcast",
                on_click=State.send_notification_to_group,
                width="100%",
                size="3",
                background="rgba(255, 255, 255, 0.2)",
                color=Colors.white,
                _hover={"background": "rgba(255, 255, 255, 0.3)"},
            ),

            spacing="4",
            width="100%",
            align="stretch",
        ),
        gradient=Gradients.navy_gradient,
        padding="6",
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
