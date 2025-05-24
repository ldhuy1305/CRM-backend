import json
from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import datetime, timedelta

import cloudinary.uploader
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.utils.encoding import smart_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, views, viewsets
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api import constants, settings
from authentication.services import gen_verify_code
from utilities.email.mailer import (
    send_invited_email,
    send_password_reset_email,
    send_verify_login,
)
from utilities.permissions.custom_permissions import CustomPermission, IsAuthenticated

from .models import User
from .serializers import (
    AvatarSerializer,
    ChangePasswordSerializer,
    ListUserSerializer,
    LoginSerializer,
    LogoutSerializer,
    MeSerializer,
    PasswordSerializer,
    RegisterSerializer,
    ResetPasswordRequestSerializer,
    SetNewPasswordSerializer,
    UserSerializer,
    VerifyCodeSerializer,
)

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [CustomPermission]

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ["create", "retrieve"]:
            return RegisterSerializer
        if self.action == "list":
            return ListUserSerializer
        if self.action == "update":
            return UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        user_data = serializer.data

        user_data["id"] = user.id
        data = {
            "email": user.email,
            "expired_at": (
                datetime.now() + timedelta(minutes=settings.MAIL_EXPIRE)
            ).strftime(constants.FULL_DAY_FORMAT),
        }
        json_str = json.dumps(data)
        email_encode = urlsafe_b64encode(json_str.encode()).decode("utf-8")

        url = f"{settings.WEBSITE_URL}/invited-email?p={email_encode}"

        send_invited_email(user, url)
        return Response(
            {"user": user_data, "code": email_encode}, status=status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddPasswordView(generics.GenericAPIView):
    serializer_class = PasswordSerializer

    def post(self, request, *args, **kwargs):
        params = request.query_params
        if (encoded_data := params.get("p", None)) is None:
            raise NotFound("Parameter 'p' is missing.")
        try:
            decoded_data = urlsafe_b64decode(encoded_data).decode("utf-8")
            data = json.loads(decoded_data)
            serializer = self.serializer_class(
                data=request.data, context={"email": data.get("email", None)}
            )
            serializer.is_valid(raise_exception=True)
        except (ValueError, json.JSONDecodeError):
            raise NotFound("Invalid data provided.")

        return Response({"message": "User is created"}, status=status.HTTP_201_CREATED)


class LoginAPIView(views.APIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=request.data["email"])
        except User.DoesNotExist:
            raise NotFound("Invalid email")
        # if not user.last_login:
        #     verify_code = gen_verify_code(user)
        #
        #     send_verify_login(user, verify_code)
        #
        #     return Response(
        #         {
        #             "is_send_code": True,
        #             "message": "Send code verify for mail success",
        #         },
        #         status=status.HTTP_200_OK,
        #     )
        # else:
        refresh = user.tokens()
        return Response(
            {"is_send_code": False, "message": "Login successful", **refresh},
            status=status.HTTP_200_OK,
        )


class VerifyCodeAPIView(views.APIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(views.APIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResendCodeAPIView(views.APIView):

    def post(self, request, *args, **kwargs):
        if not request.data.get("email", None):
            raise ValidationError("Please enter email.")
        try:
            user = User.objects.get(email=request.data["email"])
        except User.DoesNotExist:
            raise NotFound("Invalid email")

        verify_code = gen_verify_code(user)

        send_verify_login(user, verify_code)
        return Response(
            {
                "is_send_code": True,
                "message": "Send code verify for mail success",
            },
            status=status.HTTP_200_OK,
        )


class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message: Change password succesfully"}, status=status.HTTP_200_OK
        )


class ResetPasswordAPIView(views.APIView):
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=request.data["email"])

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

        current_site = get_current_site(request=request).domain
        relative_link = reverse(
            "password-reset-confirm",
            kwargs={"uidb64": uidb64, "token": token},
        )
        send_password_reset_email(user, current_site, relative_link)

        return Response(
            {"message": "We have sent you a link to reset your password"},
            status=status.HTTP_200_OK,
        )


class PasswordTokenCheckAPI(views.APIView):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            id_auto_gen = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id_auto_gen)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return HttpResponseRedirect(
                    settings.WEBSITE_URL + "/password-reset?token_valid=False"
                )
            return HttpResponseRedirect(
                settings.WEBSITE_URL
                + "/password-reset?token_valid=True&message=Credentials Valid&uidb64="
                + uidb64
                + "&token="
                + token
            )
        except Exception as e:
            print(e)
            return HttpResponseRedirect(settings.WEBSITE_URL + "?token_valid=False")


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": True, "message": "Password reset success"},
            status=status.HTTP_200_OK,
        )


class MeAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MeSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class UploadAvatarAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AvatarSerializer

    @swagger_auto_schema(request_body=AvatarSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        # Get the authenticated user
        user = request.user

        # Upload image to Cloudinary
        try:
            upload_result = cloudinary.uploader.upload(
                serializer.validated_data["avatar"],
                folder="avatars/",
                resource_type="image",
                use_filename=True,
                unique_filename=False,
            )
            # Update user's avatar with Cloudinary URL
            user.avatar = upload_result["secure_url"]
            user.save()

            return Response(
                {"message": "Avatar uploaded successfully", "avatar_url": user.avatar},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": f"Failed to upload avatar: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
