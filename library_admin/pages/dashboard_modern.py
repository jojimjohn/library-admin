"""Modern Dashboard page for PTC Library Admin - Inspired by modern mobile app design."""

import reflex as rx
from library_admin.state import State
from library_admin.components.modern_ui import (
    Colors,
    Gradients,
    Shadows,
    stat_card_modern,
    action_card_modern,
    modern_page_container,
    section_header,
    modern_button,
)


def welcome_header() -> rx.Component:
    """Welcome header with greeting."""
    return rx.vstack(
        rx.text(
            "Welcome back!",
            size="3",
            weight="medium",
            color=Colors.dark_gray,
        ),
        rx.text(
            "PTC Library Dashboard",
            size="8",
            weight="bold",
            color=Colors.dark_navy,
        ),
        spacing="1",
        align="start",
        width="100%",
        margin_bottom="2",
    )


def stats_grid_modern() -> rx.Component:
    """Modern statistics grid with gradient cards."""
    return rx.vstack(
        # Row 1: Main stats
        rx.grid(
            stat_card_modern(
                title="Total Books",
                value=State.dashboard_stats.get("total_books", 0).to(str),
                icon="book_open",
                gradient=Gradients.light_blue_gradient,
            ),
            stat_card_modern(
                title="Available",
                value=State.dashboard_stats.get("available_books", 0).to(str),
                icon="circle_check",
                gradient=Gradients.mint_gradient,
            ),
            columns="2",
            spacing="4",
            width="100%",
        ),

        # Row 2: Borrowed & Active
        rx.grid(
            stat_card_modern(
                title="Borrowed",
                value=State.dashboard_stats.get("borrowed_books", 0).to(str),
                icon="bookmark",
                gradient=Gradients.coral_gradient,
            ),
            stat_card_modern(
                title="Active Loans",
                value=State.dashboard_stats.get("active_loans", 0).to(str),
                icon="users",
                gradient=Gradients.navy_gradient,
            ),
            columns="2",
            spacing="4",
            width="100%",
        ),

        # Row 3: Alerts (full width for emphasis)
        rx.grid(
            stat_card_modern(
                title="Overdue Books",
                value=State.dashboard_stats.get("overdue_books", 0).to(str),
                icon="circle_alert",
                gradient=f"linear-gradient(135deg, {Colors.error_red} 0%, #C62828 100%)",
            ),
            stat_card_modern(
                title="Due Soon",
                value=State.dashboard_stats.get("due_soon", 0).to(str),
                icon="clock",
                gradient=f"linear-gradient(135deg, {Colors.warning_orange} 0%, #F57C00 100%)",
            ),
            columns="2",
            spacing="4",
            width="100%",
        ),

        spacing="4",
        width="80%",
        align_self="center",
    )


def quick_actions_modern() -> rx.Component:
    """Modern quick action cards."""
    return rx.vstack(
        section_header(
            title="Quick Actions",
            subtitle="Access key features"
        ),

        rx.grid(
            action_card_modern(
                title="Send Notifications",
                icon="send",
                href="/notifications",
                gradient=Gradients.light_blue_gradient,
            ),
            action_card_modern(
                title="Manage Genres",
                icon="library",
                href="/genres",
                gradient=Gradients.navy_gradient,
            ),
            action_card_modern(
                title="View All Users",
                icon="users",
                href="/users",
                gradient=Gradients.mint_gradient,
            ),
            action_card_modern(
                title="Settings",
                icon="settings",
                href="/settings",
                gradient=Gradients.coral_gradient,
            ),
            columns="2",
            spacing="4",
            width="100%",
        ),

        spacing="3",
        width="80%",
        align_self="center",
    )


def dashboard_page() -> rx.Component:
    """Modern dashboard page with gradient cards and clean design."""
    return modern_page_container(
        # Welcome header
        welcome_header(),

        # Loading indicator
        rx.cond(
            State.is_loading,
            rx.center(
                rx.vstack(
                    rx.spinner(size="3", color=Colors.bright_blue),
                    rx.text("Loading...", size="2", color=Colors.dark_gray),
                    spacing="2",
                ),
                padding="8",
            ),
        ),

        # Error message (modern callout)
        rx.cond(
            State.error_message != "",
            rx.box(
                rx.hstack(
                    rx.icon("circle_alert", size=20, color=Colors.error_red),
                    rx.text(
                        State.error_message,
                        size="2",
                        color=Colors.error_red,
                        weight="medium",
                    ),
                    spacing="2",
                    align="center",
                ),
                background=f"{Colors.error_red}15",
                border=f"1px solid {Colors.error_red}",
                border_radius="12px",
                padding="3",
            ),
        ),

        # Statistics grid
        stats_grid_modern(),

        # Quick actions
        quick_actions_modern(),

        # Refresh button
        rx.center(
            modern_button(
                "Refresh Data",
                icon="refresh_cw",
                on_click=State.load_dashboard_data,
                variant="soft",
            ),
            width="100%",
        ),
    )
