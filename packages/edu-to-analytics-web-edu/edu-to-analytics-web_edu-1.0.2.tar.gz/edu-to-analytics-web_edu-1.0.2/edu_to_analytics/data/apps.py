from django.apps.config import AppConfig


class AppConfig(AppConfig):

    name = __package__
    label = 'to_analytics_data'
