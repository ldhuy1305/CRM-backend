from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter

from task.views import PriorityAPI, TaskStatusAPI, TaskViewSet

router = SimpleRouter()
router.register(r"", TaskViewSet, "deals")

urlpatterns = [
    path("statuses/", TaskStatusAPI.as_view(), name="task-status-list"),
    path("priorities/", PriorityAPI.as_view(), name="priority-list"),
    re_path(r"^", include(router.urls)),
]
