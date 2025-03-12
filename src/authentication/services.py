import random
import string
from datetime import timedelta

from api import settings
from authentication.serializers import UserVerifySerializer
from django.utils import timezone

from authentication.models import User


def gen_verify_code(user: User):

    gen_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    exp_at = timezone.now() + timedelta(minutes=settings.TOKEN_EXPIRE)

    user_verify_code = {"user": user.id, "code": gen_code, "expired_at": exp_at}

    serializer_user_verify_code = UserVerifySerializer(data=user_verify_code)
    serializer_user_verify_code.is_valid(raise_exception=True)
    serializer_user_verify_code.save()

    return serializer_user_verify_code.data