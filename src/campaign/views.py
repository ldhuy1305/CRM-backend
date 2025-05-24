from pickle import FALSE

from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from campaign.models import Campaign, CampaignStatus, CampaignType
from campaign.serializers import (
    CampaignDetailSerializer,
    CampaignSerializer,
    CampaignStatusDetailSerializer,
    CampaignTargetContactDetailSerializer,
    CampaignTargetDetailSerializer,
    CampaignTargetLeadDetailSerializer,
    CampaignTargetSerializer,
    CampaignTypeSerializer,
)
from campaign_target.models import CampaignTarget
from common.views import ListAPI, SortAndFilterViewSet
from contact.models import Contact
from lead.models import Lead
from lead.serializers import LeadDetailSerializer, LeadSerializer
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
        if self.action in ["add"]:
            return CampaignTargetSerializer
        return CampaignDetailSerializer

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

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[IsAuthenticated],
        url_path="add",
    )
    def add_member(self, request, pk=None):
        campaign = self.get_object()  # Lấy campaign với pk
        serializer = CampaignTargetSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.update(
            instance=campaign, validated_data=serializer.validated_data
        )

        return Response(
            CampaignTargetDetailSerializer(serialized_data).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["get"],
        url_path="leads",
        permission_classes=[IsAuthenticated],
    )
    def list_leads(self, request, pk=None):
        campaign = self.get_object()
        targets = CampaignTarget.objects.filter(campaign=campaign).select_related(
            "lead"
        )

        queryset = Lead.objects.filter(
            id__in=targets.values_list("lead_id", flat=True).distinct()
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CampaignTargetLeadDetailSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CampaignTargetLeadDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        url_path="contacts",
        permission_classes=[IsAuthenticated],
    )
    def list_contacts(self, request, pk=None):
        campaign = self.get_object()
        targets = CampaignTarget.objects.filter(campaign=campaign).select_related(
            "contact"
        )

        queryset = Contact.objects.filter(
            id__in=targets.values_list("contact_id", flat=True).distinct()
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CampaignTargetContactDetailSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CampaignTargetContactDetailSerializer(queryset, many=True)
        return Response(serializer.data)


class CampaignStatusAPIView(ListAPI):
    serializer_class = CampaignStatusDetailSerializer


class CampaignTypeAPIView(ListAPI):
    serializer_class = CampaignTypeSerializer
