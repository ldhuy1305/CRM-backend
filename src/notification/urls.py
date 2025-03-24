from django.urls import path
from rest_framework.routers import SimpleRouter

from notification.views import NotificationAPIView

router = SimpleRouter()
# router.register(r"", NotificationViewSet, "notifications")

urlpatterns = [
    path("", NotificationAPIView.as_view(), name="notification"),
]
