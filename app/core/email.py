import logging
from _socket import gaierror
from smtplib import SMTPAuthenticationError, SMTPNotSupportedError

from django.contrib.sites.models import Site
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

app_log = logging.getLogger('zampo.app.core')


def send_zampo_email(email_info, att_file=None, att_bytes=None):
    """
    email_info:
    - subjec
    - to
    - msg_txt
    - msg_html
    """
    
    
    email = EmailMultiAlternatives(subject=email_info['subject'], body=email_info['msg_txt'], to=email_info['to'])

    if 'msg_html' in email_info:
        email.attach_alternative(email_info['msg_html'], 'text/html')

    if att_file:
        for attachment in att_file:
            email.attach_file(attachment)

    if att_bytes:
        for attachment in att_bytes:
            email.attach(*attachment)

    try:
        email.send()
    except SMTPAuthenticationError as e:
        app_log.error(f'send_zampo_mail - Wrong credentials: {e}')
    except SMTPNotSupportedError as e:
        app_log.error(f'send_zampo_mail - Wrong TLS setting: {e}')
    except ConnectionRefusedError as e:
        app_log.error(f'send_zampo_mail - No SMTP server: {e}')
    except gaierror as e:
        app_log.error(f'send_zampo_mail - Wrong SMTP server: {e}')
    except TimeoutError as e:
        app_log.error(f'send_zampo_mail - No response (wrong SMTP port?): {e}')