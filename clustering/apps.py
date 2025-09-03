"""App-konfiguration för Django-appen `clustering`."""

from django.apps import AppConfig


class ClusteringConfig(AppConfig):
    """Konfigurationsklass för appen `clustering`.

    Attributes:
        default_auto_field (str): Typ av auto-skapad primärnyckel.
        name (str): Applikationens namn.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "clustering"
