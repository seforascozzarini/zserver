from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from celery import shared_task
from celery.utils.log import get_task_logger

from core.email import send_zampo_email


logger = get_task_logger(__name__)


@shared_task
def send_otp_pswd_reset_email(to, context):
    logger.info('Sending otp for password reset via e-mail')

    email_info = {
        'subject': f'Zampo - {_("Richiesta di reset password")}',
        'to': to,
        'msg_txt': _('Please enable HTML view'),
        'msg_html': render_to_string('emails/reset_password_otp.html', context),
    }
    send_zampo_email(email_info)