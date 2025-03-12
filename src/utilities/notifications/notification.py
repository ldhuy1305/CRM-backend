from django.contrib.auth.models import User
from django_notification.models.helper.enums.status_choices import NotificationStatus
from django_notification.models.notification import Notification

# Define the actor and recipients
actor = User.objects.get(username="admin")
recipient = User.objects.get(username="john_doe")

# Create a new notification
Notification.objects.create_notification(
    verb="Logged in to Admin panel",
    actor=actor,
    recipients=[recipient],
    description="User logged in to admin area.",
    status=NotificationStatus.INFO,
    public=True,
    link="https://example.com/admin/dashboard",
    is_sent=True,
)
