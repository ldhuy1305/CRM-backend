from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.serializers import UserSerializer
from common.serializers import BaseDetailSerializer, BaseNameSerializer, BaseSerializer
from task.models import Priority, Task, TaskStatus


class PrioritySerializer(BaseNameSerializer):
    class Meta(BaseNameSerializer.Meta):
        model = Priority


class TaskStatusSerializer(BaseNameSerializer):
    class Meta(BaseNameSerializer.Meta):
        model = TaskStatus


class TaskSerializer(BaseSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def create(self, validated_data):
        super().create(validated_data)
        task = Task.objects.create(**validated_data)
        return task

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class TaskDetailSerializer(BaseDetailSerializer):
    from account.serializers import AccountDetailSerializer
    from contact.serializers import ContactDetailSerializer
    from deal.serializers import DealDetailSerializer
    from lead.serializers import LeadDetailSerializer

    task_owner = UserSerializer(read_only=True)
    lead = LeadDetailSerializer(read_only=True)
    contact = ContactDetailSerializer(read_only=True)
    related_account = AccountDetailSerializer(read_only=True)
    related_deal = DealDetailSerializer(read_only=True)
    priority = PrioritySerializer(read_only=True)
    status = TaskStatusSerializer(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"


class TaskCompleteSerializer(serializers.Serializer):
    def update(self, instance, validated_data=None):
        if instance.is_completed:
            return ValidationError("This task is already completed.")

        instance.updated_by = self.context["request"].user
        instance.is_completed = True
        instance.save()

        return instance
