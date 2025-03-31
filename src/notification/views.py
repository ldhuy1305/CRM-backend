import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User

from api.celery import shared_task, send_notification_for_task


class NotificationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Tạo lịch trình chạy mỗi phút
        schedule, _ = CrontabSchedule.objects.get_or_create(
            hour='*',
            minute='*',
            day_of_month='*',
            month_of_year='*',
            day_of_week='*'
        )

        task, created = PeriodicTask.objects.get_or_create(
            name="notification-3",
            defaults=dict(
                task="api.celery.send_notification_for_task",
                crontab=schedule,
                args=json.dumps([1, '1']),
            )
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        result = send_notification_for_task.delay(user.id, user.id)
        return Response({"message": "Task has been triggered", "task_id": result.id}, status=status.HTTP_200_OK)

from django.shortcuts import render

actor = User.objects.get(id=1).id
recipients = [User.objects.get(id=1).id]


# task, created = PeriodicTask.objects.get_or_create(
#     name="notification-1",
#     defaults=dict(
#         task="api.celery.send_notification_for_task",
#         crontab=schedule,
#         args=json.dumps([actor, recipients])
#     )
# )
# task, created = PeriodicTask.objects.get_or_create(
#     name="notification-2",
#     defaults=dict(
#         task="api.celery.shared_task",
#         crontab=schedule,
#     )
# )
# Create your views here.