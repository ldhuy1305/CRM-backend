from django.urls import include, re_path
from rest_framework.routers import SimpleRouter

from account.views import AccountViewSet

router = SimpleRouter()
router.register(r"", AccountViewSet, "accounts")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
