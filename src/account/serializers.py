from rest_framework import serializers

from account.models import Account, AccountType
from authentication.serializers import UserSerializer
from common.serializers import BaseDetailSerializer, BaseNameSerializer, BaseSerializer
from contact.serializers import ContactDetailSerializer
from lead.serializers import IndustrySerializer


class AccountTypeSerializer(BaseNameSerializer):
    class Meta(BaseNameSerializer.Meta):
        model = AccountType


class RatingSerializer(BaseNameSerializer):
    class Meta(BaseNameSerializer.Meta):
        model = AccountType


class AccountSerializer(BaseSerializer):
    class Meta:
        model = Account
        fields = "__all__"

    def create(self, validated_data):
        super().create(validated_data)
        account = Account.objects.create(**validated_data)
        return account

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AccountDetailSerializer(BaseDetailSerializer):
    account_owner = UserSerializer(read_only=True)
    account_type = AccountTypeSerializer(read_only=True)
    rating = RatingSerializer(read_only=True)
    industry = IndustrySerializer(read_only=True)
    contacts = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        fields = "__all__"

    def get_contacts(self, obj):
        contacts = obj.contacts.all()
        return ContactDetailSerializer(contacts, many=True).data
