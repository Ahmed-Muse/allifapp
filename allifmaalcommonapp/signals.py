# allifmaalcommonapp/signals.py
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
import logging
# Import your models (using your 'User' model)
from .models import User,CommonSectorsModel,CommonBaseModel, CommonTaxParametersModel, CommonLogsModel, CommonCompanyDetailsModel
logger = logging.getLogger('allifmaalcommonapp') # Use your app-specific logger
# --- Helper to get the current request user (Signals often need this) ---
# Analogy: A "sticky note" attached to the current operation, saying "This was done by User X."
# This requires a simple middleware to make `request.user` available in signals.

# --- Default Sectors to Create ---
# You can customize this list
DEFAULT_SECTORS = [
    {'name': 'Distribution', 'notes': 'Serves sales and general distribution'},
    {'name': 'Healthcare', 'notes': 'Hospitals, clinics, medical services'},
    {'name': 'Education', 'notes': 'Schools, universities, training centers'},
    {'name': 'Hospitality', 'notes': 'Hotels, restaurants, tourism'},
    {'name': 'Realestate', 'notes': 'Property management, sales, development'},
    {'name': 'Logistics', 'notes': 'Transportation, warehousing, supply chain'},
    {'name': 'Service', 'notes': 'Consulting, IT services, maintenance'},
]
# --- END Default Sectors ---

_current_request = {} # A simple thread-local like dict
class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _current_request['user'] = request.user
        response = self.get_response(request)
        _current_request.clear() # Clear after request to prevent data leakage
        return response

def get_current_user():
    """Retrieves the current authenticated user from the request context."""
    user = _current_request.get('user')
    return user if user and user.is_authenticated else None

# --- Signal Receiver for CommonBaseModel (for AuditLog on save) ---
# This will apply to CommonTaxParametersModel and any other model inheriting CommonBaseModel
@receiver(post_save, sender=CommonBaseModel)
def log_model_save_event(sender, instance, created, **kwargs):
    """
    Creates an AuditLog entry whenever a CommonBaseModel instance (or its child) is saved.
    """
    action_type = 'CREATED' if created else 'UPDATED'
    user = get_current_user() # Get user from middleware or None

    content_type = ContentType.objects.get_for_model(instance)

    change_message = f"{sender.__name__} '{instance.name}' {action_type.lower()}."
    # For a more detailed update log, you'd compare old vs new instance (requires pre_save signal too)
    # For simplicity, we'll just note if it's an update.
    if not created and 'update_fields' in kwargs and kwargs['update_fields']:
        change_message += f" Fields changed: {', '.join(kwargs['update_fields'])}"
    elif not created:
        change_message += " (Full update)"

    CommonLogsModel.all_objects.create(
        owner=user, # Can be None if no user is logged in (e.g., via management command)
        action_type=action_type,
        content_type=content_type,
        object_id=str(instance.pk),
        object_repr=str(instance),
        change_message=change_message
    )
    logger.info(f"AuditLog: {action_type} {sender.__name__} {instance.pk}")


@receiver(post_delete, sender=CommonBaseModel)
def log_model_delete_event(sender, instance, **kwargs):
    """
    Creates an AuditLog entry whenever a CommonBaseModel instance (or its child) is deleted.
    """
    user = get_current_user()
    content_type = ContentType.objects.get_for_model(instance)

    CommonLogsModel.all_objects.create(
        owner=user,
        action_type='Deleted',
        content_type=content_type,
        object_id=str(instance.pk),
        object_repr=str(instance),
        change_message=f"{sender.__name__} '{instance.name}' deleted."
    )
    logger.warning(f"AuditLog: Deleted {sender.__name__} {instance.pk}")


@receiver(user_logged_in, sender=User) # Sender is your custom User model
def log_user_login(sender, request, user, **kwargs):
    """
    Creates an AuditLog entry when a User successfully logs in.
    """
    content_type = ContentType.objects.get_for_model(user)
    CommonLogsModel.all_objects.create(
        owner=user,
        action_type='Login',
        content_type=content_type,
        object_id=str(user.pk),
        object_repr=str(user),
        change_message=f"User '{user.email}' logged in from {request.META.get('REMOTE_ADDR', 'Unknown IP')}."
    )
    logger.info(f"AuditLog: Login for user {user.email}")


@receiver(post_save, sender=CommonCompanyDetailsModel)
def send_new_company_notification(sender, instance, created, **kwargs):
    """
    Sends a notification (simulated by logging) when a new CommonCompanyDetailsModel is created.
    """
    if created:
        logger.info(f"NOTIFICATION: New company '{instance.company}' (ID: {instance.pk}) created. Sending welcome email/notification.")
        # In a real ERP, you might trigger an email sending task here (e.g., with Celery)
        # from some_email_utility import send_welcome_email
        # send_welcome_email(instance.email, instance.company)


# --- NEW: Signal Receiver for User Logout ---
@receiver(user_logged_out, sender=User) # Sender is your custom User model
def log_user_logout(sender, request, user, **kwargs):
    """
    Creates an AuditLog entry when a User successfully logs out.
    """
    # Note: For logout, request.user might already be an AnonymousUser by the time
    # this signal fires, depending on where logout is handled.
    # It's safer to use the 'user' argument provided by the signal.
    
    content_type = ContentType.objects.get_for_model(user)
    CommonLogsModel.all_objects.create(
        owner=user,
        action_type='Logout',
        content_type=content_type,
        object_id=str(user.pk),
        object_repr=str(user),
        change_message=f"User '{user.email}' logged out."
    )
    logger.info(f"AuditLog: Logout for user {user.email}")


# --- NEW: Signal Receiver to Create Default Sectors on First Login ---
@receiver(user_logged_in, sender=User)
def create_default_sectors_on_first_login(sender, request, user, **kwargs):
    """
    Checks if CommonSectorsModel is empty. If so, creates default sectors.
    This ensures initial setup of core data.
    """
    if not CommonSectorsModel.all_objects.exists():
        logger.info(f"CommonSectorsModel is empty. Attempting to create default sectors by user {user.email}.")
        created_count = 0
        for sector_data in DEFAULT_SECTORS:
            try:
                # Use get_or_create to prevent duplicates if multiple users log in simultaneously
                # or if the signal somehow fires multiple times before the check.
                sector, created = CommonSectorsModel.all_objects.get_or_create(
                    name=sector_data['name'],
                    defaults={
                        'notes': sector_data.get('notes', ''),
                        'owner': user # Set the logged-in user as the owner
                    }
                )
                if created:
                    created_count += 1
                    logger.info(f"Created default sector: '{sector.name}' by {user.email}.")
                    # Optionally log this to AuditLog as well
                    content_type = ContentType.objects.get_for_model(sector)
                    CommonLogsModel.all_objects.create(
                        owner=user,
                        action_type='Created_default_sector',
                        content_type=content_type,
                        object_id=str(sector.pk),
                        object_repr=str(sector),
                        change_message=f"Default sector '{sector.name}' created automatically on login."
                    )

            except Exception as e:
                logger.error(f"Failed to create default sector '{sector_data['name']}' by {user.email}: {e}")
        
        if created_count > 0:
            logger.info(f"Successfully created {created_count} default sectors.")
        else:
            logger.info("No new default sectors were created (they might already exist).")
    else:
        logger.debug(f"CommonSectorsModel already contains data. Skipping default sector creation.")

@receiver(post_save, sender=CommonCompanyDetailsModel)
def send_new_company_notification(sender, instance, created, **kwargs):
    """
    Sends a notification (simulated by logging) when a new CommonCompanyDetailsModel is created.
    """
    if created:
        logger.info(f"NOTIFICATION: New company '{instance.company}' (ID: {instance.pk}) created. Sending welcome email/notification.")
