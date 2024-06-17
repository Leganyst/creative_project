from django.apps import AppConfig

# Определяет конфигурацию приложения

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
