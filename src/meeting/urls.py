from django.urls import include, re_path
from rest_framework.routers import SimpleRouter

from meeting.views import MeetingViewSet

router = SimpleRouter()
router.register(r"", MeetingViewSet, "meetings")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
