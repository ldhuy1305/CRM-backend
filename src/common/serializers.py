from rest_framework import serializers

from authentication.serializers import UserSerializer
from common.models import BaseNameModel


class BaseSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context["request"].user
        validated_data.update(created_by=user)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data.update(updated_by=user)


class BaseNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseNameModel
        fields = ["id", "name"]


class BaseDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        fields = ["created_by", "updated_by"]
