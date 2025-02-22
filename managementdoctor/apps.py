from django.apps import AppConfig

class ManagementdoctorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'managementdoctor'

    def ready(self):
        import managementdoctor.signals  # Import signals