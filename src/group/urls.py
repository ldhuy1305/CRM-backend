from django.urls import include, path
from django.urls import re_path as url
from rest_framework.routers import SimpleRouter

from .views import GroupViewSet

router = SimpleRouter()
router.register(r"", GroupViewSet, "auth")

urlpatterns = [
    url(r"^", include(router.urls)),
]
