from django.urls import include, re_path
from rest_framework.routers import SimpleRouter

from .views import GroupViewSet

router = SimpleRouter()
router.register(r"", GroupViewSet, "group")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
