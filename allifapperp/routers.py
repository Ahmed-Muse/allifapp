# dbrouter.py

from django.db import connections

class CommonReplicaRouter:
    """
    A router to control all database operations on models in the
    allifmaalcommonapp.
    """
    
    # A list of Django's built-in app labels that should always use the 'default' database.
    # This prevents errors with tables like django_session, auth_user, etc.
    route_app_labels = {'auth', 'admin', 'sessions', 'contenttypes','allifmaalusersapp','allifmaalcommonapp','allifmaalshaafiapp'}

    def db_for_read(self, model, **hints):
        """
        Reads go to the replica database unless the model is a built-in Django app.
        """
        # If the model is from a built-in Django app, use the default database
        if model._meta.app_label in self.route_app_labels:
            return 'default'

        # Otherwise, check the connections. If 'replica' is available, use it.
        # This is a more robust check than the previous try/except block.
        if 'replica' in connections:
            return 'replica'
        
        # Fallback to the default database if 'replica' is not configured
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Writes always go to the default database.
        """
        # All write operations must go to the primary database
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations between models in the same database.
        """
        # If both models are on the 'default' database, allow the relation
        if obj1._state.db == 'default' and obj2._state.db == 'default':
            return True
        # If both models are on the 'replica' database, allow the relation
        # Note: This is less common in a read-replica setup but good practice.
        elif obj1._state.db == 'replica' and obj2._state.db == 'replica':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Migrations for built-in apps should only run on the default database.
        """
        if app_label in self.route_app_labels:
            return db == 'default'
        # All other migrations should run on the 'default' database
        return db == 'default'

