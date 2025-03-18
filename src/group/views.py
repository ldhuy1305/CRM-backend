from django.contrib.auth.models import Group
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from authentication.models import User
from group.serializers import GroupDetailSerializer, GroupSerializer
from utilities.permissions.custom_permissions import CustomPermission


# Create your views here.
class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [CustomPermission]
    http_method_names = ["get", "post", "put", "delete"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return GroupDetailSerializer
        if self.action in ["create", "update"]:
            return GroupSerializer
        return GroupDetailSerializer

    def get_queryset(self):
        return Group.objects.all()

    def list(self, request, *args, **kwargs):
        name = request.query_params.get("name", None)
        queryset = self.get_queryset()

        if name:
            queryset = queryset.filter(name__icontains=name)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serialize = self.get_serializer(page, many=True)
            return self.get_paginated_response(serialize.data)
        return Response(
            self.get_serializer(
                queryset,
                many=True,
            ).data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.create(validated_data=serializer.validated_data)
        return Response(
            GroupDetailSerializer(data).data, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.update(
            instance=instance, validated_data=serializer.validated_data
        )

        return Response(GroupDetailSerializer(data).data, status=status.HTTP_200_OK)

    @swagger_auto_schema()
    @action(
        detail=False,
        methods=["post"],
        url_path="(?P<pk>\d+)/assign-users",
    )
    def assign_users(self, request, *args, **kwargs):
        user_ids = request.data.get("user_ids", None)

        instance = self.get_object()
        users = User.objects.filter(id__in=user_ids)
        instance.user_set.add(*users)
        return Response(GroupDetailSerializer(instance).data, status=status.HTTP_200_OK)

    # @swagger_auto_schema()
    # @action(
    #     detail=False,
    #     methods=["post"],
    #     url_path="(?P<pk>\d+)/add-permission",
    # )
    # def assign_users(self, request, *args, **kwargs):
    #     permission_ids = request.data.get("user_ids", None)
    #
    #     instance = self.get_object()
    #     users = User.objects.filter(id__in=user_ids)
    #     instance.user_set.add(*users)
    #     return Response(GroupDetailSerializer(instance).data, status=status.HTTP_200_OK)
