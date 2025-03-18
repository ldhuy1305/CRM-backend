from django.urls import include, re_path
from rest_framework.routers import SimpleRouter

from lead.views import LeadViewSet

router = SimpleRouter()
router.register(r"", LeadViewSet, "leads")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
