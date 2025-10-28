"""Modern UI Design System for PTC Library Admin.

Inspired by modern mobile app aesthetics with:
- Gradient backgrounds (light blue to navy)
- Soft shadows and rounded corners
- Minimalist icons and clean typography
- Mobile-first responsive design
"""

import reflex as rx
from typing import Any, Optional


# Color Palette
class Colors:
    """Modern color palette with gradients."""
    # Primary Blues
    light_blue = "#87CEEB"
    sky_blue = "#4FC3F7"
    bright_blue = "#29B6F6"
    navy = "#1A237E"
    dark_navy = "#0D1B3E"

    # Accent Colors
    mint = "#4DD0E1"
    coral = "#FF6B9D"
    purple = "#7C4DFF"

    # Neutrals
    white = "#FFFFFF"
    light_gray = "#F5F7FA"
    gray = "#E0E0E0"
    dark_gray = "#757575"

    # Status Colors
    success_green = "#4CAF50"
    warning_orange = "#FF9800"
    error_red = "#F44336"
    info_blue = "#2196F3"


# Gradient Definitions
class Gradients:
    """Pre-defined gradient backgrounds."""
    # Light gradient (for main cards)
    light_blue_gradient = f"linear-gradient(135deg, {Colors.light_blue} 0%, {Colors.sky_blue} 100%)"

    # Navy gradient (for emphasis cards)
    navy_gradient = f"linear-gradient(135deg, {Colors.navy} 0%, {Colors.dark_navy} 100%)"

    # Mint gradient (for success/positive actions)
    mint_gradient = f"linear-gradient(135deg, {Colors.mint} 0%, {Colors.bright_blue} 100%)"

    # Coral gradient (for special features)
    coral_gradient = f"linear-gradient(135deg, {Colors.coral} 0%, {Colors.purple} 100%)"

    # Subtle background
    subtle_gray = f"linear-gradient(135deg, {Colors.light_gray} 0%, {Colors.white} 100%)"


# Shadow Definitions
class Shadows:
    """Soft drop shadows for layered design."""
    sm = "0 2px 4px rgba(0, 0, 0, 0.05)"
    md = "0 4px 12px rgba(0, 0, 0, 0.08)"
    lg = "0 8px 24px rgba(0, 0, 0, 0.12)"
    xl = "0 12px 32px rgba(0, 0, 0, 0.15)"


def gradient_card(
    *children,
    gradient: str = Gradients.light_blue_gradient,
    **props
) -> rx.Component:
    """Modern card with gradient background and soft shadow.

    Args:
        children: Card content
        gradient: Background gradient (from Gradients class)
        **props: Additional properties
    """
    return rx.box(
        *children,
        background=gradient,
        border_radius="20px",
        padding="4",
        box_shadow=Shadows.md,
        **props
    )


def stat_card_modern(
    title: str,
    value: str,
    icon: str,
    gradient: str = Gradients.light_blue_gradient,
    icon_color: str = Colors.white,
    text_color: str = Colors.white,
) -> rx.Component:
    """Modern statistics card with gradient background.

    Args:
        title: Card title (e.g., "Total Books")
        value: Main value to display (e.g., "127")
        icon: Icon name (lucide icons)
        gradient: Background gradient
        icon_color: Icon color
        text_color: Text color
    """
    return gradient_card(
        rx.vstack(
            # Icon
            rx.box(
                rx.icon(icon, size=32, color=icon_color),
                margin_bottom="2",
            ),
            # Title
            rx.text(
                title,
                size="2",
                weight="medium",
                color=text_color,
                opacity="0.9",
            ),
            # Value
            rx.text(
                value,
                size="8",
                weight="bold",
                color=text_color,
            ),
            spacing="1",
            align="start",
            width="100%",
        ),
        gradient=gradient,
        min_height="140px",
    )


def action_card_modern(
    title: str,
    icon: str,
    href: str = "#",
    gradient: str = Gradients.mint_gradient,
    icon_size: int = 40,
) -> rx.Component:
    """Modern action card with icon and title (clickable).

    Args:
        title: Action title
        icon: Icon name
        href: Link destination
        gradient: Background gradient
        icon_size: Icon size in pixels
    """
    return rx.link(
        gradient_card(
            rx.vstack(
                rx.icon(icon, size=icon_size, color=Colors.white),
                rx.text(
                    title,
                    size="3",
                    weight="bold",
                    color=Colors.white,
                    text_align="center",
                ),
                spacing="3",
                align="center",
                justify="center",
                width="100%",
                min_height="120px",
            ),
            gradient=gradient,
        ),
        href=href,
        text_decoration="none",
        _hover={"transform": "translateY(-2px)", "transition": "transform 0.2s"},
    )


def modern_button(
    text: str,
    icon: Optional[str] = None,
    on_click: Any = None,
    variant: str = "solid",
    color_scheme: str = "blue",
    **props
) -> rx.Component:
    """Modern button with optional icon.

    Args:
        text: Button text
        icon: Optional icon name
        on_click: Click handler
        variant: Button variant (solid, soft, ghost)
        color_scheme: Color scheme
    """
    content = []
    if icon:
        content.append(rx.icon(icon, size=18))
    content.append(rx.text(text, size="2", weight="bold"))

    return rx.button(
        rx.hstack(*content, spacing="2", align="center"),
        on_click=on_click,
        variant=variant,
        color_scheme=color_scheme,
        border_radius="12px",
        size="3",
        **props
    )


def section_header(
    title: str,
    subtitle: Optional[str] = None,
    badge_value: Optional[str] = None,
) -> rx.Component:
    """Modern section header with optional subtitle and badge.

    Args:
        title: Main heading
        subtitle: Optional subtitle text
        badge_value: Optional badge value
    """
    header_content = [
        rx.text(
            title,
            size="7",
            weight="bold",
            color=Colors.dark_navy,
        )
    ]

    if badge_value:
        header_content.append(
            rx.badge(
                badge_value,
                color_scheme="blue",
                size="2",
                border_radius="12px",
            )
        )

    if subtitle:
        return rx.vstack(
            rx.hstack(*header_content, spacing="2", align="center"),
            rx.text(
                subtitle,
                size="2",
                color=Colors.dark_gray,
            ),
            spacing="1",
            align="start",
        )
    else:
        return rx.hstack(*header_content, spacing="2", align="center")


def modern_input(
    placeholder: str = "",
    value: Any = "",
    on_change: Any = None,
    icon: Optional[str] = None,
    **props
) -> rx.Component:
    """Modern input field with optional icon.

    Args:
        placeholder: Placeholder text
        value: Input value
        on_change: Change handler
        icon: Optional leading icon
    """
    if icon:
        return rx.box(
            rx.hstack(
                rx.icon(icon, size=18, color=Colors.dark_gray),
                rx.input(
                    placeholder=placeholder,
                    value=value,
                    on_change=on_change,
                    border="none",
                    _focus={"outline": "none"},
                    flex="1",
                    **props
                ),
                spacing="2",
                align="center",
                width="100%",
            ),
            border=f"1px solid {Colors.gray}",
            border_radius="12px",
            padding="2",
            background=Colors.white,
            _focus_within={
                "border_color": Colors.bright_blue,
                "box_shadow": f"0 0 0 3px rgba(41, 182, 246, 0.1)",
            },
        )
    else:
        return rx.input(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            border_radius="12px",
            size="3",
            **props
        )


def filter_chip(
    text: str,
    is_active: bool = False,
    on_click: Any = None,
    color_scheme: str = "blue",
) -> rx.Component:
    """Modern filter chip/badge.

    Args:
        text: Chip text
        is_active: Whether chip is active/selected
        on_click: Click handler
        color_scheme: Color scheme
    """
    return rx.badge(
        text,
        variant=rx.cond(is_active, "solid", "soft"),
        color_scheme=color_scheme,
        on_click=on_click,
        cursor="pointer",
        border_radius="12px",
        padding_x="3",
        padding_y="1",
        size="2",
        _hover={
            "transform": "scale(1.05)",
            "transition": "transform 0.2s",
        },
    )


def list_item_modern(
    *children,
    **props
) -> rx.Component:
    """Modern list item with hover effect.

    Args:
        children: Item content
    """
    return rx.box(
        *children,
        background=Colors.white,
        border_radius="16px",
        padding="4",
        box_shadow=Shadows.sm,
        _hover={
            "box_shadow": Shadows.md,
            "transform": "translateY(-1px)",
            "transition": "all 0.2s",
        },
        **props
    )


def notification_badge(
    count: int,
    color: str = Colors.error_red,
) -> rx.Component:
    """Notification badge with count.

    Args:
        count: Number to display
        color: Badge color
    """
    return rx.cond(
        count > 0,
        rx.box(
            rx.text(
                str(count) if count < 100 else "99+",
                size="1",
                weight="bold",
                color=Colors.white,
            ),
            background=color,
            border_radius="999px",
            padding_x="2",
            padding_y="1",
            min_width="20px",
            text_align="center",
        ),
    )


def modern_page_container(
    *children,
    **props
) -> rx.Component:
    """Modern page container with proper spacing and background.

    Args:
        children: Page content
    """
    return rx.box(
        rx.vstack(
            *children,
            spacing="4",
            width="100%",
        ),
        background=Colors.light_gray,
        min_height="100vh",
        padding="4",
        padding_bottom="100px",  # Space for bottom nav
        **props
    )


def empty_state(
    icon: str,
    title: str,
    description: str,
    action_text: Optional[str] = None,
    on_action: Any = None,
) -> rx.Component:
    """Modern empty state component.

    Args:
        icon: Icon name
        title: Main title
        description: Description text
        action_text: Optional action button text
        on_action: Optional action handler
    """
    content = [
        rx.icon(icon, size=64, color=Colors.dark_gray, opacity="0.3"),
        rx.text(
            title,
            size="5",
            weight="bold",
            color=Colors.dark_gray,
            text_align="center",
        ),
        rx.text(
            description,
            size="2",
            color=Colors.dark_gray,
            text_align="center",
            opacity="0.7",
        ),
    ]

    if action_text and on_action:
        content.append(
            modern_button(
                action_text,
                on_click=on_action,
                variant="soft",
            )
        )

    return rx.center(
        rx.vstack(
            *content,
            spacing="3",
            align="center",
            padding="8",
        ),
        width="100%",
        min_height="300px",
    )
