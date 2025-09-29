# users/utils.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_welcome_email(user):
    subject = "Welcome to My Blog 🎉"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    # Render the HTML content
    html_content = render_to_string("email/welcome_email.html", {"username": user.username})

    # Fallback plain text (in case user’s email doesn’t support HTML)
    text_content = f"Hi {user.username}, thanks for joining our blog platform!"

    # Send email with both plain + HTML versions
    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()