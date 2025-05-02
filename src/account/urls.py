from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter

from account.views import AccountTypeAPI, AccountViewSet, RatingAPI

router = SimpleRouter()
router.register(r"", AccountViewSet, "accounts")

urlpatterns = [
    path("ratings/", RatingAPI.as_view(), name="rating-list"),
    path("types/", AccountTypeAPI.as_view(), name="type-list"),
    re_path(r"^", include(router.urls)),
]
