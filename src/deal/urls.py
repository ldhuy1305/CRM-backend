from django.urls import include, re_path
from rest_framework.routers import SimpleRouter

from deal.views import DealViewSet

router = SimpleRouter()
router.register(r"", DealViewSet, "deals")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
