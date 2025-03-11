from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from api import settings


def send_mail(subject, template, emails, merge_data={}):
    html_body = render_to_string(template, merge_data)

    msg = EmailMultiAlternatives(
        subject=subject, from_email=settings.ADMIN_EMAIL, to=emails, body=""
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send()
