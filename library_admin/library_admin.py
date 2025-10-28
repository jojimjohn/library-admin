"""PTC Library Admin Dashboard - Main Application."""

import reflex as rx
from library_admin.state import State
from library_admin.pages.dashboard import dashboard_page
from library_admin.pages.books_v2 import books_page_v2
from library_admin.pages.loans_v2 import loans_page_v2
from library_admin.pages.users import users_page
from library_admin.pages.genres import genres_page
from library_admin.pages.notifications import notifications_page
from library_admin.pages.settings import settings_page


def login_page() -> rx.Component:
    """Login page with password authentication."""
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("PTC Library Admin", size="8", margin_bottom="2"),
                rx.text("Enter admin password to continue", size="2", color="gray"),

                # Error message
                rx.cond(
                    State.auth_error != "",
                    rx.callout(
                        State.auth_error,
                        icon="circle_alert",
                        color_scheme="red",
                        role="alert",
                    ),
                ),

                # Password input
                rx.input(
                    placeholder="Password",
                    type="password",
                    value=State.password_input,
                    on_change=State.set_password_input,
                    on_key_down=lambda key: rx.cond(
                        key == "Enter",
                        State.check_password(),
                        rx.noop(),
                    ),
                    width="100%",
                ),

                # Login button
                rx.button(
                    "Login",
                    on_click=State.check_password,
                    width="100%",
                    size="3",
                ),

                spacing="4",
                width="100%",
            ),
            max_width="400px",
        ),
        height="100vh",
        padding="4",
    )


def navigation_bar() -> rx.Component:
    """Top navigation bar with improved design."""
    return rx.box(
        rx.hstack(
            # Logo/Title area with icon
            rx.hstack(
                rx.icon("library", size=24, color=rx.color("blue", 11)),
                rx.vstack(
                    rx.heading("PTC Library", size="5", color=rx.color("blue", 11)),
                    rx.text("Admin Dashboard", size="1", color="gray"),
                    spacing="0",
                    align="start",
                ),
                spacing="2",
                align="center",
            ),
            rx.spacer(),
            # Settings and Logout
            rx.hstack(
                rx.link(
                    rx.icon_button(
                        rx.icon("settings", size=18),
                        variant="ghost",
                        size="2",
                    ),
                    href="/settings",
                ),
                rx.button(
                    rx.icon("log_out", size=18),
                    "Logout",
                    on_click=State.logout,
                    variant="soft",
                    size="2",
                ),
                spacing="2",
            ),
            width="100%",
            align="center",
            padding="3",
        ),
        background_color=rx.color("gray", 2),
        border_bottom=f"1px solid {rx.color('gray', 6)}",
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1)",
    )


def bottom_navigation() -> rx.Component:
    """Bottom navigation for mobile."""
    return rx.box(
        rx.hstack(
            rx.link(
                rx.vstack(
                    rx.icon("home", size=20),
                    rx.text("Home", size="1"),
                    spacing="1",
                    align="center",
                ),
                href="/",
                text_decoration="none",
                color=rx.cond(
                    State.current_page == "dashboard",
                    rx.color("blue", 11),
                    rx.color("gray", 11),
                ),
                flex="1",
            ),
            rx.link(
                rx.vstack(
                    rx.icon("book", size=20),
                    rx.text("Books", size="1"),
                    spacing="1",
                    align="center",
                ),
                href="/books",
                text_decoration="none",
                color=rx.cond(
                    State.current_page == "books",
                    rx.color("blue", 11),
                    rx.color("gray", 11),
                ),
                flex="1",
            ),
            rx.link(
                rx.vstack(
                    rx.icon("bookmark", size=20),
                    rx.text("Loans", size="1"),
                    spacing="1",
                    align="center",
                ),
                href="/loans",
                text_decoration="none",
                color=rx.cond(
                    State.current_page == "loans",
                    rx.color("blue", 11),
                    rx.color("gray", 11),
                ),
                flex="1",
            ),
            rx.link(
                rx.vstack(
                    rx.icon("library", size=20),
                    rx.text("Genres", size="1"),
                    spacing="1",
                    align="center",
                ),
                href="/genres",
                text_decoration="none",
                color=rx.cond(
                    State.current_page == "genres",
                    rx.color("blue", 11),
                    rx.color("gray", 11),
                ),
                flex="1",
            ),
            rx.link(
                rx.vstack(
                    rx.icon("users", size=20),
                    rx.text("Users", size="1"),
                    spacing="1",
                    align="center",
                ),
                href="/users",
                text_decoration="none",
                color=rx.cond(
                    State.current_page == "users",
                    rx.color("blue", 11),
                    rx.color("gray", 11),
                ),
                flex="1",
            ),
            justify="between",
            align="center",
            padding="2",
        ),
        background_color=rx.color("gray", 2),
        border_top=f"1px solid {rx.color('gray', 6)}",
        position="fixed",
        bottom="0",
        left="0",
        right="0",
        z_index="1000",
    )


def main_layout(page_content: rx.Component) -> rx.Component:
    """Main layout with navigation."""
    return rx.box(
        navigation_bar(),
        rx.box(
            page_content,
            padding_bottom="80px",  # Space for bottom nav
        ),
        bottom_navigation(),
    )


@rx.page(route="/", on_load=State.load_dashboard_data)
def index() -> rx.Component:
    """Dashboard page route."""
    State.current_page = "dashboard"
    return rx.cond(
        State.is_authenticated,
        main_layout(dashboard_page()),
        login_page(),
    )


@rx.page(route="/books", on_load=State.load_books)
def books() -> rx.Component:
    """Books management page route."""
    State.current_page = "books"
    return rx.cond(
        State.is_authenticated,
        main_layout(books_page_v2()),
        login_page(),
    )


@rx.page(route="/loans", on_load=State.load_active_loans)
def loans() -> rx.Component:
    """Loans management page route."""
    State.current_page = "loans"
    return rx.cond(
        State.is_authenticated,
        main_layout(loans_page_v2()),
        login_page(),
    )


@rx.page(route="/users", on_load=State.load_users)
def users() -> rx.Component:
    """Users management page route."""
    State.current_page = "users"
    return rx.cond(
        State.is_authenticated,
        main_layout(users_page()),
        login_page(),
    )


@rx.page(route="/genres", on_load=State.load_genres_list)
def genres() -> rx.Component:
    """Genres management page route."""
    State.current_page = "genres"
    return rx.cond(
        State.is_authenticated,
        main_layout(genres_page()),
        login_page(),
    )


@rx.page(route="/notifications", on_load=State.load_users)
def notifications() -> rx.Component:
    """Notifications page route."""
    State.current_page = "notifications"
    return rx.cond(
        State.is_authenticated,
        main_layout(notifications_page()),
        login_page(),
    )




@rx.page(route="/settings", on_load=[State.load_settings, State.load_templates])
def settings() -> rx.Component:
    """Settings page route."""
    State.current_page = "settings"
    return rx.cond(
        State.is_authenticated,
        main_layout(settings_page()),
        login_page(),
    )


# App configuration
app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        accent_color="blue",
    ),
)
