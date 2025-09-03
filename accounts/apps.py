"""App-konfiguration för Django-appen `accounts`."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Konfigurationsklass för appen `accounts`.

    Attributes:
        default_auto_field (str): Typ av auto-skapad primärnyckel.
        name (str): Applikationens namn.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
