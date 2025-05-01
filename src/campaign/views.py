from rest_framework import status, views, viewsets
from rest_framework.response import Response

from campaign.models import Campaign, CampaignStatus, CampaignType
from campaign.serializers import (
    CampaignDetailSerializer,
    CampaignSerializer,
    CampaignStatusDetailSerializer,
    CampaignTypeSerializer,
)
from common.views import SortAndFilterViewSet
from utilities.permissions.custom_permissions import CustomPermission, IsAuthenticated

# Create your views here.


class CampaignViewSet(SortAndFilterViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [CustomPermission]
    model = Campaign

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CampaignDetailSerializer
        if self.action in ["create", "update"]:
            return CampaignSerializer

    def get_queryset(self):
        return Campaign.objects.all()

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
        return Response(
            CampaignDetailSerializer(data).data, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        serializer = self.get_serializer(instance=instance, data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.update(
            instance=instance, validated_data=serializer.validated_data
        )

        return Response(CampaignDetailSerializer(data).data, status=status.HTTP_200_OK)
