from celery import shared_task
from django.apps import apps

@shared_task
def revoke_pswd_reset_otp(user_id):
    user = apps.get_model('core', 'User').objects.get(pk=user_id)
    user.otp_pswd_reset = None
    user.save()