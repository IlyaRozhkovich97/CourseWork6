from django.apps import AppConfig
from time import sleep


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

    def ready(self):
        from mailing.services import start_scheduler
        sleep(2)
        start_scheduler()
