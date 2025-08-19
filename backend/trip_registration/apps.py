from django.apps import AppConfig


class TripRegistrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trip_registration'
    verbose_name = 'Trip Registration'
    
    def ready(self):
        import trip_registration.signals
