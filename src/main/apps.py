import random

from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        """Location for package configurations"""
        random.seed()
        return True
