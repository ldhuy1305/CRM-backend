from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter

from deal.views import DealViewSet, LostReasonAPI, StageAPI

router = SimpleRouter()
router.register(r"", DealViewSet, "deals")

urlpatterns = [
    path("lost-reasons/", LostReasonAPI.as_view(), name="lost-reason-list"),
    path("stages/", StageAPI.as_view(), name="stage-list"),
    re_path(r"^", include(router.urls)),
]
