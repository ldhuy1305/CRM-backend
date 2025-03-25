from django.urls import path
from rest_framework.routers import SimpleRouter

from notification.views import NotificationAPIView

from notification import views
router = SimpleRouter()
# router.register(r"", NotificationViewSet, "notifications")
urlpatterns = [
    path("", views.notification_page_view, name="notification_page")
]
