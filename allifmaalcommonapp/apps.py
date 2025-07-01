from django.apps import AppConfig


class AllifmaalcommonappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'allifmaalcommonapp'

# allifmaalcommonapp/apps.py
# allifmaalcommonapp/apps.py

from django.apps import AppConfig

class AllifmaalCommonAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'allifmaalcommonapp'
    verbose_name = "Allifmaal Common Application"

    def ready(self):
        # Import your signals here to ensure they are connected when Django starts
        # This is where Django "discovers" your @receiver functions.
        import allifmaalcommonapp.signals 


