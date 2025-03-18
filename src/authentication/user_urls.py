from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter

from .views import AddPasswordView, UserViewSet

router = SimpleRouter()
router.register(r"", UserViewSet, "user")

urlpatterns = [
    path("password/", AddPasswordView.as_view(), name="add_password"),
    re_path(r"^", include(router.urls)),
]
