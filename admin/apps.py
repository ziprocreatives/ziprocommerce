from django.apps import AppConfig


class AdminConfig(AppConfig):
    name = 'admin'
    label = 'custom_admin'  # To avoid conflict with Django's built-in 'admin' app
