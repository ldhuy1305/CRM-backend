from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter

from call.views import CallPurposeAPI, CallResultAPI, CallTypeAPI, CallViewSet

router = SimpleRouter()
router.register(r"", CallViewSet, "calls")

urlpatterns = [
    path("results/", CallResultAPI.as_view(), name="results-list"),
    path("purposes/", CallPurposeAPI.as_view(), name="purposes-list"),
    path("types/", CallTypeAPI.as_view(), name="types-list"),
    re_path(r"^", include(router.urls)),
]
