from django.urls import include, re_path
from rest_framework.routers import SimpleRouter

from task.views import TaskViewSet

router = SimpleRouter()
router.register(r"", TaskViewSet, "deals")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
