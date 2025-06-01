from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from authentication.models import User
from authentication.serializers import UserSerializer


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):
    content_type = ContentTypeSerializer(read_only=True)

    class Meta:
        model = Permission
        fields = ["id", "name", "content_type"]


class GroupDetailSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    users = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ["id", "name", "permissions", "users"]

    def get_users(self, obj):
        users = obj.user_set.all()
        return UserSerializer(users, many=True).data


class GroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    users = serializers.ListField(child=serializers.IntegerField(), required=False)
    permissions = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )

    class Meta:
        model = Group
        fields = ["id", "name", "users", "permissions"]

    def validate_users(self, value):
        if value and not User.objects.filter(id__in=value).count() == len(value):
            raise serializers.ValidationError("Users do not exist.")
        return value

    def validate_permissions(self, value):
        if value and not Permission.objects.filter(id__in=value).count() == len(value):
            raise serializers.ValidationError("Permissions do not exist.")
        return value

    def create(self, validated_data):
        user_ids = validated_data.pop("users", [])
        permission_ids = validated_data.pop("permissions", [])

        group = Group.objects.create(**validated_data)

        if user_ids:
            group.user_set.set(user_ids)
        if permission_ids:
            group.permissions.set(permission_ids)
        return group

    def update(self, instance, validated_data):
        user_ids = validated_data.pop("users", None)
        permission_ids = validated_data.pop("permissions", None)

        instance.name = validated_data.get("name", instance.name)
        instance.save()

        if user_ids is not None:
            instance.user_set.set(user_ids)

        if permission_ids is not None:
            instance.permissions.set(permission_ids)

        return instance
