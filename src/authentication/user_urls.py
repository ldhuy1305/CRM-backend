from django.urls import include, path
from django.urls import re_path as url
from rest_framework.routers import SimpleRouter

from .views import AddPasswordView, UserViewSet

router = SimpleRouter()
router.register(r"", UserViewSet, "user")

urlpatterns = [
    path("password/", AddPasswordView.as_view(), name="add_password"),
    url(r"^", include(router.urls)),
]
