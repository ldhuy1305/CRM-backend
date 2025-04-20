from django.urls import include, re_path
from rest_framework.routers import SimpleRouter

from contact.views import ContactViewSet

router = SimpleRouter()
router.register(r"", ContactViewSet, "contacts")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
