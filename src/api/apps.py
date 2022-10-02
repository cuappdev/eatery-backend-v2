from django.apps import AppConfig

# THis will replace apiconfig
class MenuConfig(AppConfig):
    name = "menu"

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
