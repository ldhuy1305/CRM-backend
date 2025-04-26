from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter

from lead.views import (
    IndustryAPIView,
    LeadSourceAPIView,
    LeadStatusAPIView,
    LeadViewSet,
)

router = SimpleRouter()
router.register(r"", LeadViewSet, "leads")

urlpatterns = [
    path("sources/", LeadSourceAPIView.as_view(), name="lead-source-list"),
    path("statuses/", LeadStatusAPIView.as_view(), name="lead-status-list"),
    path("industries/", IndustryAPIView.as_view(), name="industry-list"),
    path("", include(router.urls)),
]
