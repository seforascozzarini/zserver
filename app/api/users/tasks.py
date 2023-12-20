from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from celery import shared_task
from celery.utils.log import get_task_logger
from django.apps import apps

from core.email import send_zampo_email

logger = get_task_logger(__name__)


@shared_task
def expire_activation_link(user_id):
    user = apps.get_model('core', 'User').objects.get(pk=user_id)
    if not user.is_active:
        user.delete()

@shared_task
def send_activation_email(to, context):
    logger.info('Sending otp for password reset via e-mail')

    email_info = {
        'subject': f'Zampo - {_("Attivazione account")}',
        'to': to,
        'msg_txt': _('Please enable HTML view'),
        'msg_html': render_to_string('emails/user_activation.html', context),
    }
    send_zampo_email(email_info)