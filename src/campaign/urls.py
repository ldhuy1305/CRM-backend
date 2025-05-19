from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter

from campaign.views import CampaignStatusAPIView, CampaignTypeAPIView, CampaignViewSet

router = SimpleRouter()
router.register(r"", CampaignViewSet, "campaigns")

urlpatterns = [
    path("statuses/", CampaignStatusAPIView.as_view(), name="campaign_status"),
    path("types/", CampaignTypeAPIView.as_view(), name="campaign_types"),
    re_path(r"^", include(router.urls)),
]
