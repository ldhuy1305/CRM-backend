from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ChangePasswordAPIView,
    LoginAPIView,
    LogoutAPIView,
    PasswordTokenCheckAPI,
    RegisterUserView,
    ResendCodeAPIView,
    ResetPasswordAPIView,
    SetNewPasswordAPIView,
    UserViewSet,
    VerifyCodeAPIView,
    VerifyEmailView,
)

router = SimpleRouter()
router.register(r"", UserViewSet, "auth")

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("verify_email/", VerifyEmailView.as_view(), name="verify_email"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("login/verify_code", VerifyCodeAPIView.as_view(), name="verify_code"),
    path("login/resend_code", ResendCodeAPIView.as_view(), name="resend_code"),
    path("change_password/", ChangePasswordAPIView.as_view(), name="resend_code"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("reset_password/", ResetPasswordAPIView.as_view(), name="reset_password"),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordTokenCheckAPI.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset-complete/",
        SetNewPasswordAPIView.as_view(),
        name="password-reset-complete",
    ),
]
