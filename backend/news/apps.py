from django.apps import AppConfig

class NewsServiceAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals