from django.apps import AppConfig
import sys

class MonitoreoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitoreo'

    def ready(self):
        if 'runserver' in sys.argv:
            try:
                from . import mqtt_client
                mqtt_client.start_mqtt()
            except ImportError:
                pass