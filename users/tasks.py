# from celery import shared_task
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.conf import settings
# from django.contrib.auth import get_user_model

# User = get_user_model()

# @shared_task
# def send_welcome_email_task(user_id):
#     user = User.objects.get(pk=user_id)
#     subject = f"Welcome to {getattr(settings, 'SITE_NAME', 'Our Site')}, {user.first_name or user.username}"
#     context = {"user": user, "site_name": getattr(settings, "SITE_NAME", "Our Site")}
#     text_body = render_to_string("emails/welcome.txt", context)
#     html_body = render_to_string("emails/welcome.html", context)

#     msg = EmailMultiAlternatives(subject, text_body, settings.DEFAULT_FROM_EMAIL, [user.email])
#     msg.attach_alternative(html_body, "text/html")
#     msg.send()
