from django.urls import path, re_path
from rest_framework.routers import SimpleRouter

from notification import views
from notification.consumers import NotificationConsumer

router = SimpleRouter()
# router.register(r"", NotificationViewSet, "notifications")
urlpatterns = [
    path("", views.notification_page_view, name="notification_page"),
    path('test/', views.notification_test, name='notification_test'),
]

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi())
]
