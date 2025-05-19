from django.db import transaction
from rest_framework import serializers

from authentication.serializers import UserSerializer
from campaign.models import Campaign, CampaignStatus, CampaignType
from campaign_target.models import CampaignTarget
from common.serializers import BaseDetailSerializer, BaseNameSerializer, BaseSerializer
from contact.models import Contact
from lead.models import Lead


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


class CampaignTargetSerializer(serializers.Serializer):
    lead = serializers.IntegerField(required=False, allow_null=True)
    contact = serializers.IntegerField(required=False, allow_null=True)

    def update(self, instance, validated_data):
        lead_id = validated_data.get("lead")
        contact_id = validated_data.get("contact")

        return CampaignTarget.objects.create(
            campaign=instance, lead_id=lead_id, contact_id=contact_id
        )


class CampaignTargetLeadDetailSerializer(serializers.ModelSerializer):
    lead_source = serializers.CharField(source="lead_source.name", read_only=True)
    lead_status = serializers.CharField(source="lead_status.name", read_only=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = [
            "id",
            "name",
            "company_name",
            "email",
            "phone",
            "lead_source",
            "lead_status",
        ]

    def get_name(self, obj):
        return obj.get_full_name()


class CampaignTargetContactDetailSerializer(serializers.ModelSerializer):
    contact_owner = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "contact_owner",
        ]

    def get_contact_owner(self, obj):
        if obj.contact_owner:
            return obj.contact_owner.get_full_name()
        return None

    def get_name(self, obj):
        return obj.get_full_name()


class CampaignTargetDetailSerializer(serializers.Serializer):
    lead = CampaignTargetLeadDetailSerializer(read_only=True)
    contact = CampaignTargetContactDetailSerializer(read_only=True)
