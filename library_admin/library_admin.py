"""PTC Library Admin Dashboard - Main Application."""

import reflex as rx
from library_admin.state import State
from library_admin.pages.dashboard_modern import dashboard_page
from library_admin.pages.books_modern import books_page_modern
from library_admin.pages.loans_modern import loans_page_modern
from library_admin.pages.users_modern import users_page_modern
from library_admin.pages.genres_modern import genres_page_modern
from library_admin.pages.notifications_modern import notifications_page_modern
from library_admin.pages.settings_modern import settings_page_modern


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
    """Modern top navigation bar with gradient and clean design."""
    return rx.box(
        rx.hstack(
            # Logo/Title area with gradient icon
            rx.hstack(
                rx.box(
                    rx.icon("library", size=24, color="#FFFFFF"),
                    background="linear-gradient(135deg, #4FC3F7 0%, #29B6F6 100%)",
                    border_radius="12px",
                    padding="2",
                ),
                rx.vstack(
                    rx.heading("PTC Library", size="5", color="#1A237E", weight="bold"),
                    rx.text("Admin Dashboard", size="1", color="#757575"),
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
                        border_radius="10px",
                    ),
                    href="/settings",
                ),
                rx.button(
                    rx.icon("log_out", size=16),
                    "Logout",
                    on_click=State.logout,
                    variant="soft",
                    size="2",
                    border_radius="10px",
                ),
                spacing="2",
            ),
            width="100%",
            align="center",
            padding="3",
        ),
        background="linear-gradient(135deg, #F5F7FA 0%, #FFFFFF 100%)",
        border_bottom="1px solid #E0E0E0",
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.05)",
        position="sticky",
        top="0",
        padding_left="10px",
        z_index="999",
    )


def bottom_navigation() -> rx.Component:
    """Modern bottom navigation for mobile with icons and active states."""
    def nav_item(icon: str, label: str, page: str, href: str):
        """Create a navigation item with active state."""
        is_active = State.current_page == page

        return rx.link(
            rx.vstack(
                rx.cond(
                    is_active,
                    rx.box(
                        rx.icon(icon, size=22, color="#FFFFFF"),
                        background="linear-gradient(135deg, #4FC3F7 0%, #29B6F6 100%)",
                        border_radius="12px",
                        padding="2",
                    ),
                    rx.icon(icon, size=22, color="#757575"),
                ),
                rx.text(
                    label,
                    size="1",
                    weight=rx.cond(is_active, "bold", "medium"),
                    color=rx.cond(is_active, "#29B6F6", "#757575"),
                ),
                spacing="1",
                align="center",
            ),
            href=href,
            text_decoration="none",
            flex="1",
            display="flex",
            justify_content="center",
            _hover={
                "transform": "translateY(-2px)",
                "transition": "transform 0.2s",
            },
        )

    return rx.box(
        rx.hstack(
            nav_item("home", "Home", "dashboard", "/"),
            nav_item("book_open", "Books", "books", "/books"),
            nav_item("bookmark", "Loans", "loans", "/loans"),
            nav_item("library", "Genres", "genres", "/genres"),
            nav_item("users", "Users", "users", "/users"),
            justify="between",
            align="center",
            padding="2",
            width="100%",
        ),
        background="linear-gradient(180deg, #FFFFFF 0%, #F5F7FA 100%)",
        border_top="1px solid #E0E0E0",
        box_shadow="0 -2px 8px rgba(0, 0, 0, 0.05)",
        position="fixed",
        bottom="10px",
        left="0",
        right="0",
        z_index="10000",
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


@rx.page(route="/books", on_load=[State.load_books, State.load_genres])
def books() -> rx.Component:
    """Books management page route."""
    State.current_page = "books"
    return rx.cond(
        State.is_authenticated,
        main_layout(books_page_modern()),
        login_page(),
    )


@rx.page(route="/loans", on_load=State.load_active_loans)
def loans() -> rx.Component:
    """Loans management page route."""
    State.current_page = "loans"
    return rx.cond(
        State.is_authenticated,
        main_layout(loans_page_modern()),
        login_page(),
    )


@rx.page(route="/users", on_load=State.load_users)
def users() -> rx.Component:
    """Users management page route."""
    State.current_page = "users"
    return rx.cond(
        State.is_authenticated,
        main_layout(users_page_modern()),
        login_page(),
    )


@rx.page(route="/genres", on_load=State.load_genres_list)
def genres() -> rx.Component:
    """Genres management page route."""
    State.current_page = "genres"
    return rx.cond(
        State.is_authenticated,
        main_layout(genres_page_modern()),
        login_page(),
    )


@rx.page(route="/notifications", on_load=State.load_users)
def notifications() -> rx.Component:
    """Notifications page route."""
    State.current_page = "notifications"
    return rx.cond(
        State.is_authenticated,
        main_layout(notifications_page_modern()),
        login_page(),
    )




@rx.page(route="/settings", on_load=[State.load_settings, State.load_templates])
def settings() -> rx.Component:
    """Settings page route."""
    State.current_page = "settings"
    return rx.cond(
        State.is_authenticated,
        main_layout(settings_page_modern()),
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
