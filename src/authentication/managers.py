from cfgv import ValidationError
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email
from utilities.validate_password import validate_password


class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Invalid email")

    def password_validator(self, password):
        validate_password(password)

    def create_user(
        self,
        first_name,
        last_name,
        email,
        address,
        phone,
        password,
        role_id,
    ):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError("Users must have a mail")

        if password:
            self.password_validator(password)
        else:
            raise ValueError("Users must have a password")

        user = self.model(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            phone=phone,
            role_id=role_id,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        email,
        username=None,
        password=None,
    ):
        if password is None:
            raise TypeError("Password should not be none")
        user = self.create_user(
            first_name="",
            last_name="",
            email=email,
            address="",
            phone="",
            password=password,
            role_id=1,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.set_password(password)
        user.save()
        return user