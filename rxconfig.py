"""Reflex configuration for PTC Library Admin Dashboard."""

import reflex as rx
import os

# Determine if running in production (Docker)
is_prod = os.getenv("REFLEX_ENV", "dev") == "prod"

config = rx.Config(
    app_name="library_admin",
    api_url="http://0.0.0.0:8000" if is_prod else "http://localhost:8000",
    frontend_port=3000,
    backend_port=8000,
    backend_host="0.0.0.0" if is_prod else "localhost",
    telemetry_enabled=False,
)
