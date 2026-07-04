"""Django app configuration for Tactical Hub."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TacticalHubConfig(AppConfig):
    """Application configuration for the Tactical Hub domain."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "tactical_hub"
    verbose_name = _("Tactical Hub")

    def ready(self):
        """Register signal handlers when Django loads the app."""
        from . import signals  # noqa: F401
