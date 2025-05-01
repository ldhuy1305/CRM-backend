from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter

from call.views import CallViewSet

router = SimpleRouter()
router.register(r"", CallViewSet, "calls")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
