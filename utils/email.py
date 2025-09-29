from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def is_valid_email(email: str) -> bool:
    try:
        EmailValidator()(email)
        return True
    except ValidationError:
        return False

def send_email_notification(subject, template, context, recipient_list):
    recipient_list = [e for e in recipient_list if is_valid_email(e)]
    if not recipient_list:
        return False
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False,
    )
    return True