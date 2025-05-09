from django.apps import AppConfig


class SerializertopixConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'serializerTopix'

    def ready(self):
        import serializerTopix.signals  # ensures signals are loaded
