from rest_framework import status, viewsets
from rest_framework.response import Response

from lead.models import Lead
from lead.serializers import LeadDetailSerializer, LeadSerializer
from utilities.permissions.custom_permissions import CustomPermission

# Create your views here.


class LeadViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [CustomPermission]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return LeadDetailSerializer
        if self.action in ["create", "update"]:
            return LeadSerializer
        if self.action == "convert":
            return LeadSerializer

    def get_queryset(self):
        return Lead.objects.all()

    def list(self, request, *args, **kwargs):
        is_view_all = getattr(request, "is_view_all", None)
        queryset = self.get_queryset()
        if not is_view_all:
            queryset = queryset.filter(created_by=self.request.user)

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
        # instance.delete()
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
