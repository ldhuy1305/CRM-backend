from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from api import settings
from authentication.models import User, UserVerifyCode


def _send_mail(subject, template, emails, merge_data):
    html_body = render_to_string(template, merge_data)

    msg = EmailMultiAlternatives(
        subject=subject, from_email=settings.ADMIN_EMAIL, to=emails, body=""
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send()


def send_invited_email(user: User, url):
    merge_data = {"full_name": user.full_name, "url": url}
    subject = "Welcome to UniBeam"
    _send_mail(subject, "emails/invited_email.html", [user.email], merge_data)
    return True


def send_verify_login(user: User, verify_code: UserVerifyCode):
    subject = "Xác thực 2FA"
    merge_data = {
        "code": verify_code.code,
        "full_name": user.full_name,
        "expire_time": settings.TOKEN_EXPIRE,
    }
    _send_mail(subject, "emails/send_code_login.html", [user.email], merge_data)
    return True


def send_password_reset_email(user,url):
    subject = "Reset your password"
    merge_data = {
        "link": url,
        "fullname": user.full_name,
    }
    _send_mail(
        subject,
        "emails/password_reset_confirm.html",
        [user.email],
        merge_data,
    )
    return True
