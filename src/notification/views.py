import json

from django_celery_beat.models import CrontabSchedule, PeriodicTask
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User


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

        actor = User.objects.get(id=1).id
        recipients = [User.objects.get(id=10).id]

        task, created = PeriodicTask.objects.get_or_create(
            name="notification-1",
            defaults=dict(
                task="api.celery.send_notifica.etion_for_task",
                crontab=schedule,
                args=json.dumps([actor, recipients])
            )
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
