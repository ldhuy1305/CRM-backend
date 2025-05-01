from django.db import transaction
from rest_framework import serializers

from authentication.serializers import UserSerializer
from campaign.models import Campaign, CampaignStatus, CampaignType
from common.serializers import BaseDetailSerializer, BaseNameSerializer, BaseSerializer


class CampaignStatusDetailSerializer(BaseNameSerializer):
    class Meta:
        model = CampaignStatus
        fields = BaseNameSerializer.Meta.fields


class CampaignTypeSerializer(BaseNameSerializer):
    class Meta:
        model = CampaignType
        fields = BaseNameSerializer.Meta.fields


class CampaignSerializer(BaseSerializer):

    class Meta:
        model = Campaign
        fields = "__all__"

    def create(self, validated_data):
        super().create(validated_data)
        campaign = Campaign.objects.create(**validated_data)

        return campaign

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class CampaignDetailSerializer(BaseDetailSerializer):
    campaign_type = CampaignTypeSerializer(read_only=True)
    campaign_status = CampaignStatusDetailSerializer(read_only=True)
    campaign_owner = UserSerializer(read_only=True)

    class Meta:
        model = Campaign
        fields = "__all__"
