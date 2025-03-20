from django.db import transaction
from rest_framework import serializers

from account.models import Account
from authentication.models import User
from authentication.serializers import UserSerializer
from common.serializers import BaseDetailSerializer, BaseNameSerializer, BaseSerializer
from contact.models import Contact
from lead.models import Industry, Lead, LeadSource, LeadStatus


class IndustrySerializer(BaseNameSerializer):
    class Meta(BaseNameSerializer.Meta):
        model = Industry


class LeadSourceSerializer(BaseNameSerializer):
    class Meta(BaseNameSerializer.Meta):
        model = LeadSource


class LeadStatusSerializer(BaseNameSerializer):
    class Meta(BaseNameSerializer.Meta):
        model = LeadStatus


class LeadSerializer(BaseSerializer):
    # email = serializers.EmailField()

    class Meta:
        model = Lead
        fields = "__all__"

    def validate_email(self, value):
        lead_id = self.instance.id if self.instance else None
        if Lead.objects.filter(email=value).exclude(id=lead_id).exists():
            raise serializers.ValidationError("This email is used by another lead")
        return value

    def create(self, validated_data):
        super().create(validated_data)
        lead = Lead.objects.create(**validated_data)
        return lead

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class LeadDetailSerializer(BaseDetailSerializer, serializers.ModelSerializer):
    industry = IndustrySerializer(read_only=True)
    lead_source = LeadSourceSerializer(read_only=True)
    lead_status = LeadStatusSerializer(read_only=True)
    lead_owner = UserSerializer(read_only=True)

    class Meta:
        model = Lead
        fields = "__all__"


class ConvertSerializer(serializers.Serializer):
    account_owner = serializers.IntegerField(required=True, write_only=True)
    is_create_deal = serializers.BooleanField(default=False, write_only=True)

    # TODO: create serializer of Deal

    @transaction.atomic
    def update(self, instance, validated_data):
        user = User.objects.get(pk=validated_data["account_owner"])
        user_create = self.context.get("request").user

        data_account = instance.get_data_account_from_lead()
        account = Account.objects.create(
            **data_account,
            account_owner=user,
            created_by=user_create
        )

        data_contact = instance.get_data_contact_from_lead()
        contact = Contact.objects.create(
            **data_contact,
            contact_owner=user,
            created_by=user_create
        )

        instance.delete()
        return dict(account=account, contact=contact)
