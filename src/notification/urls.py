from django.urls import path, re_path
from django_notification.api.views.notification import NotificationViewSet
from rest_framework.routers import SimpleRouter

from notification import views
from notification.consumers import NotificationConsumer
from notification.views import NotificationAPIView

# router = SimpleRouter()
# router.register(r"", NotificationViewSet, "notifications")
urlpatterns = [
    # path('test/', views.notification_test, name='notification_test'),
    path('test/', NotificationAPIView.as_view(), name='notification'),
]

websocket_urlpatterns = [
    re_path(r'ws/notifications/(?P<user_id>\d+)/$', NotificationConsumer.as_asgi())
]
