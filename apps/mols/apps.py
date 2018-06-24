from django.apps import AppConfig


class MolsConfig(AppConfig):
    name = 'mols'

    def ready(self):
        import mols.signals
