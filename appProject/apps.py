from django.apps import AppConfig

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appProject'

    def ready(self):
        import appProject.signals  # Importa el archivo que contiene las señales