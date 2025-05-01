from django.db import transaction
from rest_framework import serializers

from account.serializers import AccountDetailSerializer
from authentication.serializers import UserSerializer
from call.models import Call, CallPurpose, CallResult, CallType
from common.serializers import BaseDetailSerializer, BaseNameSerializer, BaseSerializer
from contact.serializers import ContactDetailSerializer
from deal.serializers import DealDetailSerializer
from lead.serializers import LeadDetailSerializer


class CallTypeDetailSerializer(BaseNameSerializer):
    class Meta:
        model = CallType
        fields = BaseNameSerializer.Meta.fields


class CallPurposeDetailSerializer(BaseNameSerializer):
    class Meta:
        model = CallPurpose
        fields = BaseNameSerializer.Meta.fields


class CallResultDetailSerializer(BaseNameSerializer):
    class Meta:
        model = CallResult
        fields = BaseNameSerializer.Meta.fields


class CallSerializer(BaseSerializer):
    class Meta:
        model = Call
        fields = "__all__"

    def create(self, validated_data):
        super().create(validated_data)
        call = Call.objects.create(**validated_data)

        return call

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class CallDetailSerializer(BaseDetailSerializer):
    call_type = CallTypeDetailSerializer(read_only=True)
    call_purpose = CallPurposeDetailSerializer(read_only=True)
    call_result = CallResultDetailSerializer(read_only=True)
    call_owner = UserSerializer(read_only=True)
    related_deal = DealDetailSerializer(read_only=True)
    related_account = AccountDetailSerializer(read_only=True)
    lead = LeadDetailSerializer(read_only=True)
    contact = ContactDetailSerializer(read_only=True)

    class Meta:
        model = Call
        fields = "__all__"
