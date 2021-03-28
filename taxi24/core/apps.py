"""
Config core app.
"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        """
        Import signals.
        """
        import core.signals
