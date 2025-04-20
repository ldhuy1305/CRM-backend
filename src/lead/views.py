from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.views import SortAndFilterViewSet
from lead.models import Lead, LeadSource, LeadStatus, Industry
from lead.serializers import (
    ConvertSerializer,
    LeadDetailSerializer,
    LeadSerializer,
    LeadSourceSerializer,
    LeadStatusSerializer,
    IndustrySerializer)
from utilities.permissions.custom_permissions import CustomPermission, IsAuthenticated

# Create your views here.

class LeadSourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LeadSource.objects.all()
    serializer_class = LeadSourceSerializer
    permission_classes = [IsAuthenticated]


class LeadStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LeadStatus.objects.all()
    serializer_class = LeadStatusSerializer
    permission_classes = [IsAuthenticated]


class IndustryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [IsAuthenticated]

class LeadViewSet(SortAndFilterViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [CustomPermission]
    model = Lead

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return LeadDetailSerializer
        if self.action in ["create", "update"]:
            return LeadSerializer
        if self.action == "convert":
            return ConvertSerializer

    def get_queryset(self):
        return Lead.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset_by_filter(queryset=self.get_queryset())
        queryset = self.get_queryset_by_sort(queryset)
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
        serializer = self.get_serializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.create(validated_data=serializer.validated_data)
        return Response(LeadDetailSerializer(data).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        serializer = self.get_serializer(instance=instance, data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.update(
            instance=instance, validated_data=serializer.validated_data
        )

        return Response(LeadDetailSerializer(data).data, status=status.HTTP_200_OK)

    @swagger_auto_schema()
    @action(
        detail=True,
        methods=["post"],
        url_path="convert",
    )
    def convert(self, request, pk=None, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        serializer = self.get_serializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=instance, validated_data=serializer.validated_data)
        return Response(data={"msg": "Convert successfully"}, status=status.HTTP_200_OK)
